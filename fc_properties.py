import arcpy
import logging
log = logging.getLogger()


# -----------------------------------------
# get_fc_properties
# -----------------------------------------

def get_fc_properties(fc_path):
    """
    this is the main function that controls the profile generation

    :param fc_path: - fully qualified path to the input feature class to profile
    pre: the input feature class exists
    pre: the output xls is somewhere that can be writen too
    post: a xls file will be written
    :return: None
    """

    # generate the list of feature class properties
    fc_properties_list = [("Feature Class", get_fc_name(fc_path)),
                          ("Parent fGDB", get_fc_gdb_path(fc_path)),
                          ("Geometry Type", get_fc_geometry_type(fc_path)),
                          ("CRS Name", get_crs_name(fc_path)),
                          ("CRS EPSG WKID", get_crs_wkid(fc_path)),
                          ("CRS Type", get_crs_type(fc_path)),
                          ("CRS Units", get_crs_units(fc_path))]

    if logging.getLevelName(log.getEffectiveLevel()) == "INFO":
        log.info("FC Properties List:")
        for item in fc_properties_list:
            log.info("{:18}: {}".format(item[0],item[1]))

    return fc_properties_list


# -----------------------------------------
# get_fc_gdb_name
# -----------------------------------------


def get_fc_gdb_path(fc_path):
    """
    :pre the fc_path is a valid fGDB path
    :returns the path of the parent file geodatabase
    """
    gdb_path = fc_path.split(".gdb", 1)[0] + ".gdb"
    log.debug("get_fc_gdb_path returning: " + gdb_path)
    return gdb_path


# -----------------------------------------
# get name
# -----------------------------------------

def get_fc_name(fc_path):
    """
    :returns the name of a feature class from the feature class object
    """
    base_name = arcpy.Describe(fc_path).baseName
    log.debug("get_crs_name returning: " + base_name)
    return base_name


# -----------------------------------------
# get geometry type
# -----------------------------------------

def get_fc_geometry_type(fc_path):
    """
    :returns the geometry type of a feature class
             usually in the set {MultiPatch, Multipoint,Point,Polyline,Polygon}
    """
    geometry_type = arcpy.Describe(fc_path).shapeType
    log.debug("get_fc_geometry_type returning: " + geometry_type)
    return geometry_type


# -----------------------------------------
# get CRS functions
# -----------------------------------------

def get_crs_name(fc_path):
    """
    :return the coordinate system name of a feature class
    """
    sr = arcpy.Describe(fc_path).spatialReference
    log.debug("get_crs_name returning: " + sr.name)
    return sr.name


def get_crs_wkid(fc_path):
    """
    :returns the coordinate system EPSG WKID of a feature class
    """
    sr = arcpy.Describe(fc_path).spatialReference
    log.debug("get_crs_wkid returning: " + str(sr.factoryCode))
    return sr.factoryCode


def get_crs_type(fc_path):
    """
    :return the type of coordiate system of a feature class
             usually in the set {geographic, projected}
    """
    sr = arcpy.Describe(fc_path).spatialReference
    log.debug("get_crs_type returning: " + str(sr.type))
    return sr.type


def get_crs_units(fc_path):
    """
    :return the geometry units of a feature class
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
