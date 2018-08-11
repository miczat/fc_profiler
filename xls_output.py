import xlwt
import logging
import datetime
log = logging.getLogger()

# ---------------------------------------------------------
# write_fc_properties
# writes the feature class properties to a page in an XLS
#     pre: the user has write permission to the output path
# ---------------------------------------------------------

def write_fc_properties(data, xls_path):
    """"
    :param data: a list of (key, value) pairs
    :type data: list of tuples

    :param xls_path: the full path to the output xls file
    :type   xls_path: basestring

    """

    book = xlwt.Workbook()
    sheet = book.add_sheet("fc_properties", cell_overwrite_ok=True)
    cols = ["A", "B"]

    # define styles
    title_style = xlwt.easyxf('font:name Century Gothic, '
                              'bold on, height 320;'
                              'align: vert centre, horz left;')

    subtitle_style = xlwt.easyxf('font:name Century Gothic, '
                                 'bold off, italic on, height 160;'
                                 'align: vert centre, horz left;')

    xlwt.add_palette_colour("custom_colour", 0x21)
    book.set_colour_RGB(0x21, 192, 192, 192)
    heading_style = xlwt.easyxf('font:name Century Gothic, '
                                'bold on;'
                                'align: vert centre, horz left;'
                                'pattern: pattern solid, fore_colour custom_colour')

    data_style = xlwt.easyxf('font:name Consolas, '
                             'bold off; '
                             'align: vert centre, horz left')


    log.debug("Setting columm widths")
    heading_column = sheet.col(1)
    heading_column.width = 256 * 18  # approx 20 chars

    data_column = sheet.col(2)
    data_column.width = 256 * 80  # approx 20 chars wide

    # write title
    log.debug("writing title")
    title = "Feature Class Profile"
    sheet.write(1, 1, title, title_style)

    # write subtitle title
    log.debug("Writing subtitle")
    now = datetime.datetime.now()
    now = now.replace(second=int(round(now.second, 0)), microsecond=0)
    now = now.strftime("%d-%m-%Y %H:%M:%S")
    subtitle = "Generated on " + now
    sheet.write(2, 1, subtitle, subtitle_style)

    # write data
    log.debug("Writing data")
    row_num = 4  # start on row 5
    for record in data:
        sheet.write(row_num, 1, record[0], heading_style)  # row, column, value
        sheet.write(row_num, 2, record[1], data_style)  # row, column, value
        row_num = row_num + 1

    # save
    log.debug("Saving " + xls_path)
    try:
        book.save(xls_path)
    except Exception as e:
        log.error("Error writing xls")
        raise

    # if all went well
    return True



def write_fc_structure(data, xls_path):
    """"
    :param data: a tuple of (headings, data)
    :type data: tuple of (namedtuple,  list of namedtuples)

    :param xls_path: the full path to the output xls file
    :type   xls_path: basestring

    """

    # upack data
    headings = data[0]
    log.debug(str(len(headings)) + " headings")

    log.debug("Headings:")
    log.debug("--------------------------------")
    for heading in headings:
        log.debug(heading),
    log.debug("--------------------------------")

    rows = data[1]
    log.debug("fields type = " + str(type(rows)))
    log.debug(str(len(rows)) + " records in data")

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
