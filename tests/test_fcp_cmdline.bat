@echo off
cls

set python_exe=C:\Users\micza\OneDrive\code\py\fc_profiler\venv_p27arcpy\Scripts\python.exe
set fc_profiler_py=C:\Users\micza\OneDrive\code\py\fc_profiler\fc_profiler.py


echo # ------------------------------------------------------------------------
echo # input_fc valid, out_folder valid, zero records,  expecting Exit Code 0
echo # ------------------------------------------------------------------------
set input_fc="c:\tmp\fc_profiler_testdata\fc_profiler_test.gdb\WGS84_point"
set out_folder="C:\tmp\fc_profiler_testdata"

@echo on
%python_exe% %fc_profiler_py% %input_fc% %out_folder%
@echo off
echo ERRORLEVEL %ERRORLEVEL%
if %ERRORLEVEL% == 0 (
    echo PASS
) else if %ERRORLEVEL% == 1 (
    echo FAIL
) else (
    echo FAIL
)
echo.


echo # ------------------------------------------------------------------------
echo # input_fc valid, out_folder valid, 602 records,  expecting Exit Code 0
echo # ------------------------------------------------------------------------
set input_fc="c:\tmp\fc_profiler_testdata\fc_profiler_test.gdb\MGAZ56_602_rec_polyline"
set out_folder="C:\tmp\fc_profiler_testdata"

@echo on
%python_exe% %fc_profiler_py% %input_fc% %out_folder%
@echo off
echo ERRORLEVEL %ERRORLEVEL%
if %ERRORLEVEL% == 0 (
    echo PASS
) else if %ERRORLEVEL% == 1 (
    echo FAIL
) else (
    echo FAIL
)
echo.


echo # ------------------------------------------------------------------------
echo # input_fc valid, out_folder valid, 0 records, no CRS  expecting Exit Code 0
echo # ------------------------------------------------------------------------
set input_fc="c:\tmp\fc_profiler_testdata\fc_profiler_test.gdb\NO_CRS_point"
set out_folder="C:\tmp\fc_profiler_testdata"

@echo on
%python_exe% %fc_profiler_py% %input_fc% %out_folder%
@echo off
echo ERRORLEVEL %ERRORLEVEL%
if %ERRORLEVEL% == 0 (
    echo PASS
) else if %ERRORLEVEL% == 1 (
    echo FAIL
) else (
    echo FAIL
)
echo.


echo # ------------------------------------------------------------------------
echo # input_fc valid, out_folder valid, 5M records,  expecting Exit Code 0
echo # ------------------------------------------------------------------------
set input_fc="c:\tmp\fc_profiler_testdata\fc_profiler_test.gdb\MGAZ56_5_million_rec_point"
set out_folder="C:\tmp\fc_profiler_testdata"

@echo on
%python_exe% %fc_profiler_py% %input_fc% %out_folder%
@echo off
echo ERRORLEVEL %ERRORLEVEL%
if %ERRORLEVEL% == 0 (
    echo PASS
) else if %ERRORLEVEL% == 1 (
    echo FAIL
) else (
    echo FAIL
)
echo.



echo # ------------------------------------------------------------------------
echo # input_fc valid, out_folder valid, Z and M valuess, expecting Exit Code 0
echo # ------------------------------------------------------------------------
set input_fc="c:\tmp\fc_profiler_testdata\fc_profiler_test.gdb\MGAZ56_has_Z_M_polyline"
set out_folder="C:\tmp\fc_profiler_testdata"

@echo on
%python_exe% %fc_profiler_py% %input_fc% %out_folder%
@echo off
echo ERRORLEVEL %ERRORLEVEL%
if %ERRORLEVEL% == 0 (
    echo PASS
) else if %ERRORLEVEL% == 1 (
    echo FAIL
) else (
    echo FAIL
)
echo.



echo # ------------------------------------------------------------------------
echo # input_fc invalid, out_folder valid, expecting Exit Code non-zero
echo # ------------------------------------------------------------------------
set input_fc=c:\foo.gdb\bar
set out_folder=c:\tmp
@echo on
%python_exe% %fc_profiler_py% %input_fc% %out_folder%
@echo off
echo ERRORLEVEL %ERRORLEVEL%
if %ERRORLEVEL% == 0 (
    echo FAIL
) else if %ERRORLEVEL% == 1 (
    echo PASS
) else (
    echo PASS
)
echo.


echo # ------------------------------------------------------------------------
echo # input_fc valid, out_folder invalid, expecting Exit Code 1
echo # ------------------------------------------------------------------------
SET input_fc=c:\tmp\fc_profiler_testdata\fc_profiler_test.gdb\WGS84_point
SET out_folder=c:\foo\bar
@echo on
%python_exe% %fc_profiler_py% %input_fc% %out_folder%
@echo off
echo ERRORLEVEL %ERRORLEVEL%
if %ERRORLEVEL% == 0 (
    echo FAIL
) else if %ERRORLEVEL% == 1 (
    echo PASS
) else (
    echo PASS
)
echo.


echo # ------------------------------------------------------------------------
echo # input_fc invalid, out_folder invalid, expecting Exit Code 1
echo # ------------------------------------------------------------------------
SET input_fc=c:\foo.gdb\bar
SET out_folder=c:\foo\bar
@echo on
%python_exe% %fc_profiler_py% %input_fc% %out_folder%
@echo off
echo ERRORLEVEL %ERRORLEVEL%
if %ERRORLEVEL% == 0 (
    echo FAIL
) else if %ERRORLEVEL% == 1 (
    echo PASS
) else (
    echo PASS
)
echo.



echo # ------------------------------------------------------------------------
echo # no input fc arg, valid out_folder, expecting Exit Code 1
echo # ------------------------------------------------------------------------
SET input_fc=""
SET out_folder=c:\tmp
@echo on
%python_exe% %fc_profiler_py% %input_fc% %out_folder%
@echo off
echo ERRORLEVEL %ERRORLEVEL%
if %ERRORLEVEL% == 0 (
    echo FAIL
) else if %ERRORLEVEL% == 1 (
    echo PASS
) else (
    echo FAIL
)
echo.


echo # ------------------------------------------------------------------------
echo # valid input fc arg, no out_folder arg, expecting Exit Code 2
echo # ------------------------------------------------------------------------
SET input_fc=c:\tmp\fc_profiler_testdata\fc_profiler_test.gdb\WGS84_point
SET out_folder=
@echo on
%python_exe% %fc_profiler_py% %input_fc% %out_folder%
@echo off
echo ERRORLEVEL %ERRORLEVEL%
if %ERRORLEVEL% == 0 (
    echo FAIL
) else if %ERRORLEVEL% == 1 (
    echo PASS
) else (
    echo PASS
)
echo.




echo # ------------------------------------------------------------------------
echo # no args, expecting Exit Code 2 (too few arguments)
echo # ------------------------------------------------------------------------

@echo on
%python_exe% %fc_profiler_py%
@echo off
echo ERRORLEVEL %ERRORLEVEL%
if %ERRORLEVEL% == 0 (
    echo FAIL
) else if %ERRORLEVEL% == 1 (
    echo FAIL
) else (
    echo PASS
)
echo.




echo # ------------------------------------------------------------------------
echo # no args, get command line help, expecting Exit Code 0
echo # ------------------------------------------------------------------------

@echo on
%python_exe% %fc_profiler_py% --help
@echo off
echo ERRORLEVEL %ERRORLEVEL%
if %ERRORLEVEL% == 0 (
    echo PASS
) else if %ERRORLEVEL% == 1 (
    echo FAIL
) else (
    echo FAIL
)
echo.


:end
pause