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
#     Designed to work with Point, Polyline, Polygon, Multipoint and
#     Multipatch feature classes.
#
#     No current support for:
#      - shapefiles  (pull into a fGDB first)
#      - annotation FC
#
# Ref:
#     url
#
# ----------------------------------------------------------------------------

#import arcpy
import logging
import os
import sys
import datetime
import xlwt

import fc_properties
import xls_output

start_time = datetime.datetime.now()
log = logging.getLogger()

# -----------------------------------------
# run config (globals)
# -----------------------------------------
program_name = r"fc_profile"
log_folder = r"."
overwrite = True  # overwrite the existing output files. not configurable by user


# if no args are specifed, use thees

# fc_path = r"c:\tmp\fc_profiler_testdata\fc_profiler_test.gdb\MGAZ56_point"
# fc_path = r"c:\tmp\fc_profiler_testdata\fc_profiler_test.gdb\GDA94_GA_Lambert_point"
fc_path = r"c:\tmp\fc_profiler_testdata\fc_profiler_test.gdb\WGS84_point"
# fc_path = r"c:\tmp\fc_profiler_testdata\fc_profiler_test.gdb\NO_CRS_point"
# fc_path = r"c:\tmp\fc_profiler_testdata\foo.gdb\bah"

xls_folder = r"C:\tmp\fc_profiler_testdata"


# -----------------------------------------
# create and configure the logger
# -----------------------------------------
def setup_logger():
    logfile_ext = ".log.csv"
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
# validate inputs
# -----------------------------------------

def validate_inputs(fc_path, xls_path):
    """
    :param fc_path: - fully qualified path to the input feature class to profile
    :param xls_path: - fully qualified path to the output xls to write
    pre: the input feature class exists
    pre: the output xls is somewhere that can be writen too
    post: retuen True, or raise an exception
    :return: True, if no exceptions are thrown
    """

    # check that the input GDB exists
    fc_gdb_path = fc_properties.get_fc_gdb_path(fc_path)
    if not os.path.isdir(fc_gdb_path):
        log.warning("Input feature class fGDB does not exist. Stopping.")
        sys.exit(1)

    # check that the output XLS folder can be written to.
    # Better to know now than after 10 minutes of profiling
    if not os.access(xls_folder, os.W_OK):
        log.warning("No write access to the output folder. Stopping.")
        sys.exit(1)

    # if the output file exists
    if os.path.exists(xls_path) and overwrite is True:
        try:
            log.info("Removing XLS " + xls_path)
            os.remove(xls_path)
        except WindowsError as e:
            log.error("WindowsError: could not delete file")
            log.error(str(e).replace("\n", "; "))
            raise
        except Exception as e:
            log.error("Some other error")
            log.error(str(e).replace("\n", "; "))
            raise

    return True

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


def main():
    """main"""
    log.info("fc_profiler Start")

    log.info("Validating inputs")
    xls_path = os.path.join(xls_folder, fc_properties.get_fc_name(fc_path) + ".xls")
    validate_inputs(fc_path, xls_path)

    log.info("Staring profile...")
    profile(fc_path, xls_path)

    # when done
    log.info("fc_profiler Finished")
    end_time = datetime.datetime.now()
    duration = end_time - start_time
    log.info("fc_profiler Duration " + str(duration))


if __name__ == "__main__":
    setup_logger()
    main()