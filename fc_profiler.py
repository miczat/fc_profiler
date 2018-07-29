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

start_time = datetime.datetime.now()
log = logging.getLogger()

# -----------------------------------------
# run config (globals)
# -----------------------------------------
program_name = r"fc_profile"
log_folder = r"."
# fc_path = r"c:\tmp\fc_profiler_testdata\fc_profiler_test.gdb\MGAZ56_point"
# fc_path = r"c:\tmp\fc_profiler_testdata\fc_profiler_test.gdb\GDA94_GA_Lambert_point"
fc_path = r"c:\tmp\fc_profiler_testdata\fc_profiler_test.gdb\WGS84_point"
# fc_path = r"c:\tmp\fc_profiler_testdata\fc_profiler_test.gdb\NO_CRS_point"
# fc_path = r"c:\tmp\fc_profiler_testdata\foo.gdb\bah"
overwrite = True  # overwrite the existing output files?
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
# Write to excel
# -----------------------------------------

def write_fc_properties_to_xls(fc_properties_list,xls_path):
    """"writes the simple feature class properties to a page in an XLS"""
    book = xlwt.Workbook()
    sheet1 = book.add_sheet("fc_properties")
    book.save(xls_path)


# -----------------------------------------
# main
# -----------------------------------------

def main():
    """main"""
    log.info("Start")

    # check that the input GDB exists
    fc_gdb_path = fc_properties.get_fc_gdb_path(fc_path)
    if not os.path.isdir(fc_gdb_path):
        log.warning("Input feature class fGDB does not exist. Stopping.")
        sys.exit(1)

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
    xls_path = os.path.join(xls_folder, fc_properties.get_fc_name(fc_path) + ".xls")
    log.debug("xls_path = " + xls_path)
    write_fc_properties_to_xls(fc_properties_list, xls_path)

    log.info("Finished")
    end_time = datetime.datetime.now()
    duration = end_time - start_time
    log.info("Duration " + str(duration))


if __name__ == "__main__":
    setup_logger()
    main()