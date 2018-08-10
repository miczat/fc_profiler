import arcpy
import logging
log = logging.getLogger()


# -----------------------------------------------------------------
# get_fc_properties
#    this is the main function that controls the profile generation
#    pre: the input feature class exists
#    pre: the output xls is somewhere that can be writen too
#    post: a xls file will be written
# -----------------------------------------------------------------

def get_fc_properties(fc_path):
    """
    :param fc_path: fully qualified path to a feature class
    :type fc_path: basestring
    """

    # generate the list of feature class properties
    fc_properties_list = [("Feature Class", get_fc_name(fc_path)),
                          ("Parent fGDB", get_fc_gdb_path(fc_path)),
                          ("Geometry Type", get_fc_geometry_type(fc_path)),
                          ("CRS Name", get_crs_name(fc_path)),
                          ("CRS EPSG WKID", get_crs_wkid(fc_path)),
                          ("CRS Type", get_crs_type(fc_path)),
                          ("CRS Units", get_crs_units(fc_path)),
                          ("Has Z values?", str(is_z_enabled(fc_path))),
                          ("Has m values?", str(is_m_enabled(fc_path)))
                          ]

    if logging.getLevelName(log.getEffectiveLevel()) == "INFO":
        log.info("FC Properties List:")
        for item in fc_properties_list:
            log.info("{:18}: {}".format(item[0],item[1]))

    return fc_properties_list


# -----------------------------------------
# get_fc_gdb_name
#     :pre the fc_path is a valid fGDB path
# -----------------------------------------


def get_fc_gdb_path(fc_path):
    """
    :param fc_path: fully qualified path to a feature class
    :type fc_path: basestring

    :returns gdb_path: the path of the parent file geodatabase
    :rtype basestring
    """
    gdb_path = fc_path.split(".gdb", 1)[0] + ".gdb"
    log.debug("get_fc_gdb_path returning: " + gdb_path)
    return gdb_path


# ------------------------------------------------------
# get name
#    given a full path to a FC, retyurn just the FC name
# ------------------------------------------------------

def get_fc_name(fc_path):
    """
    :param fc_path: fully qualified path to a feature class
    :type fc_path: basestring

    :returns base_name: the feature class name
    :rtype basestring
    """
    base_name = arcpy.Describe(fc_path).baseName
    log.debug("get_fc_name returning: " + base_name)
    return base_name


# ----------------------------------------------------------------------------
# get geometry type
#    post:  usually in the set {MultiPatch, Multipoint,Point,Polyline,Polygon}
# ----------------------------------------------------------------------------

def get_fc_geometry_type(fc_path):
    """
    :param fc_path: fully qualified path to a feature class
    :type fc_path: basestring

    :returns geometry_type: the geometry type of a feature class
    :rtype geometry_type: basestring

    """
    geometry_type = arcpy.Describe(fc_path).shapeType
    log.debug("get_fc_geometry_type returning: " + geometry_type)
    return geometry_type


# -----------------------------------------
# get CRS functions
# -----------------------------------------

def get_crs_name(fc_path):
    """
    :param fc_path: fully qualified path to a feature class
    :type fc_path: basestring

    :returns sr.name: the coordinate system name
    :rtype sr.name: basestring

    """
    sr = arcpy.Describe(fc_path).spatialReference
    log.debug("get_crs_name returning: " + sr.name)
    return sr.name


def get_crs_wkid(fc_path):
    """
    :param fc_path: fully qualified path to a feature class
    :type fc_path: basestring

    :returns sr.factoryCode: the coordinate system EPSG WKID
    :rtype sr.factoryCode: int
    """
    sr = arcpy.Describe(fc_path).spatialReference
    log.debug("get_crs_wkid returning: " + str(sr.factoryCode))
    return sr.factoryCode


# post: usually in the set {geographic, projected}
def get_crs_type(fc_path):
    """
    :param fc_path: fully qualified path to a feature class
    :type fc_path: basestring

    :returns sr.type: the coordinate system type
    :rtype sr.type: basestring
    """
    sr = arcpy.Describe(fc_path).spatialReference
    log.debug("get_crs_type returning: " + str(sr.type))
    return sr.type


# post: usually in the set {degrees, meters}
def get_crs_units(fc_path):
    """
    :param fc_path: fully qualified path to a feature class
    :type fc_path: basestring

    :return units: the geometry units of a feature class
    :rtype units: basestring
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


# -----------------------------------------
# is_z_enabled
# -----------------------------------------

def is_z_enabled(fc_path):
    """
    :param fc_path: fully qualified path to a feature class
    :type fc_path: basestring

    :return result: True if the feature class has Z values enabled
    :rtype result: bool
    """
    result = arcpy.Describe(fc_path).hasZ
    log.debug("is_z_enabled returning: " + str(result))
    return result


# -----------------------------------------
# is_m_enabled
# -----------------------------------------

def is_m_enabled(fc_path):
    """
    :param fc_path: fully qualified path to a feature class
    :type fc_path: basestring

    :return result: True if the feature class has M values enabled
    :rtype result: bool
    """
    result = arcpy.Describe(fc_path).hasM
    log.debug("is_m_enabled returning: " + str(result))
    return result
