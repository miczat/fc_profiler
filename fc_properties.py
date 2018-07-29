import arcpy
import logging
log = logging.getLogger()


# -----------------------------------------
# get_fc_gdb_name
# -----------------------------------------

def get_fc_gdb_path(fc_path):
    """returns the path of the parent file geodatabase
    pre: the fc_path is a valid fGDB path"""
    gdb_path = fc_path.split(".gdb", 1)[0] + ".gdb"
    log.debug("get_fc_gdb_path returning: " + gdb_path)
    return gdb_path


# -----------------------------------------
# get name
# -----------------------------------------

def get_fc_name(fc_path):
    """returns the name of a feature class from the feature class object"""
    base_name = arcpy.Describe(fc_path).baseName
    log.debug("get_crs_name returning: " + base_name)
    return base_name


# -----------------------------------------
# get geometry type
# -----------------------------------------

def get_fc_geometry_type(fc_path):
    """returns the geometry type of a feature class
       usually in the set {MultiPatch, Multipoint,Point,Polyline,Polygon}
    """
    geometry_type = arcpy.Describe(fc_path).shapeType
    log.debug("get_fc_geometry_type returning: " + geometry_type)
    return geometry_type


# -----------------------------------------
# get CRS functions
# -----------------------------------------

def get_crs_name(fc_path):
    """returns the coordinate system name of a feature class"""
    sr = arcpy.Describe(fc_path).spatialReference
    log.debug("get_crs_name returning: " + sr.name)
    return sr.name


def get_crs_wkid(fc_path):
    """returns the coordinate system EPSG WKID of a feature class"""
    sr = arcpy.Describe(fc_path).spatialReference
    log.debug("get_crs_wkid returning: " + str(sr.factoryCode))
    return sr.factoryCode


def get_crs_type(fc_path):
    """returns the type of coordiate system of a feature class
       usually in the set {geographic, projected}
    """
    sr = arcpy.Describe(fc_path).spatialReference
    log.debug("get_crs_type returning: " + str(sr.type))
    return sr.type


def get_crs_units(fc_path):
    """returns the geometry units of a feature class
       usually in the set {degrees, meters}
    """

    sr = arcpy.Describe(fc_path).spatialReference
    if sr.type == "Projected":
        units = sr.linearUnitName
    elif sr.type == "Geographic":
        units = sr.angularUnitName
    else:
        units = "Unknown"
    log.debug("get_crs_units returning: " + str(units))
    return units