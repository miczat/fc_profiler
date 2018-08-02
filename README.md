fc_profiler

This is a tool for understanding data in an undocumented world.

Given an Esri ArcGIS feature class (fc), **fc_profiler** will execute a suite of data profiling activities outputting the results to an XLS file.

Installation
Requires the python libraries that ship with Esri ArcGIS 10.3 or greater.

Usage

_now_

Edit the run config section of the code and run.

_Soon…_

C:\>python fc_profiler --fc c:\tmp\data.gdb\roads –-xlsdir c:\temp

_later__

Create a python tool for ArcMap, using the ArcGIS tool GUI

Known bugs and issues
* This has been developed and tested against ArcGIS versions 10.3 and 10.6
* Right now, it doesn’t do much at all
* It will always run all profile tests


Why?

This is fundamentally an excuse to learn:
* **Python 2.7** (and later 3)
* **arcpy**
* **unittest**
* **xlwt**, **argparse**, and **sqlite**
* Source code management, **Git** and **GitHub**, including GitHub **Projects** 
* The python **logging** library
* Writing READMEs and **markdown**
* The **PyCharm IDE**

Why these versions?
* I work behind a military grade firewall. I’m using what comes with ArcGIS 10.3… yeah, that’s 10.3….

Git/GitHub workflow
* Master is release-ready code
* development on branches

Testing
* This is a database app and tests are run against a set of pre-made fGDBs
* The test databases are scripted via unittests

Licence
The content of this repository is licensed under a Creative Commons Attribution-ShareAlike 4.0 International (CC BT-SA 4.0)


About the author
fc_profiler is being developed by Mic Zatorsky

