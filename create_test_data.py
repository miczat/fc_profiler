#!./venv_p27arcpy/Scripts/python.exe
__author__ = "Mic Zatorsky"
__copyright__ = "Copyright 2018, Michael Zatorsky "
__license__ = "CC BT-SA 4.0"
__version__ = "1.2.0"
__date__ = "11/08/2018"

# ----------------------------------------------------------------------------
# description: Creates a suite of file geodatabases for use with unit
#              testing
# created      11/08/2018
#
# Run instructions:  configure run config and execute
# ----------------------------------------------------------------------------

import logging
import os
import sys
import shutil
import datetime
import arcpy
from arcpy import env

start_time = datetime.datetime.now()
log = logging.getLogger()

# -----------------------------------------
# run config (globals)
# -----------------------------------------
program_name = r"create_test_data"
log_folder = r"."
install_folder = r"c:\tmp\fc_profiler_testdata"
fgdb_name = "fc_profiler_test.gdb"
overwrite = True  # overwrite the existing test DB if it exists?


# -----------------------------------------
# create and configure the logger
# -----------------------------------------
def setup_logger():
    """setup logger"""
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
#     create the empty test file geodatabase
#     pre: install folder exists
#     pre: fgdb_path exists
# -----------------------------------------

def create_fgdb_test(install_folder, fgdb_name):
    """
    :param install_folder: the folder in which to create the GDB
    :type install_folder: basestring

    :param fgdb_name: the name of the fgdb, no path, with the .gdb extension
    :type fgdb_name: basestring

    :raises WindowsError: if the existing data cannot be overwritten
    """

    fgdb_path = os.path.join(install_folder, fgdb_name)
    log.debug("fgdb_path = " + fgdb_path)

    log.debug("Checking for fGDB existance")
    if os.path.exists(fgdb_path) and overwrite is True:
        try:
            log.info("Removing GDB " + fgdb_path)
            shutil.rmtree(fgdb_path)
        except WindowsError as e:
            log.error("WindowsError: could not delete folder")
            log.error("Check if the folder is being access by ArcMap or ArcCatalog")
            log.error(str(e).replace("\n", "; "))
            raise
        except Exception as e:
            log.error("Some other error")
            log.error(str(e).replace("\n", "; "))
            raise


    if os.path.exists(install_folder):
        try:
            log.info("creating GDB " + fgdb_path)
            arcpy.CreateFileGDB_management(out_folder_path=install_folder,
                                           out_name=fgdb_name,
                                           out_version="CURRENT")
        except arcpy.ExecuteError as e:
            log.error("ExecuteError - folder exists")
            log.error(str(e).replace("\n", "; "))
            raise
        except Exception as e:
            log.error("Some other error")
            log.error(str(e).replace("\n", "; "))
            raise
    else:
        log.error("Could not find the installation folder " + install_folder )
        log.error("Program stopping")
        sys.exit(1)


# -----------------------------------------
# create_crs_fcs
#     create a set of point feature classes in the test gdb
#     pre: fgdb_name exists in install_folder
# -----------------------------------------


def create_crs_fcs(fgdb_path):
    """
    :param fgdb_path: file path to the file geodatabase
    :type fgdb_path: basestring
    """

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
        arcpy.CreateFeatureclass_management(out_path=fgdb_path,
                                            out_name=name,
                                            geometry_type=geometry_type,
                                            has_m='DISABLED',
                                            has_z='DISABLED',
                                            spatial_reference=sr)

    # create one FC with NO CRS
    name = "NO_CRS_point"
    log.info("Creating FC " + name + " with NO CRS ")
    arcpy.CreateFeatureclass_management(out_path=fgdb_path,
                                        out_name=name,
                                        geometry_type=geometry_type,
                                        has_m='DISABLED',
                                        has_z='DISABLED')

# ----------------------------------------------------------------------
# create_spatial_type_fcs
#     create a set of feature classes in the test gdb with the set of
#        geometry types:
#            POINT  (already created above)
#            MULTIPATCH (not in this version supporting 10.3
#            MULTIPOINT
#            POLYGON
#            POLYLINE
#        pre: fgdb_name = "fc_profiler_test.gdb"
#        pre: fgdb_name exists in install_folder
# -------------------------------------------------------------------------


def create_geometry_type_fcs(fgdb_path):
    """
    :param fgdb_path: file path to the file geodatabase
    :type fgdb_path: basestring
    """

    wkid = 4283 # GDA94 lat/long
    sr = arcpy.SpatialReference(wkid)

    # dict of FC names and geometry_types
    geometry_type_fcs = {"GDA94_multipoint": "MULTIPOINT",
                         "GDA94_polygon": "POLYGON",
                         "GDA94_polyline": "POLYLINE"}

    # create FCs with a CRS
    for name, geometry_type in geometry_type_fcs.iteritems():
        log.info("Creating FC " + name +
                 " with geometery type " + geometry_type +
                 " and CRS " + str(wkid))

        arcpy.CreateFeatureclass_management(out_path=fgdb_path,
                                            out_name=name,
                                            geometry_type=geometry_type,
                                            has_m='DISABLED',
                                            has_z='DISABLED',
                                            spatial_reference=sr)


