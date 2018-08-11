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
    :param xls_path: the name of the xls file to delete
    :type xls_path: basestring
    :raises WindowsError
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
#     this is the main function that controls the profile generation
#
#     It is designed to be called by either the command line interface which has
#     validated validated inputs, or a Python toolbox which has validated inputs
#
#     :param fc_path    - fully qualified path to the input feature class to profile
#     :param out_folder - a writable folder
#     :param overwrite  - a flag to identity if an existing XLS should be overwritten
#     :pre the input feature class exists
#     :pre the output folder has write access
#     :post an xls file will be written
#     :return None
# -----------------------------------------

def generate_profile(fc_path, out_folder, overwrite):
    """
    :param fc_path: the full path to the feature class
    :type fc_path: basestring

    :param out_folder: the output folder
    :type out_folder: basestring

    :param overwrite: a flag to indicate if outputs should be overwritten
    :type overwrite: bool

    """

    log.info("Determining output XLS filename")
    xls_path = os.path.join(out_folder, fc_properties.get_fc_name(fc_path) + report_ext)
    if overwrite is True:
        log.info("Deleting existing xls file")
        delete_existing_xls(xls_path)

    log.info("Getting feature class properties")
    fc_properties_list = fc_properties.get_fc_properties(fc_path)

    log.info("Writing feature class properties to XLS")
    xls_output.write_fc_properties(fc_properties_list, xls_path)

    log.info("Getting feature class structure")
    fc_structure = fc_properties.get_fc_structure(fc_path)

    log.info("Writing feature class structure to XLS")
    xls_output.write_fc_structure(fc_structure, xls_path)
