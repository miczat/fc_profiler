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
import collections
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
    env.workspace = os.path.join(install_folder, fgdb_name)
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
    log.info("Creating polygon and point FCs with 5 million records (can take 15 minutes")
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


def create_field_types(fgdb_path):
    """
    :param  fgdb_path: file path to the file geodatabase
    :type fgdb_path: basestring
    """
    arcpy.env.workspace = fgdb_path
    arcpy.env.overwriteOutput = True

    fc_name = "GDA94_all_field_types_polyline"
    wkid = 4283 # GDA94 lat/long
    geometry_type = "POLYLINE"
    has_m = "DISABLED"
    has_z = "DISABLED"
    sr = arcpy.SpatialReference(wkid)

    arcpy.CreateFeatureclass_management(out_path=fgdb_path,
                                        out_name=fc_name,
                                        geometry_type=geometry_type,
                                        has_m=has_m,
                                        has_z=has_z,
                                        spatial_reference=sr)

    Field = collections.namedtuple('Field', ['field_name',
                                             'field_type',
                                             'field_precision',
                                             'field_scale',
                                             'field_length',
                                             'field_alias',
                                             'field_is_nullable',
                                             'field_is_required',
                                             'field_domain'])

    text_field = Field(field_name="text_field",
                       field_type="TEXT",
                       field_precision="",
                       field_scale="",
                       field_length="",
                       field_alias="",
                       field_is_nullable="NULLABLE",
                       field_is_required="NON_REQUIRED",
                       field_domain="")

    float_field = Field(field_name="float_field",
                        field_type="FLOAT",
                        field_precision="",
                        field_scale="",
                        field_length="",
                        field_alias="",
                        field_is_nullable="NULLABLE",
                        field_is_required="NON_REQUIRED",
                        field_domain="")

    double_field = Field(field_name="double_field",
                         field_type="DOUBLE",
                         field_precision="",
                         field_scale="",
                         field_length="",
                         field_alias="",
                         field_is_nullable="NULLABLE",
                         field_is_required="NON_REQUIRED",
                         field_domain="")

    short_field = Field(field_name="short_field",
                        field_type="SHORT",
                        field_precision="",
                        field_scale="",
                        field_length="",
                        field_alias="",
                        field_is_nullable="NULLABLE",
                        field_is_required="NON_REQUIRED",
                        field_domain="")

    long_field = Field(field_name="long_field",
                       field_type="LONG",
                       field_precision="",
                       field_scale="",
                       field_length="",
                       field_alias="",
                       field_is_nullable="NULLABLE",
                       field_is_required="NON_REQUIRED",
                       field_domain="")

    date_field = Field(field_name="date_field",
                       field_type="DATE",
                       field_precision="",
                       field_scale="",
                       field_length="",
                       field_alias="",
                       field_is_nullable="NULLABLE",
                       field_is_required="NON_REQUIRED",
                       field_domain="")

    blob_field = Field(field_name="blob_field",
                       field_type="BLOB",
                       field_precision="",
                       field_scale="",
                       field_length="",
                       field_alias="",
                       field_is_nullable="",
                       field_is_required="NON_REQUIRED",
                       field_domain="")

    raster_field = Field(field_name="raster_field",
                         field_type="RASTER",
                         field_precision="",
                         field_scale="",
                         field_length="",
                         field_alias="",
                         field_is_nullable="NULLABLE",
                         field_is_required="NON_REQUIRED",
                         field_domain="")

    guid_field = Field(field_name="guid_field",
                       field_type="GUID",
                       field_precision="",
                       field_scale="",
                       field_length="",
                       field_alias="",
                       field_is_nullable="NULLABLE",
                       field_is_required="NON_REQUIRED",
                       field_domain="")

    text_field_non_nullable = Field(field_name="text_field_non_nullable",
                                    field_type="TEXT",
                                    field_precision="",
                                    field_scale="",
                                    field_length="",
                                    field_alias="",
                                    field_is_nullable="NON_NULLABLE",
                                    field_is_required="NON_REQUIRED",
                                    field_domain="")

    short_field_required = Field(field_name="short_field_required",
                                 field_type="SHORT",
                                 field_precision="",
                                 field_scale="",
                                 field_length="",
                                 field_alias="",
                                 field_is_nullable="NULLABLE",
                                 field_is_required="REQUIRED",
                                 field_domain="")

    guid_field_alias = Field(field_name="guid_field_alias",
                             field_type="GUID",
                             field_precision="",
                             field_scale="",
                             field_length="",
                             field_alias="Globally Unique ID",
                             field_is_nullable="NULLABLE",
                             field_is_required="NON_REQUIRED",
                             field_domain="")

    date_field_non_nullable_required_alias = Field(field_name="date_field_non_nullable_required",
                                                   field_type="DATE",
                                                   field_precision="",
                                                   field_scale="",
                                                   field_length="",
                                                   field_alias="Required non-null date",
                                                   field_is_nullable="NULLABLE",
                                                   field_is_required="REQUIRED",
                                                   field_domain="")

    float_field_default_value = Field(field_name="float_field_default_value",
                                      field_type="FLOAT",
                                      field_precision="",
                                      field_scale="",
                                      field_length="",
                                      field_alias="",
                                      field_is_nullable="NULLABLE",
                                      field_is_required="NON_REQUIRED",
                                      field_domain="")

    double_field_default_value = Field(field_name="double_field_default_value",
                                       field_type="DOUBLE",
                                       field_precision="",
                                       field_scale="",
                                       field_length="",
                                       field_alias="",
                                       field_is_nullable="NULLABLE",
                                       field_is_required="NON_REQUIRED",
                                       field_domain="")

    text_field_default_value = Field(field_name="text_field_default_value",
                                     field_type="TEXT",
                                     field_precision="",
                                     field_scale="",
                                     field_length="26",
                                     field_alias="",
                                     field_is_nullable="NULLABLE",
                                     field_is_required="NON_REQUIRED",
                                     field_domain="")

    short_field_default_value = Field(field_name="short_field_default_value",
                                      field_type="SHORT",
                                      field_precision="",
                                      field_scale="",
                                      field_length="",
                                      field_alias="",
                                      field_is_nullable="NULLABLE",
                                      field_is_required="NON_REQUIRED",
                                      field_domain="")

    date_field_default_value = Field(field_name="date_field_default_value",
                                     field_type="DATE",
                                     field_precision="",
                                     field_scale="",
                                     field_length="",
                                     field_alias="",
                                     field_is_nullable="NULLABLE",
                                     field_is_required="NON_REQUIRED",
                                     field_domain="")

    fields_list = [text_field,
                   float_field,
                   double_field,
                   short_field,
                   long_field,
                   date_field,
                   blob_field,
                   raster_field,
                   guid_field,
                   text_field_non_nullable,
                   short_field_required,
                   guid_field_alias,
                   date_field_non_nullable_required_alias,
                   float_field_default_value,
                   double_field_default_value,
                   text_field_default_value,
                   short_field_default_value,
                   date_field_default_value
                   ]

    log.info(str(len(fields_list)) + " fields defined")

    for field in fields_list:
        log.info("adding field " + field.field_name)
        arcpy.AddField_management(fc_name,
                                  field.field_name,
                                  field.field_type,
                                  field.field_precision,
                                  field.field_scale,
                                  field.field_length,
                                  field.field_alias,
                                  field.field_is_nullable,
                                  field.field_is_required,
                                  field.field_domain)

    arcpy.AssignDefaultToField_management(in_table=fc_name,
                                          field_name="float_field_default_value",
                                          default_value=123.456
                                          )

    arcpy.AssignDefaultToField_management(in_table=fc_name,
                                          field_name="double_field_default_value",
                                          default_value=1234567890.012345
                                          )

    arcpy.AssignDefaultToField_management(in_table=fc_name,
                                          field_name="text_field_default_value",
                                          default_value="abcdefghijklmnopqrstuvwxyz")

    arcpy.AssignDefaultToField_management(in_table=fc_name,
                                          field_name="short_field_default_value",
                                          default_value=5)

    arcpy.AssignDefaultToField_management(in_table=fc_name,
                                          field_name="date_field_default_value",
                                          default_value="10-08-2018 10:06:55 PM")


