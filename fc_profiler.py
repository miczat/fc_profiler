# ----------------------------------------------------------------------------
# name:        fc_profiler.py
#
# description: Creates a profile of a feature class in an XLS file
#
# version      1.0
# author       Mic Zatorsky
# created      04/08/2018
#
# documentation:  https://github.com/miczat/fc_profiler
#
# ----------------------------------------------------------------------------

import logging
import os
import sys
import argparse
import datetime
import fc_properties
import xls_output

start_time = datetime.datetime.now()
log = logging.getLogger()

# --------------------------------------------
# run config (globals) - not user configurable
# --------------------------------------------
program_name = r"fc_profile"
log_folder = r"."
overwrite = True  # overwrite the existing output files
logfile_ext = ".log.csv"  # easier viewing in excel
report_ext = "_fc_profile.xls"


# -----------------------------------------
# create and configure the logger
# -----------------------------------------
def setup_logger():
    """setp the logger"""
    logfile = os.path.join(log_folder, program_name + logfile_ext)
    # log.setLevel(logging.INFO)
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
# get args
# -----------------------------------------


def parse_arguments():
    """
    gets command line arguments
    positional arguments (no flags)
    :return: a tuple as (fc_path, out_folder)
    """
    parser = argparse.ArgumentParser(description="fc_profiler")
    parser.add_argument("fc_path", help="full path to the feature class")
    parser.add_argument("out_folder", help="the output folder")
    args = parser.parse_args()
    return args.fc_path, args.out_folder


# -----------------------------------------
# validate inputs
# -----------------------------------------


def validate_inputs(fc_path, out_folder):
    """
    :param fc_path: - fully qualified path to the input feature class to profile
    :param out_folder: - fully qualified path to the output xls to write
    pre: the input feature class exists
    pre: the output xls is somewhere that can be writen too
    post: retuen True, or raise an exception
    """

    # check that the input GDB exists
    fc_gdb_path = fc_properties.get_fc_gdb_path(fc_path)
    log.debug("Checking input feature class exists")
    if not os.path.isdir(fc_gdb_path):
        log.warning("Input feature class fGDB does not exist. Stopping.")
        sys.exit(1)

    # check that the output folder exists and cab be written to.
    # Better to know now than after 10 minutes of profiling
    log.debug("Checking output folder exists and can be written to")
    if not os.access(out_folder, os.W_OK):
        log.warning("No write access to the output folder. Stopping.")
        sys.exit(1)

# -----------------------------------------
# delete existing xls
# -----------------------------------------


def delete_existing_xls(xls_path):
    """
    :param xls_path: - the name of the xls file to delete
    :return: none
    """
    if os.path.exists(xls_path):
        try:
            log.debug("Removing XLS " + xls_path)
            os.remove(xls_path)
        except WindowsError as e:
            log.error("WindowsError: could not delete file")
            log.error(str(e).replace("\n", "; "))
            raise
        except Exception as e:
            log.error("Some other error")
            log.error(str(e).replace("\n", "; "))
            raise


# -----------------------------------------
# profile
# -----------------------------------------


def profile(fc_path, xls_path):
    """
    this is the main function that controls the profile generation

    :param fc_path: - fully qualified path to the input feature class to profile
    :param xls_path: - fully qualified path to the output xls to write
    pre: the input feature class exists
    pre: the output xls is somewhere that can be writen too
    post: a xls file will be written
    :return: None
    """

    # generate the list of feature class properties
    fc_properties_list = [("Feature Class", fc_properties.get_fc_name(fc_path)),
                          ("Parent fGDB", fc_properties.get_fc_gdb_path(fc_path)),
                          ("Geometry Type", fc_properties.get_fc_geometry_type(fc_path)),
                          ("CRS Name", fc_properties.get_crs_name(fc_path)),
                          ("CRS EPSG WKID", fc_properties.get_crs_wkid(fc_path)),
                          ("CRS Type", fc_properties.get_crs_type(fc_path)),
                          ("CRS Units", fc_properties.get_crs_units(fc_path))]

    if logging.getLevelName(log.getEffectiveLevel()) == "INFO":
        log.info("FC Properties List:")
        for item in fc_properties_list:
            log.info("{:18}: {}".format(item[0],item[1]))

    # write the list of feature class properties to Excel
    log.debug("xls_path = " + xls_path)
    xls_output.write_fc_properties(fc_properties_list, xls_path)


# -----------------------------------------
# main
# -----------------------------------------


def main(fc_path, out_folder):
    """main
    :param args: -the arguments passed into the program
    """

    log.info("fc_profiler Start")


    log.info("Validating inputs")
    validate_inputs(fc_path, out_folder)

    xls_path = os.path.join(out_folder, fc_properties.get_fc_name(fc_path) + report_ext)
    if overwrite is True:
        log.info("Deleting existing xls file")
        delete_existing_xls(xls_path)

    log.info("Starting profile...")
    profile(fc_path, xls_path)

    # when done
    log.info("fc_profiler Finished")
    end_time = datetime.datetime.now()
    duration = end_time - start_time
    log.info("fc_profiler Duration " + str(duration))


if __name__ == "__main__":
    setup_logger()
    args = parse_arguments()
    fc_path = args[0]
    out_folder = args[1]
    log.debug("arg fc_path = " + fc_path)
    log.debug("arg out_folder = " + out_folder)
    main(fc_path,out_folder)
