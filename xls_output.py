import xlwt
import logging
import datetime
log = logging.getLogger()

# -----------------------------------------
# Write to excel
# -----------------------------------------

def write_fc_properties(data, xls_path):
    """"writes the feature class properties to a page in an XLS
        :param data - a list of key, value pairs as a tuples [ (x,y), (x,y), ...]
        :param xls_path - the full path of the xls file to write
        pre: the xls file can be crated (user has write permission to folder)
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

    heading_style = xlwt.easyxf('font:name Century Gothic, '
                                'bold on;'
                                'align: vert centre, horz left;')

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

