# fc_profiler

A tool that helps understand data in an undocumented world.

Given an Esri ArcGIS feature class, **fc_profiler** will execute a suite of data profiling functions, outputting the results to an XLS file.

Information listed:
* feature class name
* parent GDB
* coordinate system name
* coordinate system EPSG/WKID
* coordinate system type
* coordinate system units

&nbsp;

Planned for development
* how many records
* does the data have M-values?
* does the data have Z-values?
* how many fields?
* max field length > 10? (_thinking about shapefile export issues here_)

&nbsp;&nbsp;&nbsp;&nbsp;_table structure_
* field name
* field alias
* field type
* field length
* field precision (for float & double)
* field scale (for float & double)
* is a domain defined?
* count where the field value IS NULL
* percent where the field value IS NULL
* count where the field value.strip() == ""
* percent where the field value.strip() == ""
* count 'no data' records (NULL plus "")  
* percent 'no data' records (NULL plus "")
* does it contain unicode?
* does it contain reserved characters (for Windows)?


&nbsp;&nbsp;&nbsp;&nbsp;_for each field_

* TOP 100 DISTINCT values ORDERED BY frequency DESC
* TOP 100 DISTINCT values ORDERED BY value ASC
* draw a histogram for numeric data
* draw a pie chart for categorical data 
 



## Installation
Requires the python libraries that ship with Esri ArcGIS 10.3 or greater.


### Requirements
TBA

## Usage

```
python fc_profiler.py <input_fc> <output_folder>
```

_for example_
```
C:\>python fc_profiler.py c:\temp\data.gdb\roads c:\temp
```


 
_later..._

I'll create a python toolbox for ArcMap

### Output

An xls file with the same name as the input feature class and with the suffix and extension ```_fc_profile.xls```


## Known bugs and issues
* This has been developed and tested against ArcGIS versions 10.3 and 10.6
* Right now, it doesn’t do much at all
* It runs all profile tests


## Why?

This is fundamentally an excuse to learn:
* Python 2.7 
* ```arcpy```
* ```unittest```
* ```logging```, ```xlwt```, ```argparse```, and ```sqlite```, or ```pandas```
* Source code management, ```Git``` and **GitHub**, including GitHub **Projects** 
* Writing READMEs and **markdown**
* The **PyCharm IDE**

And because I never get good metadata.

## Architecture

![](https://www.lucidchart.com/publicSegments/view/e96cd7de-7b89-45a2-8bd4-3396e7b224f1/image.png)

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

