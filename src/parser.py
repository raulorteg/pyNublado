import numpy as np
import pandas as pd 
import pathlib
import os
import warnings
import hashlib
import subprocess

class OutputParser:
    def __init__(self):
        pass

    def __call__(path:str):
        self.parse(path)

    def parse(self, path:str):
        """
        Main method of the class, calls all other implemented
        parsing methods.
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
        the combination of inputs. THe method starts by hashing all inputs individually,
        then it concatenates the hashed inputs and hashes again this concatenated single element
        to obtain the final hash to be used as an id of the combination of inputs. The hashing
        protocol used is MD5.

        :param list inputs: list of float inputs to be used in producing the unique hash id
        :return str hash_:  unique hash id
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

        :param pathlib.PosixPath path: path to the .npy file containing the
        input parameters combinations
        :return pandas.DataFrame inputs: input parameter combinations as a pandas Dataframe
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
        column_names = ["gas_density",
                "gas_phase_metallicity",
                "Redshift",
                "ionization_parameter",
                "stellar_metallicity",
                "stellar_age"]

        inputs = pd.DataFrame(inputs, columns=column_names)
        inputs["id"] = hashes_column

        # save the file in pickle format
        inputs.to_pickle(save_path)

        self.inputs = inputs
        return inputs

    def status_to_int(self, status:str):
        """
        Method to map the different exit status of the ran models
        into an index. 0=succesfull, 1=aborted,
        2=unfinished/didnt converge, 3=empty, 4=didnt exist

        :param str status: line containing the exit status of the model
        :return int status_code: mapped status code int.
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
        :return str hash_: string hash id of the model
        """
        hash_ = self.inputs.iloc[index].id
        return hash_
        
    def parse_status(self, path:pathlib.PosixPath):
        """
        Given the path to the "done" directory
        where finished models are saved, this method looks at the 
        last line of the model.out files to extract how did the model exited
        (e.g it was succesfull, it aborted, it didnt converge, ....)
        this status codes are represented by an int: 0=succesfull, 1=aborted,
        2=unfinished/didnt converge, 3=empty, 4=didnt exist. THe method then saves
        the extracted information in a pandas dataframe and serializes it with pickle.

        :param pathlib.PosixPath path: path to the "done" directory
        """
        save_path = path.parent.joinpath("status.pkl")

        status_codes, indexes, hashes, times = [], [], [], []
        for item in path.iterdir():
            out_file = item.joinpath("model.out")
            index = str(out_file.parent).split("/")[-1]
            if out_file.exists():
                
                line = subprocess.check_output(['tail', '-1', out_file])
                line = bytes.decode(line)
                status_code = self.status_to_int(line)

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
            indexes.append(index)
            status_codes.append(status_code)
            hashes.append(self.index_to_hash(int(index)))
        
        status_df = pd.DataFrame()
        status_df["index_model"] = indexes
        status_df["status"] = status_codes
        status_df["hashes"] = hashes
        status_df["time"] = times
        status_df.to_pickle(save_path)
        print(status_df)
        del status_df
    
    def parse_emis(self, path:pathlib.PosixPath):
        exit()
        save_path = path.parent.joinpath("emis.pkl")

        indexes, hashes = [], []
        for item in path.iterdir():
            out_file = item.joinpath("model.emis")
            index = str(out_file.parent).split("/")[-1]
            if out_file.exists():
                
                line = subprocess.check_output(['tail', '-1', out_file])
                line = bytes.decode(line)
                status_code = self.status_to_int(line)
            else:
                status_code = 4 # model.out wasnt created
            indexes.append(index)
            status_codes.append(status_code)
            hashes.append(self.index_to_hash(int(index)))


            
# example
if __name__ == "__main__":
    
    path = "/home/raul/Desktop/sample_N4000"
    output_parser = OutputParser()
    output_parser.parse(path=path)

