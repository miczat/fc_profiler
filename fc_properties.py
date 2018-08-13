import collections
import logging
import arcpy
log = logging.getLogger()


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
                          ("Has m values?", str(is_m_enabled(fc_path))),
                          ("Total Records", '{:,}'.format(get_fc_total_record_count(fc_path))),
                          ("Total Fields",str(get_fc_field_count(fc_path)))
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


# -----------------------------------------
# get_fc_total_record_count
#     no where clause, returns total rows
# -----------------------------------------

def get_fc_total_record_count(fc_path):
    """
    :param fc_path: fully qualified path to a feature class
    :type fc_path: basestring

    :return count: the record count for a feature class
    :rtype result: int
    """

    table_view = "count_rec_tblview"
    arcpy.Delete_management("count_rec_tblview")  #just in case it exists
    arcpy.MakeTableView_management(in_table=fc_path,
                                   out_view=table_view)
    count = int(arcpy.GetCount_management(table_view).getOutput(0))
    arcpy.Delete_management(table_view)
    log.debug("get_fc_record_count returning: " + str(count))

    return count


# -----------------------------------------
# get_fc_field_count
# -----------------------------------------

def get_fc_field_count(fc_path):
    """
    :param fc_path: fully qualified path to a feature class
    :type fc_path: basestring

    :return count: the field count for a feature class
    :rtype result: int
    """

    fields = arcpy.ListFields(dataset=fc_path, field_type="All")
    count = len(fields)
    log.debug("get_fc_field_count returning: " + str(count))
    return count


# -----------------------------------------
# get_structure
# -----------------------------------------

def get_fc_structure(fc_path):
    """
    :param fc_path: fully qualified path to a feature class
    :type fc_path: basestring

    :return (headins, data)
    :rtype (namedtuple, list of namedtuples)
    """

    # define the named tuple
    Row = collections.namedtuple("Row", ["field_name",
                                         "field_name_len",
                                         "field_alias",
                                         "field_type",
                                         "field_length",
                                         "field_precision",
                                         "field_scale",
                                         "field_is_nullable",
                                         "field_is_required",
                                         "field_is_editable",
                                         "field_domain"
                                         ]
                                 )

    # create headings row
    heading_row = Row(field_name="Name",
                      field_name_len="Name field len",
                      field_alias="Alias",
                      field_type="Type",
                      field_length="Length",
                      field_precision="Precision",
                      field_scale="Scale",
                      field_is_nullable="is nullable?",
                      field_is_required="is required?",
                      field_is_editable="is editable?",
                      field_domain="Domain Name"
                      )

    log.debug('Getting structure from the feature class')
    data_rows = []
    field_list = arcpy.ListFields(dataset=fc_path, field_type="All")
    for field in field_list:
        data_rows.append(Row(field_name=field.baseName,
                             field_name_len=len(field.baseName),
                             field_alias=field.aliasName,
                             field_type=field.type,
                             field_length=field.length,
                             field_precision=field.precision,
                             field_scale=field.scale,
                             field_is_nullable=str(field.isNullable),
                             field_is_required=str(field.required),
                             field_is_editable=str(field.editable),
                             field_domain=field.domain
                             )
                         )

    return heading_row, data_rows
