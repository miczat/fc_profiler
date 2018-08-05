import arcpy
import logging
import os
import fc_properties
import xls_output

log = logging.getLogger()


# --------------------------------------------
# run config (globals) - not user configurable
# --------------------------------------------
report_ext = "_fc_profile.xls"


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
# get_fc_properties
# -----------------------------------------

def get_fc_properties(fc_path):
    """
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

    return fc_properties_list


# -----------------------------------------
# get_field_properties
# -----------------------------------------

def get_field_properties(fc_path, field):
    # STUB
    pass

# -----------------------------------------
# generate profile
# -----------------------------------------

def generate_profile(fc_path, out_folder, overwrite):

    """
    this is the main function that controls the profile generation

    It is designed to be called by either a validated scipt tool, or a validated
    Python toolbox.

    :param fc_path    - fully qualified path to the input feature class to profile
    :param out_folder - a writable folder
    :param overwrite  - a flag to identity if an existing XLS should be overwritten
    :pre the input feature class exists
    :pre the output folder has write access
    :post an xls file will be written
    :return None
    """

    log.info("Determining output XLS filename")
    xls_path = os.path.join(out_folder, fc_properties.get_fc_name(fc_path) + report_ext)
    if overwrite is True:
        log.info("Deleting existing xls file")
        delete_existing_xls(xls_path)

    log.info("Getting feature class properties")
    fc_properties_list = fc_properties.get_fc_properties(fc_path)
    # write the list of feature class properties to Excel

    log.info("Writing XLS")
    log.debug("xls_path = " + xls_path)
    xls_output.write_fc_properties(fc_properties_list, xls_path)
