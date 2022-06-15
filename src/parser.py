import numpy as np
import pandas as pd 
import pathlib
import os
import warnings
import hashlib
import subprocess

class OutputParser(object):
    """ Parser class used to parse all outputs from CLOUDY and save them into a dataframe
    for future use.
    """
    def __init__(self):
        pass

    def __call__(path:str):
        self.parse(path)

    def parse(self, path:str):
        """
        Main method of the class, calls all other implemented
        parsing methods. Takes as input the path to the folder where all CLOUDY outputs
        are stored.

        :param str path: string path to the folder where the ran models are
        :return: None
        :rtype: None
        """
        raw_path = path
        path = pathlib.Path(path).iterdir()

        # create a dict index to access each subpath
        subdirs = {"todo":None, "done":None, "inputs":None}
        for item in path:
            if "todo" in str(item):
                subdirs["todo"] = item
            elif "done" in str(item):
                subdirs["done"] = item
            elif "parameters" in str(item):
                subdirs["inputs"] = item
        
        # print warning if any of the expected subdirs wasnt found
        for key in subdirs.keys():
            if not subdirs[key]:
                warnings.warn(f"[{key}] subdirectory couldnt be found within the path given ({raw_path}).")
        
        # check /todo subdirectory is empty
        if subdirs["todo"]:
            n_items = 0
            [n_items + 1 for item in subdirs["todo"].iterdir()]
            if n_items > 0:
                warnings.warn(f"TODO folder not empty. Found {n_items} not executed models.")
        
        # load the input parameters as a dataframe to be accessed by all
        # parsing methods
        if subdirs["inputs"]:
            inputs_df = self.parse_inputs(path=subdirs["inputs"])

        # here we list the parsing methods to be executed
        if subdirs["done"]:
            self.parse_status(path=subdirs["done"])
            self.parse_emis(path=subdirs["done"])

    def hash_list(self, inputs:list):
        """
        Given a list of elements produce a unique fixed-limit hash to be used as an id of
        the combination of inputs. The method starts by hashing all inputs individually,
        then it concatenates the hashed inputs and hashes again this concatenated single element
        to obtain the final hash to be used as an id of the combination of inputs. The hashing
        protocol used is MD5.

        :param list inputs: list of float inputs to be used in producing the unique hash id
        :return hash_:  unique hash id
        :rtype: list
        """
        hashed_inputs = []
        for x in inputs:
            x = bytes(str(x), 'utf-8')
            hashed_inputs.append(hashlib.md5(x).hexdigest())

        merged_hashes = ""
        for x in hashed_inputs:
            merged_hashes = merged_hashes + x
        merged_hashes = bytes(merged_hashes, 'utf-8')
        # hash the concatenated hash
        return hashlib.md5(merged_hashes).hexdigest()


    def parse_inputs(self, path:pathlib.PosixPath):
        """
        Method that given the path to the .npy file containing
        the inputs loads it, converts it into a dataframe to be used in the other
        methods and computes the id column by hashing the inputs.

        :param pathlib.PosixPath path: path to the .npy file containing the input parameters combinations
        :return inputs: input parameter combinations as a pandas Dataframe
        :rtype: pandas.DataFrame
        """

        save_path = path.parent.joinpath("inputs.pkl")
        
        inputs = np.load(path)
        hashes_column = []
        for inputs_list in inputs:
            hashes_column.append(self.hash_list(inputs_list))

        column_names = ["gas_density",
                "gas_phase_metallicity",
                "Redshift",
                "cr_ionization_factor",
                "ionization_parameter",
                "stellar_metallicity",
                "stellar_age"]
        
        # remove this
        #column_names = ["gas_density",
        #        "gas_phase_metallicity",
        #        "Redshift",
        #        "ionization_parameter",
        #        "stellar_metallicity",
        #        "stellar_age"]

        inputs = pd.DataFrame(inputs, columns=column_names)
        inputs["id"] = hashes_column

        # save the file in pickle format
        inputs.to_pickle(save_path)

        self.inputs = inputs
        return inputs

    def status_to_int(self, status:str):
        """
        Method to map the different exit status of the ran models
        into an index. 0=succesfull, 1=aborted, 2=unfinished/didnt converge, 3=empty, 4=didnt exist
        
        :param str status: line containing the exit status of the model
        :return status_code: mapped status code int.
        :rtype: int
        """

        if "Cloudy exited OK" in status:
            return 0

        elif "something went wrong" in status:
            return 1

        else:
            mod_status = status.replace(" ", "")
            mod_status = mod_status.replace("\n", "")
            if len(mod_status) < 0:
                return 2 # model didnt finish
            else:
                return 3 # model got stuck without printing anything

    def index_to_hash(self, index:int):
        """
        Given an int index, look for the hash associated in the inputs
        dataframe and return it.

        :param int index: index of the model
        :return hash: string hash id of the model
        :rtype: str
        """
        return self.inputs.iloc[index].id
        
    def parse_status(self, path:pathlib.PosixPath):
        """
        Given the path to the "done" directory
        where finished models are saved, this method looks at the 
        last line of the model.out files to extract how did the model exited
        (e.g it was succesfull, it aborted, it didnt converge, ....)
        this status codes are represented by an int: 0=succesfull, 1=aborted,
        2=unfinished/didnt converge, 3=empty, 4=didnt exist. Tje method then saves
        the extracted information in a pandas dataframe and serializes it with pickle.

        :param pathlib.PosixPath path: path to the "done" directory
        """
        save_path = path.parent.joinpath("status.pkl")

        status_codes, indexes, hashes, times = [], [], [], []
        for item in path.iterdir():
            out_file = item.joinpath("model.out")
            index = str(out_file.parent).split("/")[-1]
            if out_file.exists():
                
                # read the exit code phrase from the last line in model.out file
                line = subprocess.check_output(['tail', '-1', out_file])
                line = bytes.decode(line)
                status_code = self.status_to_int(line)

                # save the execution time, if present in model.out file
                line = subprocess.check_output(['tail', '-2', out_file])
                line = bytes.decode(line)
                if "ExecTime(s)" in line:
                    subline = line.split()
                    for idx, word in enumerate(subline):
                        if word == "ExecTime(s)":
                            break
                    time = subline[idx+1]
                    times.append(float(time))
                else:
                    times.append(None)

            else:
                status_code = 4 # model.out wasnt created
                times.append(None)
            indexes.append(index)
            status_codes.append(status_code)
            hashes.append(self.index_to_hash(int(index)))
        
        # build the dataframe, by adding all the columns
        status_df = pd.DataFrame()
        status_df["index_model"] = indexes
        status_df["status"] = status_codes
        status_df["hashes"] = hashes
        status_df["time"] = times
        status_df.to_pickle(save_path)

        # let the table of status codes available
        # for other methods of the parser class
        self.status = status_df
        del status_df
    
    def parse_emis_file(self, path:pathlib.PosixPath):
        """
        Given the path to e.g "done/1234" directory
        where a finished model is saved, this method parses the model.emis
        file containing the emission lines and saves it into a dataframe. 
        finally it returns the deepest line in the model, corresponding
        to the outer-most zone (emergent emission). The method then saves
        the extracted information in a pandas dataframe and serializes it with pickle.

        :param pathlib.PosixPath path: path to the e.g "done/1234" directory
        """

        save_path = path.parent.joinpath("emis.pkl")
        with open(path, "r") as f:
            lines = f.readlines()

            # identify the columns (emission lines) to be the header
            header = lines[0].split()
            header_columns = []
            header_columns.append(header[0].replace("#", "")) # this is "#depth"

            buffer = []
            for idx, item in enumerate(header[1:]):
                if len(buffer) == 0:
                    buffer.append(item)
                
                elif "." in item:
                    buffer.append(item)
                    header_columns.append("_".join(buffer))
                    buffer = []
                    
                else:
                    buffer.append(item)
            
            # initialize the dictionary with empty lists
            emis_dict = {}
            for key in header_columns:
                emis_dict[key] = []
            
            # fill in the dicitonary
            for line in lines[1:]:
                splitted_line = line.split()
                for idx, elem in enumerate(splitted_line):
                    try:
                        emis_dict[header_columns[idx]].append(float(elem))
                    except:
                        print(elem)
                        pass
            # convert the dictionary into a pandas dataframe
            emis_df = pd.DataFrame().from_dict(emis_dict)
            emis_df.to_pickle(save_path)

            # return the outer-most emission line results
            emis_max_depth = emis_df[emis_df["depth"] == emis_df["depth"].max()]
            
            # free memory
            del emis_dict
            del emis_df
            return emis_max_depth

    def parse_emis(self, path:pathlib.PosixPath):
        """
        Given the path to "done" directory
        where a finished model is saved, this method parses loops over
        all methods and for each parses the model.emis
        file containing the emission lines. Then creates a dataframe containing
        the outer-most zone (emergent emission) for all models. The method then saves
        the extracted information in a pandas dataframe and serializes it with pickle.

        :param pathlib.PosixPath path: path to the e.g "done" directory
        """

        save_path = path.parent.joinpath("emis.pkl")

        emis_df, indexes, hashes, status = [], [], [], []
        for item in path.iterdir():
            print(item)
            emis_file = item.joinpath("model.emis")
            index = str(emis_file.parent).split("/")[-1]

            # check if status_code of index model is "OK"
            exit_code = self.status[self.status["index_model"] == index].status.values[0]
            if (emis_file.exists()) and (exit_code == 0):
                df = self.parse_emis_file(emis_file)
                emis_df.append(df)
                    
                indexes.append(index)
                hashes.append(self.index_to_hash(int(index)))
                
            
        emis_dataframe = pd.concat(emis_df)
        emis_dataframe["index_model"] = indexes
        emis_dataframe["hashes"] = hashes
        emis_dataframe.to_pickle(save_path)
        del emis_dataframe

# example
if __name__ == "__main__":
    
    path = "/home/raul/Desktop/sample_N4000"
    output_parser = OutputParser()
    output_parser.parse(path=path)



