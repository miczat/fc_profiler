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

    book = xlwt.Workbook()

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

    data_style_aligned_left = xlwt.easyxf('font:name Consolas, '
                                          'bold off; '
                                          'align: vert centre, horz left')

    data_style_aligned_centre = xlwt.easyxf('font:name Consolas, '
                                            'bold off; '
                                            'align: vert centre, horz centre')

    book.set_colour_RGB(0x21, 250, 250, 250)  # light slate grey

    # ----------------------------------
    # Write FC properties
    # ----------------------------------
    log.info("writing sheet_fc_properties")
    sheet_fc_properties = book.add_sheet("fc_properties", cell_overwrite_ok=True)

    # set column widths
    sheet_fc_properties.col(1).width = 256 * 18  # headings
    sheet_fc_properties.col(2).width = 256 * 80  # properties

    # write title
    title = "Feature Class Properties"
    sheet_fc_properties.write(1, 1, title, title_style)

    # write sub-title
    now = datetime.datetime.now()
    now = now.replace(second=int(round(now.second, 0)), microsecond=0)
    now = now.strftime("%d-%m-%Y %H:%M:%S")
    subtitle = "Generated on " + now
    sheet_fc_properties.write(2, 1, subtitle, subtitle_style)

    # write headings and data
    log.debug("Writing fc_property_data")
    row_num = 4  # start on row 5
    for record in fc_property_data:
        sheet_fc_properties.write(row_num, 1, record[0], heading_style)  # row, column, value
        sheet_fc_properties.write(row_num, 2, record[1], data_style_aligned_left)  # row, column, value
        row_num = row_num + 1

    # ----------------------------------
    # FC Structure / field properties
    # ----------------------------------
    log.info("writing sheet_fc_structure")
    sheet_fc_structure = book.add_sheet("fc_structure", cell_overwrite_ok=True)

    # set column widths
    sheet_fc_structure.col(1).width = 256 * 35   # name
    sheet_fc_structure.col(2).width = 256 * 16   # name field len
    sheet_fc_structure.col(3).width = 256 * 30   # alias
    sheet_fc_structure.col(4).width = 256 * 14   # type
    sheet_fc_structure.col(5).width = 256 * 8    # length
    sheet_fc_structure.col(6).width = 256 * 10   # precision
    sheet_fc_structure.col(7).width = 256 * 7    # scale
    sheet_fc_structure.col(8).width = 256 * 12   # is nullable
    sheet_fc_structure.col(9).width = 256 * 12   # is required
    sheet_fc_structure.col(10).width = 256 * 12  # is editable
    sheet_fc_structure.col(11).width = 256 * 30  # domain

    # write title
    title = "Feature Class Structure"
    sheet_fc_structure.write(1, 1, title, title_style)

    # write headings
    headings = fc_structure[0]
    log.debug(str(len(headings)) + " headings")
    row = 4  # heading row
    col = 1  # starting column
    for heading in headings:
        sheet_fc_structure.write(row, col, heading, heading_style)
        col = col + 1

    # write data
    structure_records = fc_structure[1]
    log.debug(str(len(structure_records)) + " records in fc_structure")
    row = 5  # starting row
    col = 1  # starting column
    for record in structure_records:
        sheet_fc_structure.write(row, col, record.field_name, data_style_aligned_left)
        sheet_fc_structure.write(row, col+1, record.field_name_len, data_style_aligned_centre)
        sheet_fc_structure.write(row, col+2, record.field_alias, data_style_aligned_left)
        sheet_fc_structure.write(row, col+3, record.field_type, data_style_aligned_left)
        sheet_fc_structure.write(row, col+4, record.field_length, data_style_aligned_centre)
        sheet_fc_structure.write(row, col+5, record.field_precision, data_style_aligned_centre)
        sheet_fc_structure.write(row, col+6, record.field_scale, data_style_aligned_centre)
        sheet_fc_structure.write(row, col+7, record.field_is_nullable, data_style_aligned_centre)
        sheet_fc_structure.write(row, col+8, record.field_is_required, data_style_aligned_centre)
        sheet_fc_structure.write(row, col+9, record.field_is_editable, data_style_aligned_centre)
        sheet_fc_structure.write(row, col+10, record.field_domain, data_style_aligned_left)
        row = row + 1

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


