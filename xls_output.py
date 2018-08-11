import xlwt
import logging
import datetime
log = logging.getLogger()

# ---------------------------------------------------------------------------------
# write_fc_profile
# writes the feature class using the xlwt library available ArcGIS 10.3.
# xlwt cannot edit existing xls files, so all writing must be done in a single pass
# ---------------------------------------------------------------------------------

def write_fc_profile(fc_property_data,
                     fc_structure,
                     xls_path):
    """"
    :param fc_property_data: a list of (key, value) pairs
    :type fc_property_data: list of tuples

    :param fc_structure: a tuple of (headings, data)
    :type fc_structure: tuple of (namedtuple,  list of namedtuples)

    :param xls_path: the full path to the output xls file
    :type   xls_path: basestring

    """

    # ----------------------------------
    # define styles
    # ----------------------------------
    title_style = xlwt.easyxf('font:name Century Gothic, '
                              'bold on, height 320;'
                              'align: vert centre, horz left;')

    subtitle_style = xlwt.easyxf('font:name Century Gothic, '
                                 'bold off, italic on, height 160;'
                                 'align: vert centre, horz left;')

    xlwt.add_palette_colour("custom_colour", 0x21)

    heading_style = xlwt.easyxf('font:name Century Gothic,bold on, color gray50;'
                                'borders: bottom_color gray25, bottom thin;'
                                'align: vert centre, horz left;'
                                'pattern: pattern solid, fore_colour custom_colour')

    data_style = xlwt.easyxf('font:name Consolas, '
                             'bold off; '
                             'align: vert centre, horz left')

    # ----------------------------------
    # Write FC properties
    # ----------------------------------
    book = xlwt.Workbook()
    sheet1 = book.add_sheet("fc_properties", cell_overwrite_ok=True)

    book.set_colour_RGB(0x21, 250, 250, 250)  # light slate grey

    log.debug("Setting columm widths")
    heading_column = sheet1.col(1)
    heading_column.width = 256 * 18  # approx 20 chars

    data_column = sheet1.col(2)
    data_column.width = 256 * 80  # approx 20 chars wide

    # write title
    log.debug("writing title")
    title = "Feature Class Profile"
    sheet1.write(1, 1, title, title_style)

    # write subtitle title
    log.debug("Writing subtitle")
    now = datetime.datetime.now()
    now = now.replace(second=int(round(now.second, 0)), microsecond=0)
    now = now.strftime("%d-%m-%Y %H:%M:%S")
    subtitle = "Generated on " + now
    sheet1.write(2, 1, subtitle, subtitle_style)

    # write fc_property_data
    log.debug("Writing fc_property_data")
    row_num = 4  # start on row 5
    for record in fc_property_data:
        sheet1.write(row_num, 1, record[0], heading_style)  # row, column, value
        sheet1.write(row_num, 2, record[1], data_style)  # row, column, value
        row_num = row_num + 1

    # ----------------------------------
    # FC Structure / field properties
    # ----------------------------------

    sheet2 = book.add_sheet("fc_structure", cell_overwrite_ok=True)

    # write title
    log.debug("writing sheet 2 title")
    title = "Feature Class Structure"
    sheet2.write(1, 1, title, title_style)


    # upack fc_structure
    headings = fc_structure[0]
    log.debug(str(len(headings)) + " headings")

    log.debug("Headings:")
    log.debug("--------------------------------")
    for heading in headings:
        log.debug(heading),
    log.debug("--------------------------------")

    row = 4
    col = 1
    for heading in headings:
        sheet2.write(row, col, heading, heading_style)
        col = col + 1

    rows = fc_structure[1]
    log.debug("fields type = " + str(type(rows)))
    log.debug(str(len(rows)) + " records in fc_structure")

    for row in rows:
        log.debug("")
        log.debug("Name      = " + row.field_name)
        log.debug("Width     = " + str(row.field_name_width))
        log.debug("Alias     = " + row.field_alias)
        log.debug("Type      = " + row.field_type)
        log.debug("Precision = " + str(row.field_precision))
        log.debug("Scale     = " + str(row.field_scale))
        log.debug("Length    = " + str(row.field_length))
        log.debug("Nullable  = " + str(row.field_is_nullable))
        log.debug("Required  = " + str(row.field_is_required))
        log.debug("Editable  = " + str(row.field_is_editable))

    # TODO - write this to XLS

    # ----------------------------------
    # save
    # ----------------------------------

    log.debug("Saving " + xls_path)
    try:
        book.save(xls_path)
    except Exception as e:
        log.error("Error writing xls")
        raise

    # if all went well
    return True


def write_fc_structure(fc_structure, xls_path):
    """"
    :param fc_structure: a tuple of (headings, data)
    :type fc_structure: tuple of (namedtuple,  list of namedtuples)

    :param xls_path: the full path to the output xls file
    :type   xls_path: basestring

    """

    # upack fc_structure
    headings = fc_structure[0]
    log.debug(str(len(headings)) + " headings")

    log.debug("Headings:")
    log.debug("--------------------------------")
    for heading in headings:
        log.debug(heading),
    log.debug("--------------------------------")

    rows = fc_structure[1]
    log.debug("fields type = " + str(type(rows)))
    log.debug(str(len(rows)) + " records in fc_structure")

    for row in rows:
        log.debug("")
        log.debug("Name      = " + row.field_name)
        log.debug("Width     = " + str(row.field_name_width))
        log.debug("Alias     = " + row.field_alias)
        log.debug("Type      = " + row.field_type)
        log.debug("Precision = " + str(row.field_precision))
        log.debug("Scale     = " + str(row.field_scale))
        log.debug("Length    = " + str(row.field_length))
        log.debug("Nullable  = " + str(row.field_is_nullable))
        log.debug("Required  = " + str(row.field_is_required))
        log.debug("Editable  = " + str(row.field_is_editable))

  # TODO - write this to XLS
