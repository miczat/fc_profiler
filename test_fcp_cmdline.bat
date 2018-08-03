@echo off

echo # ------------------------------------------------------------------------
echo # TEST 1
echo # input_fc valid, out_folder valid, expecting Exit code 0
echo # ------------------------------------------------------------------------
set input_fc="c:\tmp\fc_profiler_testdata\fc_profiler_test.gdb\WGS84_point"
set out_folder="C:\tmp\fc_profiler_testdata"

@echo on
C:\Python27\ArcGIS10.6\python.exe C:\Users\micza\OneDrive\code\py_arcpy\fc_profiler\fc_profiler.py %input_fc% %out_folder%
@echo off

if %ERRORLEVEL% == 0 (
    echo PASS, got exit code 0
) else if %ERRORLEVEL% == 1 (
    echo FAIL, got exit code 1
) else (
   echo FAIL, got exit code %ERRORLEVEL%
 )
echo.


echo # ------------------------------------------------------------------------
echo # TEST 2
echo # input_fc invalid, out_folder valid, expecting Exit Code 1
echo # ------------------------------------------------------------------------
SET input_fc=c:\foo.gdb\bar
SET out_folder=c:\tmp

@echo on
C:\Python27\ArcGIS10.6\python.exe C:\Users\micza\OneDrive\code\py_arcpy\fc_profiler\fc_profiler.py %input_fc% %out_folder%
@echo off

if %ERRORLEVEL% == 0 (
    echo FAIL, got exit code 0
) else if %ERRORLEVEL% == 1 (
    echo PASS, got exit code 1
) else (
   echo PASS, got exit code %ERRORLEVEL%
echo.


echo # ------------------------------------------------------------------------
echo # TEST 3
echo # input_fc valid, out_folder invalid, expecting Exit Code 1
echo # ------------------------------------------------------------------------
SET input_fc=c:\tmp\fc_profiler_testdata\fc_profiler_test.gdb\WGS84_point
SET out_folder=c:\foo\bar

@echo on
C:\Python27\ArcGIS10.6\python.exe C:\Users\micza\OneDrive\code\py_arcpy\fc_profiler\fc_profiler.py %input_fc% %out_folder%
@echo off


if %ERRORLEVEL% == 0 (
    echo FAIL, got exit code 0
) else if %ERRORLEVEL% == 1 (
    echo PASS, got exit code 1
) else (
   echo PASS, got exit code %ERRORLEVEL%
echo.


echo # ------------------------------------------------------------------------
echo # TEST 4
echo # input_fc invalid, out_folder invalid, expecting Exit Code 1
echo # ------------------------------------------------------------------------
SET input_fc=c:\foo.gdb\bar
SET out_folder=c:\foo\bar

@echo on
C:\Python27\ArcGIS10.6\python.exe C:\Users\micza\OneDrive\code\py_arcpy\fc_profiler\fc_profiler.py %input_fc% %out_folder%
@echo off

if %ERRORLEVEL% == 0 (
    echo FAIL, got exit code 0
) else if %ERRORLEVEL% == 1 (
    echo PASS, got exit code 1
) else (
   echo PASS, got exit code %ERRORLEVEL%
echo.


echo # ------------------------------------------------------------------------
echo # TEST 4
echo # no input fc arg, valid out_folder, expecting Exit Code ???
echo # ------------------------------------------------------------------------
SET input_fc=
SET out_folder=c:\tmp

@echo on
C:\Python27\ArcGIS10.6\python.exe C:\Users\micza\OneDrive\code\py_arcpy\fc_profiler\fc_profiler.py %input_fc% %out_folder%
@echo off

if %ERRORLEVEL% == 0 (
    echo got 0
) else if %ERRORLEVEL% == 1 (
    echo got 1
) else (
   echo ErrorLevel is > 1
echo.


echo # ------------------------------------------------------------------------
echo # TEST 5
echo # valid input fc arg, no out_folde arg, expecting Exit Code ???
echo # ------------------------------------------------------------------------
SET input_fc=c:\tmp\fc_profiler_testdata\fc_profiler_test.gdb\WGS84_point
SET out_folder=

@echo on
C:\Python27\ArcGIS10.6\python.exe C:\Users\micza\OneDrive\code\py_arcpy\fc_profiler\fc_profiler.py %input_fc% %out_folder%
@echo off

if %ERRORLEVEL% == 0 (
    echo got 0
) else if %ERRORLEVEL% == 1 (
    echo got 1
) else (
   echo ErrorLevel is > 1
echo.


echo # ------------------------------------------------------------------------
echo # TEST 6
echo # no args, expecting Exit Code ???
echo # ------------------------------------------------------------------------

@echo on
C:\Python27\ArcGIS10.6\python.exe C:\Users\micza\OneDrive\code\py_arcpy\fc_profiler\fc_profiler.py
@echo off

if %ERRORLEVEL% == 0 (
    echo got 0
) else if %ERRORLEVEL% == 1 (
    echo got 1
) else (
   echo ErrorLevel is > 1
echo.

echo # ------------------------------------------------------------------------
echo # TEST 7
echo # no args, get command line help, expecting Exit Code 0
echo # ------------------------------------------------------------------------

@echo on
C:\Python27\ArcGIS10.6\python.exe C:\Users\micza\OneDrive\code\py_arcpy\fc_profiler\fc_profiler.py --help
@echo off

if %ERRORLEVEL% == 0 (
    echo PASS
) else if %ERRORLEVEL% == 1 (
    echo FAIL
) else (
   echo ErrorLevel is > 1
)
echo.

:end
pause