# fc_profiler

A tool that helps understand data in an undocumented world.

Given an Esri ArcGIS feature class, **fc_profiler** will execute a suite of data profiling functions, outputting the results to an XLS file.

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
* **Python 2.7** (and later 3)
* ```arcpy```
* ```unittest```
* ```logging```, ```xlwt```, ```argparse```, and ```sqlite```
* Source code management, ```Git``` and **GitHub**, including GitHub **Projects** 
* Writing READMEs and **markdown**
* The **PyCharm IDE**


## Git/GitHub workflow
* _master_ is release-ready code
* development on branches

## Testing
* This is a database app and tests are run against a set of pre-made file GDBs
* The test databases are scripted via unittests

## Licence
The content of this repository is licensed under a Creative Commons Attribution-ShareAlike 4.0 International (CC BT-SA 4.0)


### About the author
**fc_profiler** is being developed by Mic Zatorsky

