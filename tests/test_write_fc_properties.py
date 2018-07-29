from unittest import TestCase
from xls_output import write_fc_properties
import os
import tempfile


# self.assertEqual( <expected>, <actual>)


class TestWrite_fc_properties(TestCase):

    def setUp(self):
        """make sure the test xls does not exist from a previous test"""
        # C:\Users\micza\AppData\Local\Temp
        tf = tempfile.NamedTemporaryFile().name
        self.xls_path = os.path.join(tf + ".xls")
        if os.path.exists(self.xls_path):
            os.remove(self.xls_path)

    def test_write_fc_properties_normal(self):

        """test normal writing of the xls"""
        # test data
        fc_name = "test_fc"
        fc_gdb_path = r"c:\tmp\fc_profiler_testdata\fc_profiler_test.gdb"
        fc_geometry = "Point"
        crs_name = "GCS_WGS_1984"
        crs_wkid = 4326
        crs_type = "Geographic"
        crs_units = "Degree"


        fc_properties_list = [("Feature Class", fc_name),
                              ("Parent fGDB", fc_gdb_path),
                              ("Geometry Type",fc_geometry),
                              ("CRS Name", crs_name),
                              ("CRS EPSG WKID", crs_wkid),
                              ("CRS Type", crs_type),
                              ("CRS Units", crs_units)]

        # call function being tested
        result = write_fc_properties(fc_properties_list, self.xls_path)

        print("tmp file location = " + self.xls_path)

        # Fail if the function retuens false or the outpur file is not found
        if result is False or not os.path.exists(self.xls_path):
            self.fail()

    def tearDown(self):
        #delete the temp file
        if os.path.exists(self.xls_path):
            print("deleting temp xls file")
            os.remove(self.xls_path)