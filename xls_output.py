import xlwt
import logging
log = logging.getLogger()

# -----------------------------------------
# Write to excel
# -----------------------------------------

def write_fc_properties(data, xls_path):
    """"writes the feature class properties to a page in an XLS
        pre: the xls file can be crated (user has write permission to folder)
    """

    book = xlwt.Workbook()
    sheet = book.add_sheet("fc_properties")

    cols = ["A", "B"]

    row_num = 1
    for record in data:
        sheet.write(row_num, 1, record[0])  # row, column, value
        sheet.write(row_num, 2, record[1])  # row, column, value
        row_num = row_num + 1

    log.info("saving " + xls_path)
    try:
        book.save(xls_path)
    except Error as e:
        log.error("Error writing xls")
        raise

    # if all went well
    return True

