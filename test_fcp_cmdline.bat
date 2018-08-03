@echo off
echo # ------------------------------------------------------------------------
echo # TEST 1
echo # input_fc valid, out_folder valid, expecting Exit code 0
echo # ------------------------------------------------------------------------
SET input_fc="c:\tmp\fc_profiler_testdata\fc_profiler_test.gdb\WGS84_point"
SET out_folder="c:\tmp"
C:\Python27\ArcGIS10.6\python.exe C:\Users\micza\OneDrive\code\py_arcpy\fc_profiler\fc_profiler.py
if %ERRORLEVEL% == 0 (
    echo.
    echo PASS
) else if %ERRORLEVEL% == 1 (
    echo.
    echo FAIL
) else (
   echo.
   echo ErrorLevel is > 1
   echo A second statement
)
echo.

echo # ------------------------------------------------------------------------
echo # TEST 2
echo # input_fc invalid, out_folder valid, expecting Exit Code 1
echo # ------------------------------------------------------------------------
echo STUB
echo.

echo # ------------------------------------------------------------------------
echo # TEST 3
echo # input_fc valid, out_folder invalid, expecting Exit Code 1
echo # ------------------------------------------------------------------------
echo STUB
echo.

echo # ------------------------------------------------------------------------
echo # TEST 4
echo # input_fc invalid, out_folder invalid, expecting Exit Code 1
echo # ------------------------------------------------------------------------
echo STUB
echo.

pause