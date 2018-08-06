import xlwt
import logging
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
    sheet = book.add_sheet("fc_properties")
    cols = ["A", "B"]

    # define styles
    title_style = xlwt.easyxf('font:name Century Gothic, bold on, height 320;'
                                'align: vert centre, horz left;')

    heading_style = xlwt.easyxf('font:name Century Gothic, bold on;'
                                'align: vert centre, horz left;')
    data_style = xlwt.easyxf('font:name Consolas bold off; align: vert centre, horz left')

    log.debug("setting columm widths ")
    heading_column = sheet.col(1)
    heading_column.width = 256 * 18  # approx 20 chars wide

    data_column = sheet.col(2)
    data_column.width = 256 * 80  # approx 20 chars wide

    # write title
    log.debug("writing title")
    sheet.write(1, 1, "Feature Class Profile", title_style)

    # write data
    log.debug("writing data")
    row_num = 3  # start on row 4
    for record in data:
        sheet.write(row_num, 1, record[0], heading_style)  # row, column, value
        sheet.write(row_num, 2, record[1], data_style)  # row, column, value
        row_num = row_num + 1


    # save
    log.debug("saving " + xls_path)
    try:
        book.save(xls_path)
    except Exception as e:
        log.error("Error writing xls")
        raise

    # if all went well
    return True

