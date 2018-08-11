# -------------------------------------------
# driver for developing xls_output
# -------------------------------------------
from xls_output import write_fc_properties
import logging


# simple logger setup
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


# driver

data = [("Feature Class", "GDA94_polyline"),
       ("Parent fGDB", r"C:\tmp\fc_profiler_testdata\fc_profiler_test.gdb"),
       ("Geometry Type", "Polyline"),
       ("CRS Name", "GCS_GDA_1994"),
       ("CRS EPSG WKID", 4283),
       ("CRS Type", "Geographic"),
       ("CRS Units", "Degree"),
       ("Has Z values?",str(True)),
       ("Has m values?", str(False)),
       ("Total Records", '{:,}'.format(5000000000)),
       ("Total Fields", 256)
       ]

xls_path = r"C:\tmp\dev.xls"

print(write_fc_properties(data, xls_path))



