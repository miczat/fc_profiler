# fc_profiler

This is a data interrogation tool for use with Esri ArcGIS feature classes.

Given an Esri ArcGIS feature class, **fc_profiler** will execute a suite of data profiling functions, outputting the results to an XLS file.

![](https://www.lucidchart.com/publicSegments/view/de4245bf-2ca4-4512-8165-4edbee306e3b/image.png)

Information listed:
* feature class name
* parent GDB
* coordinate system name
* coordinate system EPSG/WKID
* coordinate system type
* coordinate system units

_Planned for development_

 
* how many records
* does the data have M-values?
* does the data have Z-values?
* how many fields?
* max field length > 10? (_thinking about shapefile export issues here_)
* table structure (field name, alias, type, length, precision, scale)
* is a domain defined?
* count where the field value IS NULL
* percent where the field value IS NULL
* count where the field value.strip() == ""
* percent where the field value.strip() == ""
* count 'no data' records (NULL plus "")  
* percent 'no data' records (NULL plus "")
* does it contain unicode?
* does it contain reserved characters (for Windows)?
* TOP 100 DISTINCT values ORDERED BY frequency DESC
* TOP 100 DISTINCT values ORDERED BY value ASC
* draw a histogram for numeric data
* draw a pie chart for categorical data 
* port to Python 3.6.5 and *ArcGIS Pro*
&nbsp;

## Installation
Requires the python libraries that ship with Esri ArcGIS 10.3 or greater.
&nbsp;

## Usage
```
python fc_profiler.py <input_fc> <output_folder>
```

_for example_
```
C:\>python fc_profiler.py c:\temp\data.gdb\roads c:\temp
```

This can also be run as Python Toolbox tool.

![](https://www.lucidchart.com/publicSegments/view/3c1eea03-7cec-45dc-bed8-49b76b92ac7a/image.png)
&nbsp;

### Output
An Excel spreadsheet (.xls) with the same name as the input feature class and with the suffix and extension ```_fc_profile.xls``` will be created in the specified output folder. 
&nbsp;

## Version differences
_The python toolbox version_
* has a GUI
* filters input for points, polylines and polygons 

## Known bugs, issues & limitations
* This has been developed and tested against ArcGIS versions 10.3 and 10.6
* Right now, it does not do much at all
* It will run all profiles, until designed to do a subset
* It will profile all fields, until designed to do a subset
&nbsp;

## Why?
This is fundamentally an excuse to learn:
* Python 2.7 
* ```arcpy``` and * Python Toolboxes (```.pyt```)
* ```unittest```
* ```argparse```, ```logging```, ```xlwt```,
* maybe ```sqlite```, or ```pandas```
* Source code management, ```Git``` and **GitHub**, including **GitHub Projects** 
* Writing READMEs and **markdown**
* The **PyCharm IDE**

...and because I never get good metadata.
&nbsp;

## Architecture
* The program can be called from either the command line, or via a Script Tool using ```fc_profiler.py```; or the python toolbox  ```fc_profiler.pyt```

* The UI is separate from the business logic in ```generate_profile.py``` and its supporting modules. 

* All modules share a common logger defined in the UI scripts.

* It is expected that ```fc_properties.py``` will grow and another module ```field_properties.py ``` will contain code for profiling a single column.

![](https://www.lucidchart.com/publicSegments/view/552e52aa-4b6d-4200-9a65-e5b96fc0b415/image.png)


## Git/GitHub workflow
* ```master``` is release-ready code
* development on branches

## Testing
* This is a database app.  Unit and integration tests are run against a set of scripted test GDBs
* The test GDBs and their Feature Classes can be deployed using ```create_test_data.py```   
* Edit the ```#run config``` section to specify the test DB installation folder  before running
* The test scripts are in ```tests```
* Edit the ```#run config``` section in each script specify the test DB installation folder
* ```tests\test_fcp_cmdline.bat``` executes a suite of tests checking program exit codes when called form the command line 

## Licence
The content of this repository is licensed under a _Creative Commons Attribution-ShareAlike 4.0 International_ [(CC BT-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/)

![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)


### About the author
**fc_profiler** is being developed by [Mic Zatorsky](https://www.linkedin.com/in/michaelzatorsky)

