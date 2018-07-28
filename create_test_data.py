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
    log_msg_format_str = '%(asctime)s' + d + '%(levelname)s' + d +\
                         '"%(message)s"'
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
# create test file geodatabase
# -----------------------------------------


def create_fgdb_test():
    """create an empty file geodatabase"""
    fgdb_name = "fc_profiler_test.gdb"
    fgdb_path = os.path.join(install_folder,fgdb_name)

    if os.path.exists(fgdb_path) and overwrite is True:
        try:
            log.info("Removing GDB " + fgdb_path)
            shutil.rmtree(fgdb_path)
        except WindowsError as e:
            log.error("WindowsError: could not delete folder")
            log.error(str(e).replace("\n", "; "))
            raise

    try:
        log.info("creating GDB " + fgdb_name)
        arcpy.CreateFileGDB_management (out_folder_path=install_folder,
                                        out_name=fgdb_name,
                                        out_version="CURRENT")
    except arcpy.ExecuteError as e:
        log.error("ExecuteError - folder exists")
        log.error(str(e).replace("\n", "; "))
        raise


# -----------------------------------------
# create_crs_fcs
# -----------------------------------------


def create_crs_fcs():
    """create a set of point feature classes in the test gdb
       pre: fgdb_name = "fc_profiler_test.gdb"
       pre: fgdb_name exists in install_folder
    """

    fgdb_name = "fc_profiler_test.gdb"
    out_path = os.path.join(install_folder, fgdb_name)
    geometry_type = "POINT"

    # dict of FC names and WKIDs
    crs_fcs = {"GDA94_point": 4283,
               "WGS84_point": 4326,
               "Web_Mercator_point": 3857,
               "MGAZ56_point": 28356,
               "GDA94_GA_Lambert_point": 3112}

    # create FCs with a CRS
    for name,wkid in crs_fcs.iteritems():
        log.info("Creating FC " + name + " with CRS " + str(wkid))
        sr = arcpy.SpatialReference(wkid)
        arcpy.CreateFeatureclass_management(out_path=out_path,
                                            out_name=name,
                                            geometry_type=geometry_type,
                                            has_m='DISABLED',
                                            has_z='DISABLED',
                                            spatial_reference=sr)

    # create one FC without a CRS

    name = "NO_CRS_point"
    log.info("Creating FC " + name + " with NO CRS ")
    arcpy.CreateFeatureclass_management(out_path=out_path,
                                        out_name=name,
                                        geometry_type=geometry_type,
                                        has_m='DISABLED',
                                        has_z='DISABLED')

# -----------------------------------------
# create_spatial_type_fcs
# -----------------------------------------


def create_geometry_type_fcs():
    """create a set of feature classes in the test gdb with the set of
       geometry types:
           POINT
           MULTIPATCH
           MULTIPOINT
           POLYGON
           POLYLINE
       pre: fgdb_name = "fc_profiler_test.gdb"
       pre: fgdb_name exists in install_folder

       assumes "GDA94_point" already exists
    """

    fgdb_name = "fc_profiler_test.gdb"
    out_path = os.path.join(install_folder, fgdb_name)
    wkid = 4283 # GDA94 lat/long
    sr = arcpy.SpatialReference(wkid)

    # dict of FC names and geometry_types
    geometry_type_fcs = {"GDA94_multipatch": "MULTIPATCH",
                          "GDA94_multipoint": "MULTIPOINT",
                          "GDA94_polygon": "POLYGON",
                          "GDA94_polyline": "POLYLINE"}

    # create FCs with a CRS
    for name,geometry_type in geometry_type_fcs.iteritems():
        log.info("Creating FC " + name +
                 " with geometery type " + geometry_type +
                 " and CRS " + str(wkid))

        arcpy.CreateFeatureclass_management(out_path=out_path,
                                            out_name=name,
                                            geometry_type=geometry_type,
                                            has_m='DISABLED',
                                            has_z='DISABLED',
                                            spatial_reference=sr)


# -----------------------------------------
# main
# -----------------------------------------

def main():
    """main"""
    log.info("Start")

    log.info("Creating file geodatabase fc_profiler_test.gdb")
    create_fgdb_test()

    log.info("Creating CRS test feature classes")
    create_crs_fcs()

    log.info("Creating spatial Type test feature classes")
    create_geometry_type_fcs()

    log.info("Finished")
    end_time = datetime.datetime.now()
    duration = end_time - start_time
    log.info("Duration " + str(duration))


if __name__ == "__main__":
    setup_logger()
    main()