def create_fc_fields_with_domains(fgdb_path):
    """
    :param  fgdb_path: file path to the file geodatabase
    :type fgdb_path: basestring
    """
    arcpy.env.workspace = fgdb_path
    arcpy.env.overwriteOutput = True

    # ---------------------------------------------------------------
    # define domains
    #
    # pattern:
    #
    #    for coded domains
    #        create a domain object _in the GDB_ (not as a Python object)
    #        create a dictionary of domain code:description pairs
    #        load the dictionary into the domain
    #        use the domain when creating a feature class or use
    #            arcpy.AssignDomainToField_management()
    #
    #    for range domains
    #        create a domain object _in the GDB_ (not as a Python object)
    #        set SetValueForRangeDomain_management
    #        use the domain when creating a feature class or use
    #            arcpy.AssignDomainToField_management()
    #
    # --------------------------------------------------------------

    log.info("Creating feature class")
    fc_name = "GDA94_fields_with_domains_polyline"
    fc_path = os.path.join(fgdb_path, fc_name)

    arcpy.CreateFeatureclass_management(out_path=fgdb_path,
                                        out_name=fc_name,
                                        geometry_type="POLYLINE",
                                        spatial_reference=arcpy.SpatialReference(4283))  # GDA94 lat/long)

    log.info("Creating domains")
    # --------------------------------------
    domain_name = "text_field_coded_domain"
    arcpy.CreateDomain_management(in_workspace=fgdb_path,
                                  domain_name=domain_name,
                                  domain_description="uses a coded TEXT domain",
                                  field_type="TEXT",
                                  domain_type="CODED")

    text_field_coded_domain_dict = {"R": "Red",
                                    "G": "Green",
                                    "B": "Blue"}

    for code in text_field_coded_domain_dict:
        arcpy.AddCodedValueToDomain_management(in_workspace=fgdb_path,
                                               domain_name=domain_name,
                                               code=code,
                                               code_description=text_field_coded_domain_dict[code])

    arcpy.AddField_management(in_table=fc_path,
                              field_name="text_field_with_coded_domain",
                              field_type="TEXT",
                              field_length=50,
                              field_alias="has a TEXT coded domain",
                              field_domain="text_field_coded_domain")

    # -----------------------------------------------------------------------------------

    domain_name = "float_field_coded_domain"
    arcpy.CreateDomain_management(in_workspace=fgdb_path,
                                  domain_name=domain_name,
                                  domain_description="uses a coded FLOAT domain",
                                  field_type="FLOAT",
                                  domain_type="CODED")

    float_field_coded_domain_dict = {1.1: "one decimal place",
                                     1.01: "two decimal places",
                                     1.001: "three decimal places"}

    for code in float_field_coded_domain_dict:
        arcpy.AddCodedValueToDomain_management(in_workspace=fgdb_path,
                                               domain_name=domain_name,
                                               code=code,
                                               code_description=float_field_coded_domain_dict[code])

    arcpy.AddField_management(in_table=fc_path,
                              field_name="float_field_with_coded_domain",
                              field_type="FLOAT",
                              field_alias="has a FLOAT coded domain",
                              field_domain="float_field_coded_domain")

    # -----------------------------------------------------------------------------------

    domain_name = "float_field_range_domain"
    arcpy.CreateDomain_management(in_workspace=fgdb_path,
                                  domain_name=domain_name,
                                  domain_description="uses a FLOAT range domain",
                                  field_type="FLOAT",
                                  domain_type="RANGE")

    arcpy.SetValueForRangeDomain_management(in_workspace=fgdb_path,
                                            domain_name=domain_name,
                                            min_value=1.1,
                                            max_value=2.2)

    arcpy.AddField_management(in_table=fc_path,
                              field_name="float_field_with_range_domain",
                              field_type="FLOAT",
                              field_alias="has a FLOAT range domain",
                              field_domain="float_field_range_domain")

    # -----------------------------------------------------------------------------------

    domain_name = "double_field_coded_domain"
    arcpy.CreateDomain_management(in_workspace=fgdb_path,
                                  domain_name=domain_name,
                                  domain_description="uses a coded DOUBLE domain",
                                  field_type="DOUBLE",
                                  domain_type="CODED")

    double_field_coded_domain_dict = {2.2: "one decimal place",
                                     2.00000000001: "10 decimal places",
                                     2.00000000000000000002: "20 decimal places"}

    for code in double_field_coded_domain_dict:
        arcpy.AddCodedValueToDomain_management(in_workspace=fgdb_path,
                                               domain_name=domain_name,
                                               code=code,
                                               code_description=double_field_coded_domain_dict[code])

    arcpy.AddField_management(in_table=fc_path,
                              field_name="double_field_with_coded_domain",
                              field_type="DOUBLE",
                              field_alias="has a DOUBLE coded domain",
                              field_domain="double_field_coded_domain")

    # -----------------------------------------------------------------------------------

    domain_name = "double_field_range_domain"
    arcpy.CreateDomain_management(in_workspace=fgdb_path,
                                  domain_name=domain_name,
                                  domain_description="uses a DOUBLE range domain",
                                  field_type="DOUBLE",
                                  domain_type="RANGE")

    arcpy.SetValueForRangeDomain_management(in_workspace=fgdb_path,
                                            domain_name=domain_name,
                                            min_value=1.00000000000000000001,
                                            max_value=20000000000000000000.2)

    arcpy.AddField_management(in_table=fc_path,
                              field_name="double_field_with_range_domain",
                              field_type="DOUBLE",
                              field_alias="has a DOUBLE range domain",
                              field_domain="double_field_range_domain")

    # -----------------------------------------------------------------------------------

    domain_name = "short_field_coded_domain"
    arcpy.CreateDomain_management(in_workspace=fgdb_path,
                                  domain_name=domain_name,
                                  domain_description="uses a coded SHORT domain",
                                  field_type="SHORT",
                                  domain_type="CODED")

    short_field_coded_domain_dict = {101: "one O one",
                                      102: "one O two",
                                      103: "one O three"}

    for code in short_field_coded_domain_dict:
        arcpy.AddCodedValueToDomain_management(in_workspace=fgdb_path,
                                               domain_name=domain_name,
                                               code=code,
                                               code_description=short_field_coded_domain_dict[code])

    arcpy.AddField_management(in_table=fc_path,
                              field_name="short_field_with_coded_domain",
                              field_type="SHORT",
                              field_alias="has a SHORT coded domain",
                              field_domain="short_field_coded_domain")

    # -----------------------------------------------------------------------------------

    domain_name = "short_field_range_domain"
    arcpy.CreateDomain_management(in_workspace=fgdb_path,
                                  domain_name=domain_name,
                                  domain_description="uses a SHORT range domain",
                                  field_type="SHORT",
                                  domain_type="RANGE")

    arcpy.SetValueForRangeDomain_management(in_workspace=fgdb_path,
                                            domain_name=domain_name,
                                            min_value=1000,
                                            max_value=2000)

    arcpy.AddField_management(in_table=fc_path,
                              field_name="short_field_with_range_domain",
                              field_type="SHORT",
                              field_alias="has a SHORT range domain",
                              field_domain="short_field_range_domain")

    # -----------------------------------------------------------------------------------

    domain_name = "long_field_coded_domain"
    arcpy.CreateDomain_management(in_workspace=fgdb_path,
                                  domain_name=domain_name,
                                  domain_description="uses a coded LONG domain",
                                  field_type="LONG",
                                  domain_type="CODED")

    long_field_coded_domain_dict = {40000: "forty thousand",
                                     400000: "four hundred thousand",
                                     4000000: "four million"}

    for code in long_field_coded_domain_dict:
        arcpy.AddCodedValueToDomain_management(in_workspace=fgdb_path,
                                               domain_name=domain_name,
                                               code=code,
                                               code_description=
                                               long_field_coded_domain_dict[code])

    arcpy.AddField_management(in_table=fc_path,
                              field_name="long_field_with_coded_domain",
                              field_type="LONG",
                              field_alias="has a LONG coded domain",
                              field_domain="long_field_coded_domain")

    # -----------------------------------------------------------------------------------

    domain_name = "long_field_range_domain"
    arcpy.CreateDomain_management(in_workspace=fgdb_path,
                                  domain_name=domain_name,
                                  domain_description="uses a LONG range domain",
                                  field_type="LONG",
                                  domain_type="RANGE")

    arcpy.SetValueForRangeDomain_management(in_workspace=fgdb_path,
                                            domain_name=domain_name,
                                            min_value=12000000,
                                            max_value=120000000)

    arcpy.AddField_management(in_table=fc_path,
                              field_name="long_field_with_range_domain",
                              field_type="LONG",
                              field_alias="has a LONG range domain",
                              field_domain="long_field_range_domain")

    # -----------------------------------------------------------------------------------

    domain_name = "date_field_coded_domain"
    arcpy.CreateDomain_management(in_workspace=fgdb_path,
                                  domain_name=domain_name,
                                  domain_description="uses a coded DATE domain",
                                  field_type="DATE",
                                  domain_type="CODED")

    date_field_coded_domain_dict = {"01-02-1972": "Mic's Birthday",
                                    "09-08-1969": "Donna's Birthday",
                                    "22-04-2002": "Annie's Birthday"}

    for code in date_field_coded_domain_dict:
        arcpy.AddCodedValueToDomain_management(in_workspace=fgdb_path,
                                               domain_name=domain_name,
                                               code=code,
                                               code_description=
                                               date_field_coded_domain_dict[code])

    arcpy.AddField_management(in_table=fc_path,
                              field_name="date_field_with_coded_domain",
                              field_type="DATE",
                              field_alias="has a DATE coded domain",
                              field_domain="date_field_coded_domain")

    # -----------------------------------------------------------------------------------

    domain_name = "date_field_range_domain"
    arcpy.CreateDomain_management(in_workspace=fgdb_path,
                                  domain_name=domain_name,
                                  domain_description="uses a DATE range domain",
                                  field_type="DATE",
                                  domain_type="RANGE")

    arcpy.SetValueForRangeDomain_management(in_workspace=fgdb_path,
                                            domain_name=domain_name,
                                            min_value="01-01-1972",
                                            max_value="22-04-2002")

    arcpy.AddField_management(in_table=fc_path,
                              field_name="date_field_with_range_domain",
                              field_type="DATE",
                              field_alias="has a DATE range domain",
                              field_domain="date_field_range_domain")

    # -----------------------------------------------------------------------------------


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

    log.info("Creating feature classes with all field types and configurations")
    create_field_types(fgdb_path)

    log.info("Create feature classes with domains")
    create_fc_fields_with_domains(fgdb_path)

    log.info("Finished")
    end_time = datetime.datetime.now()
    duration = end_time - start_time
    log.info("Duration " + str(duration))


if __name__ == "__main__":
    setup_logger()
    main()


