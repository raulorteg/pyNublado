# Testing Cloudy and pyNublado


### Cloudy installation test run 

In order to test that your Cloudy installation works as expected, put in the path to your Cloudy executable and run it:

```bash 
  ~/c17.03/source/cloudy.exe
```

* Type "test" then press ```Enter``` **twice**
* Cloudy should print some output, which ends with "Cloudy exited OK"

### Running Cloudy manually on a model 

To test if a given .in file is compatible with Cloudy, you may want to run Cloudy independently:

1. Create a _[name].in_ file
2. Navigate to the folder where the .in file is located
3. Execute Cloudy from _that_ directory 
   
```bash
~/c17.03/source/cloudy.exe [name].in
```

### Testing

pyNublado comes with a number of tests for the pytest framework. They can be found in the ```tests/``` directory. To run the tests with pytest:

1. Install pytest, e.g. via ```pip install pytest``` or ```conda install pytest```
2. Navigate to the tests subdirectory ```cd tests```
3. Run tests ```pytest test.py -v```, the `-v` (or `-vv`) flag is optional for increased verbosity

The tests do the following:

* check if the Cloudy path in ```src/usr_settings.py``` is the correct path of the Cloudy installation by running a test model.in
* check if the output of CLOUDY is ok ("Cloudy exited OK")
* it creates the file structure src.manager.QueueManager() expects and runs 4 models on multiple cpus to test the pipeline.
* check if the stellar atmosphere model specified in `src/user_settings.py` is installed (see BPASS installation)