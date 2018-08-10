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

    log.info("Writing XLS")
    log.debug("xls_path = " + xls_path)
    xls_output.write_fc_properties(fc_properties_list, xls_path)
