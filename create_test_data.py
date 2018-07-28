# ----------------------------------------------------------------------------
# name:        create_test_data.py
#
# description: Creates a suite of file geodatabases for use with unit
#              testing
#
#             See fc_profiler_tests.xlsx for data requirements
#
#
# version      1.0
# author       Mic Zatorsky
# created      28/07/2018
#
# param:       none
#
# pre:         install_folder exists and is writable
#
# return:      none
#
# post:        a set of file geodatabases are creates
#
# Run instructions:
#     -
#     -
#     -
#
# Issues and known limitations:
#     -
#     -
#
# Ref:
#     url
#      
# ----------------------------------------------------------------------------

import arcpy
from arcpy import env
import logging
import os
import shutil
import datetime

start_time = datetime.datetime.now()
log = logging.getLogger()

# -----------------------------------------
# run config (globals)
# -----------------------------------------
program_name = r"create_test_data"
log_folder = r"."
install_folder = r"c:\tmp\fc_profiler_testdata"
overwrite = True  # overwrite the existing test DB if it exists?


# -----------------------------------------
# create and configure the logger
# -----------------------------------------
def setup_logger():
    logfile_ext = ".log.csv"
    logfile = os.path.join(log_folder, program_name + logfile_ext)
    log.setLevel(logging.DEBUG)

    # formatter for use by all handlers
    d = ","   # log column delimiter
    log_msg_format_str = '%(asctime)s' + d + '%(levelname)s' + d + '"%(message)s"'
    datetime_fmt_str  = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(log_msg_format_str,datetime_fmt_str)

    # create file handler which logs even debug messages
    try:
        fh = logging.FileHandler(filename=logfile,mode='w')
    except IOError as e:
        print("The log file is read only. Program stopping")
        raise

    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    log.addHandler(fh)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    log.addHandler(ch)

# -----------------------------------------
# create file geodatabase(s)
# -----------------------------------------


def create_fgdb_test():
    """create an empty file geodatabase"""
    fgdb_name = "fc_profiler_test.gdb"
    fgdb_path = os.path.join(install_folder,fgdb_name)

    if os.path.exists(fgdb_path) and overwrite is True:
        try:
            shutil.rmtree(fgdb_path)
        except WindowsError as e:
            log.error("WindowsError: could not delete folder")
            log.error(str(e).replace("\n", "; "))
            raise

    try:
        arcpy.CreateFileGDB_management (out_folder_path=install_folder,
                                        out_name=fgdb_name,
                                        out_version="CURRENT")
    except arcpy.ExecuteError as e:
        log.error("ExecuteError - folder exists")
        log.error(str(e).replace("\n", "; "))
        raise


# -----------------------------------------
# main
# -----------------------------------------

def main():
    """main"""

    log.info('Start')
    end_time = datetime.datetime.now()
    duration = end_time - start_time

    create_fgdb_test()
    #create_fc_GDA_LL_point()

    log.info('Finished')
    log.info("Duration " + str(duration))


if __name__ == "__main__":
    setup_logger()
    main()


