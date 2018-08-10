#!./venv_p27arcpy/Scripts/python.exe
__author__ = "Mic Zatorsky"
__copyright__ = "Copyright 2018, Michael Zatorsky "
__license__ = "CC BT-SA 4.0"
__version__ = "1.2.1"
__date__ = "11/08/2018"

# ----------------------------------------------------------------------------
# documentation:  https://github.com/miczat/fc_profiler
# ----------------------------------------------------------------------------

import logging
import os
import sys
import argparse
import datetime
from generate_profile import generate_profile

start_time = datetime.datetime.now()
log = logging.getLogger()

# --------------------------------------------
# run config (globals) - not user configurable
# --------------------------------------------
program_name = r"fc_profile"
logfile_ext = ".log.csv"  # easier viewing in excel
overwrite = True  # overwrite the existing output files


# -----------------------------------------
# create and configure the logger
# -----------------------------------------


def setup_logger(logfile):
    """
    :param logfile: full path to where the log will be stored
    :type logfile: basestring
    """

    # log.setLevel(logging.INFO)
    log.setLevel(logging.DEBUG)

    # formatter for use by all handlers
    d = ","   # log column delimiter
    log_msg_format_str = '%(asctime)s' + d + '%(levelname)s' + d + '"%(message)s"'
    datetime_fmt_str  = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(log_msg_format_str,datetime_fmt_str)

    # file handler
    try:
        fh = logging.FileHandler(filename=logfile,mode='w')
    except IOError as e:
        print("The log file is read only. Program stopping")
        raise
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    log.addHandler(fh)

    # console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    log.addHandler(ch)


# -----------------------------------------
# get args
#    positional arguments (no flags)
# -----------------------------------------


def parse_arguments():
    """
    :return: (fc_path, output folder)
    :rtype tuple
    """
    parser = argparse.ArgumentParser(description="fc_profiler")
    parser.add_argument("fc_path", help="full path to the feature class")
    parser.add_argument("out_folder", help="the output folder")
    args = parser.parse_args()
    return args.fc_path, args.out_folder


# ------------------------------------------------------------
# validate inputs
#     pre: the input feature class exists
#     pre: the output xls is somewhere that can be writen too
#     post: retuen True, or exits the program

# -----------------------------------------------------------


def validate_inputs(fc_path, out_folder):
    """
    :param fc_path: - fully qualified path to the input feature class to profile
    :type fc_path: basestring

    :param out_folder: - fully qualified path to the output folder to write to
    :type fc_path: basestring
    """

    # check that the input GDB exists
    fc_gdb_path = fc_path.split(".gdb", 1)[0] + ".gdb"
    log.debug("Checking input feature class exists")
    if not os.path.isdir(fc_gdb_path):
        log.warning("Input file GDB does not exist. Stopping.")
        sys.exit(1)

    # check that the output folder exists and can be written to.
    # Better to know now than after minutes of profiling
    log.debug("Checking output folder exists and can be written to")
    if not os.access(out_folder, os.W_OK):
        log.warning("No write access to the output folder. Stopping.")
        sys.exit(1)


# -----------------------------------------
# main
# -----------------------------------------


def main(fc_path, out_folder):
    """main
    :param fc_path: - fully qualified path to the input feature class to profile
    :type fc_path: basestring

    :param out_folder: - fully qualified path to the output folder to write to
    :type fc_path: basestring
    """

    log.info("fc_profiler Start")

    log.info("Validating inputs")
    validate_inputs(fc_path, out_folder)

    log.info("Generating profile")
    generate_profile(fc_path, out_folder, overwrite)

    log.info("fc_profiler Finished")
    end_time = datetime.datetime.now()
    duration = end_time - start_time
    log.info("fc_profiler Duration " + str(duration))


if __name__ == "__main__":
    args = parse_arguments()
    fc_path = args[0]
    out_folder = args[1]
    logfile = os.path.join(out_folder, program_name + logfile_ext)
    setup_logger(logfile)
    log.debug("arg fc_path = " + fc_path)
    log.debug("arg out_folder = " + out_folder)

    # magic happens
    main(fc_path, out_folder)

    log.debug("Closing the log file")
    log = logging.getLogger()
    log_handlers_list = list(log.handlers)
    for h in log_handlers_list:
        log.removeHandler(h)
        h.flush()
        h.close()
