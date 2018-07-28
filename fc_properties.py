import arcpy
import logging
log = logging.getLogger()


# -----------------------------------------
# get CRS functions
# -----------------------------------------

def get_crs_name(fc_path):
    sr = arcpy.Describe(fc_path).spatialReference
    log.debug("get_crs_name returning: " + sr.name)
    return sr.name

def get_crs_wkid(fc_path):
    sr = arcpy.Describe(fc_path).spatialReference
    log.debug("get_crs_wkid returning: " + str(sr.factoryCode))
    return sr.factoryCode

def get_crs_units(fc_path):
    return "buz"

