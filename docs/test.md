### Testing
Tests can be found in ```tests/```. To run the tests with pytest:
1. Install pytest ```pip install pytest```
2. Navigate to tests ```cd tests```
3. Run tests ```pytest -v test.py```, the -v flag is optional for verbosity

The tests check if cloudy path in ```src/common/settings.py``` is the correct path of the cloudy installation in our system by runnning a test model.in, then checks if the output of CLOUDY is ok ("Cloudy exited OK"), then creates the file structure src.manager.QueueManager() expects and runs 4 models on multiple cpus to check the pipeline.