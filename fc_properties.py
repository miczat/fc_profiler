import arcpy
import logging
log = logging.getLogger()


# -----------------------------------------
# get name
# -----------------------------------------

def get_fc_name(fc_path):
    base_name = arcpy.Describe(fc_path).baseName
    log.debug("get_crs_name returning: " + base_name)
    return base_name



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


def get_crs_type(fc_path):
    sr = arcpy.Describe(fc_path).spatialReference
    log.debug("get_crs_type returning: " + str(sr.type))
    return sr.type


def get_crs_units(fc_path):
    sr = arcpy.Describe(fc_path).spatialReference
    if sr.type == "Projected":
        units = sr.linearUnitName
    elif sr.type == "Geographic":
        units = sr.angularUnitName
    else:
        units = "Unknown"
    log.debug("get_crs_units returning: " + str(units))
    return units