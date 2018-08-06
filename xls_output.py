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

    # write data
    log.debug("writing " + xls_path)

    heading_style = xlwt.easyxf('font:name Century Gothic, bold on')
    data_style = xlwt.easyxf('font:name Consolas')

    row_num = 1
    for record in data:
        sheet.write(row_num, 1, record[0], heading_style)  # row, column, value
        sheet.write(row_num, 2, record[1], data_style)  # row, column, value
        row_num = row_num + 1




    # save
    log.debug("saving " + xls_path)
    try:
        book.save(xls_path)
    except Error as e:
        log.error("Error writing xls")
        raise

    # if all went well
    return True