# -----------------------------------------
# create_Z_M_enabled
#     create a set of feature class in the test gdb with:
#
#     Z only enabled
#     M only enabled
#     Z and M enabled
#
#     pre: fgdb_name = "fc_profiler_test.gdb"
#     pre: fgdb_name exists in install_folder
# -----------------------------------------


def create_z_m_enabled(fgdb_path):
    """
    :param  fgdb_path: file path to the file geodatabase
    :type fgdb_path: basestring
    """

    # Z values only enabled
    out_name = "MGAZ56_has_Z_polyline"
    wkid = 28356
    geometry_type = "POLYLINE"
    has_m = "DISABLED"
    has_z = "ENABLED"
    sr = arcpy.SpatialReference(wkid)

    log.info("Creating FC with M enabled")
    arcpy.CreateFeatureclass_management(out_path=fgdb_path,
                                        out_name=out_name,
                                        geometry_type=geometry_type,
                                        has_m=has_m,
                                        has_z=has_z,
                                        spatial_reference=sr)

    # M values only enabled
    out_name = "MGAZ56_has_M_polyline"
    wkid = 28356
    geometry_type = "POLYLINE"
    has_m = "ENABLED"
    has_z = "DISABLED"
    sr = arcpy.SpatialReference(wkid)

    log.info("Creating FC with both Z enabled")
    arcpy.CreateFeatureclass_management(out_path=fgdb_path,
                                        out_name=out_name,
                                        geometry_type=geometry_type,
                                        has_m=has_m,
                                        has_z=has_z,
                                        spatial_reference=sr)

    # both Z and M values enabled
    out_name = "MGAZ56_has_Z_M_polyline"
    wkid = 28356
    geometry_type = "POLYLINE"
    has_m = "ENABLED"
    has_z = "ENABLED"
    sr = arcpy.SpatialReference(wkid)

    log.info("Creating FC with both Z and M enabled")
    arcpy.CreateFeatureclass_management(out_path=fgdb_path,
                                        out_name=out_name,
                                        geometry_type=geometry_type,
                                        has_m=has_m,
                                        has_z=has_z,
                                        spatial_reference=sr)


# ---------------------------------------------------
# Creating feature classes with varying record counts
#     create the empty test file geodatabase
#     pre: install folder exists
#     pre: fgdb_path exists
# ---------------------------------------------------

def create_records(install_folder, fgdb_name):
    """
    :param install_folder: the folder to install the test data in
    :type install_folder: basestring

    :param fgdb_name: the name of the fgdb, no path, with the .gdb extension
    :type fgdb_name: basestring
    """
    env.workspace = os.path.join(install_folder,fgdb_name)
    env.outputCoordinateSystem = arcpy.SpatialReference(28356)  # MGA Zone 56
    env.overwriteOutput = True

    # Typical Case, 602 records
    log.info("Creating polyline FC with 602 records")
    fgdb_path = os.path.join(install_folder,fgdb_name,"MGAZ56_602_rec_polyline")
    arcpy.CreateFishnet_management(out_feature_class=fgdb_path,
                                   origin_coord='500000 6950000',
                                   y_axis_coord='500000 6950100',
                                   cell_width=100,
                                   cell_height=100,
                                   number_rows=300,
                                   number_columns=300,
                                   labels="NO_LABELS",
                                   geometry_type="POLYLINE")

    # Edge Case, 5 million records
    log.info("Creating polygon and Point FCs with 5 million records")
    fgdb_path = os.path.join(install_folder, fgdb_name, "MGAZ56_5_million_rec_polygon")
    arcpy.CreateFishnet_management(out_feature_class=fgdb_path,
                                   origin_coord='500000 6950000',
                                   y_axis_coord='500000 6950100',
                                   cell_width=100,
                                   cell_height=100,
                                   number_rows=2000,
                                   number_columns=2500,
                                   labels="LABELS",
                                   geometry_type="POLYGON")

    # rename the label points
    arcpy.Rename_management(in_data="MGAZ56_5_million_rec_polygon_label",
                            out_data="MGAZ56_5_million_rec_point",
                            data_type="FeatureClass")


# -----------------------------------------
# main
# -----------------------------------------


def main():
    """main"""
    log.info("Start")
    fgdb_path = os.path.join(install_folder, fgdb_name)

    log.info("Creating empty file geodatabase fc_profiler_test.gdb")
    create_fgdb_test(install_folder, fgdb_name)

    log.info("Creating feature classes with a range of coordinate systems")
    create_crs_fcs(fgdb_path)

    log.info("Creating feature classes with other spatial data types")
    create_geometry_type_fcs(fgdb_path)

    log.info("Creating feature classes with Z and M enabled")
    create_z_m_enabled(fgdb_path)

    log.info("Creating feature classes with varying record counts")
    create_records(install_folder, fgdb_name)

    log.info("Finished")
    end_time = datetime.datetime.now()
    duration = end_time - start_time
    log.info("Duration " + str(duration))


if __name__ == "__main__":
    setup_logger()
    main()


