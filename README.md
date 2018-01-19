# SPSS-BatchProcessor
The _SPSS BatchProcessor_ is a tool for automation developed and used within the working group "Psychologische Diagnostik. Differentielle Psychologie und Persönlichkeitspsychologie" of the University of Kiel. 

The tool automates the execution of SPSS scripts on arbitrarily large sets of input files. In particular, it enables to process a number of (subject) files without executing each one manually - and also without creating a corresponding syntax file for each and every subject. The tool supports both SPSS and PSPP. 

## Features
* Applying a given SPSS file on a given set of (subject) files
* Storage of all options in configuration files
* Extracting information from filenames and providing it in syntax files (i.e. subject shorthands, conditions ...)
* Mass generation of syntax files
* Simulation of execution 
* Capture and storage of SPSS output
* Accumulation of data files (grouping of subjects)

## Requirements
The BatchProcessor is a collection of Python scripts. As such, it can be run with any distribution of SPSS 24/PSPP. There are no requirements beyond those already imposed by SPSS/PSPP. 

## License
The project is licensed under GPLv3. 
