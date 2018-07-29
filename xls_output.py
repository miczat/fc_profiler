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
    sheet1 = book.add_sheet("fc_properties")
    log.info("Writing " + xls_path)
    try:
        book.save(xls_path)
    except Error as e:
        log.error("Error writing xls")
        raise

    # if all went well
    return True
