from unittest import TestCase
import collections
from xls_output import write_fc_profile
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

    def test_write_fc_properties_to_xls_check_return_value(self):
        # test fc properties data
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

        # test fc structure data
        Row = collections.namedtuple("Row", ["field_name",
                                             "field_name_len",
                                             "field_alias",
                                             "field_type",
                                             "field_length",
                                             "field_precision",
                                             "field_scale",
                                             "field_is_nullable",
                                             "field_is_required",
                                             "field_is_editable",
                                             "field_domain"
                                             ]
                                     )

        # create headings row
        heading_row = Row(field_name="Name",
                          field_name_len="Name field len",
                          field_alias="Alias",
                          field_type="Type",
                          field_length="Length",
                          field_precision="Precision",
                          field_scale="Scale",
                          field_is_nullable="is nullable?",
                          field_is_required="is required?",
                          field_is_editable="is editable?",
                          field_domain="Domain Name"
                          )

        # create a data row
        data_rows = []
        data_rows.append(Row(field_name="foo",
                             field_name_len=3,
                             field_alias="foo alias",
                             field_type="String",
                             field_length=10,
                             field_precision=0,
                             field_scale=0,
                             field_is_nullable="True",
                             field_is_required="False",
                             field_is_editable="True",
                             field_domain="some domain name"
                             )
                        )

        fc_structure = (heading_row, data_rows)

        # the called function returns true
        self.assertTrue(write_fc_profile(fc_properties_list,
                                         fc_structure,
                                         self.xls_path))


    def test_write_fc_properties_check_xls_file_written(self):
        """test normal writing of the xls"""
        # test fc properties data
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

        # test fc structure data
        Row = collections.namedtuple("Row", ["field_name",
                                             "field_name_len",
                                             "field_alias",
                                             "field_type",
                                             "field_length",
                                             "field_precision",
                                             "field_scale",
                                             "field_is_nullable",
                                             "field_is_required",
                                             "field_is_editable",
                                             "field_domain"])

        # create headings row
        heading_row = Row(field_name="Name",
                          field_name_len="Name field len",
                          field_alias="Alias",
                          field_type="Type",
                          field_length="Length",
                          field_precision="Precision",
                          field_scale="Scale",
                          field_is_nullable="is nullable?",
                          field_is_required="is required?",
                          field_is_editable="is editable?",
                          field_domain="domain")

        # create a data row
        data_rows = []
        data_rows.append(Row(field_name="foo",
                             field_name_len=3,
                             field_alias="foo alias",
                             field_type="String",
                             field_length=10,
                             field_precision=0,
                             field_scale=0,
                             field_is_nullable="True",
                             field_is_required="False",
                             field_is_editable="True",
                             field_domain="some domain"
                             )
                         )

        fc_structure = (heading_row, data_rows)

        # call function being tested
        write_fc_profile(fc_properties_list,
                         fc_structure,
                         self.xls_path)

        self.assertTrue(os.path.exists(self.xls_path))

    def tearDown(self):
        if os.path.exists(self.xls_path):
            print("deleting temp file     " + self.xls_path)
            os.remove(self.xls_path)
