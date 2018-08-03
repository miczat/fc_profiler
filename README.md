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


Edit the **#run config** section of the code in ```fc_profile.py``` and run.

_soon…_


```
C:\>python fc_profiler -f c:\tmp\data.gdb\roads -o c:\temp
```
_where_

&nbsp;&nbsp;&nbsp;&nbsp;```-f``` input feature class\
&nbsp;&nbsp;&nbsp;&nbsp;```-o``` output folder for the report
 
_later..._

I'll create a python toolbox for ArcMap

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


## Git/GitHub workflow
* ```master``` is release-ready code
* development on branches

## Testing
* This is a database app and tests are run against a set of pre-made file GDBs
* The test databases are scripted via unittests

## Licence
The content of this repository is licensed under a _Creative Commons Attribution-ShareAlike 4.0 International_ [(CC BT-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/)

![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)

### About the author
**fc_profiler** is being developed by [Mic Zatorsky](https://www.linkedin.com/in/michaelzatorsky)

