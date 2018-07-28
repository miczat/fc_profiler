# ----------------------------------------------------------------------------
# name:        fc_profiler.py
#
# description: Creates a profile of a feature class in an XLS file
#
#              coordinate reference system
#
#
# version      1.0
# author       Mic Zatorsky
# created      28/07/2018
#
# param:       none
#
# pre:         input feature class exists and is writable
#
# return:      none
#
# post:        none
#
# Run instructions:
#     configure run config (globals)
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
import datetime

start_time = datetime.datetime.now()
log = logging.getLogger()

# -----------------------------------------
# run config (globals)
# -----------------------------------------
program_name = r"fc_profile"
log_folder = r"."
input_fc = r"c:\tmp\fc_profiler_testdata\fc_profiler_test.gdb\MGAZ56_point"
overwrite = True  # overwrite the existing output files?


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
# main
# -----------------------------------------

def main():
    """main"""
    log.info("Start")


    log.info("Finished")
    end_time = datetime.datetime.now()
    duration = end_time - start_time
    log.info("Duration " + str(duration))


if __name__ == "__main__":
    setup_logger()
    main()