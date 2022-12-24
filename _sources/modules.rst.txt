Modules
====================

CLOUDY sampling
++++++++++++++++
The sampling module samples the CLOUDY input parameter space using LHS
in order to produce combinations of inputs that map out the whole space
efficiently.

.. automodule:: sampling
   :members:

CLOUDY inputs
++++++++++++++++
The following class takes the sampled CLOUDY input parameter
combinations and for every combination creates the model.in file that CLOUDY
expects.

.. automodule:: cloudy_input
   :members:

Running CLOUDY
++++++++++++++++
Using the generated inputs (model.in files) this module can be used to set up a queue
of inputs to be run in CLOUDY using multiple workers. The result of which are stored in a 
"done/" directory.

.. automodule:: manager
   :members:

Parsing CLOUDY
++++++++++++++++
After running the models, given the directory where the outputs are stored we can then use the parser
module to look for all outputs within the directory "done/" and parse some of the results for further
processing.

.. automodule:: parser
   :members:




