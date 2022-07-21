import numpy as np
import pandas as pd 
import pathlib
import os, re
import warnings
import hashlib
import subprocess
from tqdm import tqdm

from common.settings import SAMPLE_SUBDIR_TODO, SAMPLE_SUBDIR_DONE, INPUT_PARAMETER_NAMES, EXIT_STATUSES


class OutputParser(object):
    """ Parser class used to parse all outputs from CLOUDY and save them into a dataframe
    for future use.
    """
    def __init__(self):
        pass

    def __call__(path: str):
        self.parse(path)

    def parse(self, path: str):
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

        # create a dict index to access each sub-path
        sub_dirs = {SAMPLE_SUBDIR_TODO: None, SAMPLE_SUBDIR_DONE: None, "inputs": None}
        for item in path:
            if SAMPLE_SUBDIR_TODO in str(item):
                sub_dirs[SAMPLE_SUBDIR_TODO] = item
            elif SAMPLE_SUBDIR_DONE in str(item):
                sub_dirs[SAMPLE_SUBDIR_DONE] = item
            elif "parameters" in str(item):
                sub_dirs["inputs"] = item
        
        # print warning if any of the expected subdirectories were not found
        for key in sub_dirs.keys():
            if not sub_dirs[key]:
                warnings.warn(f"[{key}] subdirectory could not be found within the path given ({raw_path}).")
        
        # check if the todo subdirectory is empty
        if sub_dirs[SAMPLE_SUBDIR_TODO]:
            n_items = 0
            [n_items + 1 for item in sub_dirs[SAMPLE_SUBDIR_TODO].iterdir()]
            if n_items > 0:
                warnings.warn(f"{SAMPLE_SUBDIR_TODO} folder not empty. Found {n_items} not executed models.")
        
        # load the input parameters as a dataframe (to be accessed by all parsing methods)
        if sub_dirs["inputs"]:
            inputs_df = self.parse_inputs(path=sub_dirs["inputs"])
            N_models_in_sample = len(inputs_df)
        else:
            N_models_in_sample = 0          # Fallback. Value only used in tqdm progress bar, won't fail

        # here we list the parsing methods to be executed
        if sub_dirs[SAMPLE_SUBDIR_DONE]:
            self.parse_status(path=sub_dirs[SAMPLE_SUBDIR_DONE], N_models=N_models_in_sample)
            self.parse_emis(path=sub_dirs[SAMPLE_SUBDIR_DONE], N_models=N_models_in_sample)
            self.parse_cont(path=sub_dirs[SAMPLE_SUBDIR_DONE], N_models=N_models_in_sample)

    def hash_list(self, inputs: list):
        """
        Given a list of elements produce a unique fixed-limit hash to be used as an id of
        the combination of inputs. The method starts by hashing all inputs individually,
        then it concatenates the hashed inputs and hashes again this concatenated single element
        to obtain the final hash to be used as an id of the combination of inputs. The hashing
        protocol used is MD5.

        :param list inputs: list of float inputs to be used in producing the unique hash id
        :return hash:  unique hash id
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

    def parse_inputs(self, path: pathlib.PosixPath):
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

        print('Parser: Hashing input parameters')
        for inputs_list in tqdm(inputs):
            hashes_column.append(self.hash_list(inputs_list))

        column_names = INPUT_PARAMETER_NAMES

        inputs = pd.DataFrame(inputs, columns=column_names)
        inputs["id"] = hashes_column

        # save the file in pickle format
        inputs.to_pickle(save_path)

        self.inputs = inputs
        return inputs

    def status_to_int(self, tail: str):
        """
        Method to map the different exit status of the ran models
        into an index as per the dictionary of exit codes in settings.py
        
        :param str tail: line containing the exit status of the model
        :return status_code: mapped status code int.
        :rtype: int
        """
            
        if "Cloudy exited OK" in tail:
            return EXIT_STATUSES["Success"]

        elif tail == '':
            return EXIT_STATUSES["DNR"]

        elif 'ABORT' in tail:
            return EXIT_STATUSES["Abort"]

        elif 'something went wrong' in tail:
            return EXIT_STATUSES["Wrong"]

        elif 'unphysical' in tail or 'negative population' in tail:
            return EXIT_STATUSES["Unphysical"]

        elif 'did not converge' in tail:
            return EXIT_STATUSES["Converge"]

        elif "Cloudy exited OK" not in tail:
            return EXIT_STATUSES["DNF"]

    def index_to_hash(self, index: int):
        """
        Given an int index, look for the hash associated in the inputs
        dataframe and return it.

        :param int index: index of the model
        :return hash: string hash id of the model
        :rtype: str
        """
        return self.inputs.iloc[index].id
        
    def parse_status(self, path: pathlib.PosixPath, N_models: int):
        """
        Given the path to the "done" directory
        where finished models are saved, this method looks at the 
        last line of the model.out files to extract how did the model exited
        (e.g it was successful, it aborted, it didnt converge, ....)
        this status codes are represented by an int as per the dictionary in settings.py
        The method then saves the extracted information in a pandas dataframe and serializes
        it with pickle.

        :param pathlib.PosixPath path: path to the "done" directory
        :param int N_models: number of expected models in the sample
        """
        save_path = path.parent.joinpath("status.pkl")

        status_codes, indexes, hashes, times = [], [], [], []

        print('Parser: Parsing run statuses')

        for item in tqdm(path.iterdir(), total=N_models):
            out_file = item.joinpath("model.out")
            index = str(out_file.parent).split("/")[-1]
            if out_file.exists():
                
                # read the exit code phrase from the last line in model.out file
                raw_line = subprocess.check_output(['tail', '-5', out_file])
                raw_line = bytes.decode(raw_line)
                line = re.sub(r'[\n]|\[|\]', '', raw_line)
                status_code = self.status_to_int(line)

                # save the execution time, if present in model.out file,
                # it could not be present if the ran did not finish (DNF)
                if "ExecTime(s)" in raw_line:
                    subline = raw_line.split()
                    for idx, word in enumerate(subline):
                        if word == "ExecTime(s)":
                            break
                    time = subline[idx+1]
                    times.append(float(time))
                else:
                    times.append(None)

            else:
                # model.out was not created, so it did not run DNR
                status_code = EXIT_STATUSES["DNR"]
                times.append(None)

            indexes.append(index)
            status_codes.append(status_code)
            hashes.append(self.index_to_hash(int(index)))
        
        # build the dataframe, by adding all columns
        status_df = pd.DataFrame()
        status_df["index"] = indexes
        status_df["status"] = status_codes
        status_df["id"] = hashes
        status_df["time"] = times
        status_df.to_pickle(save_path)

        # let the table of status codes available
        # for other methods of the parser class, since we can only
        # parse emissions, continuum, ... if the model is successful
        self.status = status_df
        del status_df
    
    def parse_emis_file(self, path: pathlib.PosixPath):
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
            
            # fill in the dictionary
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
            del emis_dict, emis_df
            return emis_max_depth

    def parse_emis(self, path: pathlib.PosixPath, N_models: int):
        """
        Given the path to "done" directory
        where a finished model is saved, this method parses loops over
        all methods and for each parses the model.emis
        file containing the emission lines. Then creates a dataframe containing
        the outer-most zone (emergent emission) for all models. The method then saves
        the extracted information in a pandas dataframe and serializes it with pickle.

        :param pathlib.PosixPath path: path to the e.g "done" directory
        :param int N_models: number of expected models in the sample
        """

        save_path = path.parent.joinpath("emis.pkl")

        emis_df, indexes, hashes, status = [], [], [], []

        print('Parser: Parsing emission line data')

        for item in tqdm(path.iterdir(), total=N_models):
            emis_file = item.joinpath("model.emis")
            index = str(emis_file.parent).split("/")[-1]

            # check if status_code of index model is "OK"
            exit_code = self.status[self.status["index"] == index].status.values[0]
            if (emis_file.exists()) and (exit_code == 0):
                df = self.parse_emis_file(emis_file)
                emis_df.append(df)
                    
                indexes.append(index)
                hashes.append(self.index_to_hash(int(index)))
            
        emis_dataframe = pd.concat(emis_df)
        emis_dataframe["index"] = indexes
        emis_dataframe["id"] = hashes
        emis_dataframe.to_pickle(save_path)
        del emis_dataframe, emis_df, indexes, hashes
    
    def parse_cont_file(self, path: pathlib.PosixPath):
        """
        Given the path to e.g "done/1234" directory
        where a finished model is saved, this method parses the model.cont
        file containing the continuum (incident, reflected, transmitted, ...)
        and saves it into a dataframe. The method then saves the extracted information
        in a pandas dataframe and serializes it with pickle.

        :param pathlib.PosixPath path: path to the e.g "done/1234" directory
        """
        save_path = path.parent.joinpath("cont.pkl")
        cont_dataframe = pd.read_csv(path, sep="\t")
        cont_dataframe.rename(columns={"#Cont  nu": "photon_energy",
                                       "trans": "transmitted",
                                       "reflc": "reflected"},
                              inplace=True)
        cont_dataframe.drop(columns=['reflin', 'outlin', 'lineID', 'cont', 'nLine'], inplace=True)
        cont_dataframe.to_pickle(save_path)
        return cont_dataframe
    
    def parse_cont(self, path:pathlib.PosixPath, N_models: int):
        """
        Given the path to "done" directory
        where a finished model is saved, this method parses loops over
        all different samples and for each parses the model.cont
        file containing the continuum and save it into the folder serializing the
        dataframe with pickle.

        :param pathlib.PosixPath path: path to the e.g "done" directory
        :param int N_models: number of expected models in the sample
        """
        save_path = path.parent.joinpath("cont.pkl")

        cont_df, indexes, hashes, status = [], [], [], []

        print('Parser: Parsing continuum data')

        for item in tqdm(path.iterdir(), total=N_models):
            cont_file = item.joinpath("model.cont")
            index = str(cont_file.parent).split("/")[-1]

            # check if status_code of index model is "OK"
            exit_code = self.status[self.status["index"] == index].status.values[0]
            if (cont_file.exists()) and (exit_code == 0):
                cont_dataframe = self.parse_cont_file(cont_file)

                cont_df.append(cont_dataframe)
                indexes.append(index)
                hashes.append(self.index_to_hash(int(index)))
            
        cont_dataframe = pd.DataFrame()
        cont_dataframe["continuum"] = cont_df
        cont_dataframe["index"] = indexes
        cont_dataframe["id"] = hashes

        cont_dataframe.to_pickle(save_path)
        del cont_dataframe, cont_df, indexes, hashes
