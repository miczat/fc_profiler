from unittest import TestCase
from fc_properties import get_fc_gdb_path
from fc_properties import get_fc_name
from fc_properties import get_fc_geometry_type
from fc_properties import is_z_enabled
from fc_properties import is_m_enabled
from fc_properties import get_fc_total_record_count
from fc_properties import get_fc_field_count
import os

# self.assertEqual( <expected>, <actual>)

fgdb = r"C:\tmp\fc_profiler_testdata\fc_profiler_test.gdb"


class Testget_fc_gdb_path(TestCase):

    def test_get_fc_gdb_path_normal(self):
        fc_path = r"c:\tmp\test.gdb\featureclass"
        self.assertEqual(r"c:\tmp\test.gdb", get_fc_gdb_path(fc_path))


class Testget_fc_name(TestCase):

    def test_get_fc_name_GDA94_GA_Lambert(self):
        fc = "GDA94_GA_Lambert_point"
        fc_path = os.path.join(fgdb, fc)
        self.assertEqual(fc, get_fc_name(fc_path))

    def test_get_fc_name_GDA94_LL(self):
        fc = "GDA94_point"
        fc_path = os.path.join(fgdb, fc)
        self.assertEqual(fc, get_fc_name(fc_path))

    def test_get_fc_name_WGS84_LL(self):
        fc = "WGS84_point"
        fc_path = os.path.join(fgdb, fc)
        self.assertEqual(fc, get_fc_name(fc_path))

    def test_get_fc_name_WGS_1984_Web_Mercator(self):
        fc = "Web_Mercator_point"
        fc_path = os.path.join(fgdb, fc)
        self.assertEqual(fc, get_fc_name(fc_path))

    def test_get_fc_name_MGAZ56(self):
        fc = "MGAZ56_point"
        fc_path = os.path.join(fgdb, fc)
        self.assertEqual(fc, get_fc_name(fc_path))

    def test_get_fc_name_NO_CRS(self):
        fc = "NO_CRS_point"
        fc_path = os.path.join(fgdb, fc)
        self.assertEqual(fc, get_fc_name(fc_path))


class Testget_fc_geometry_type(TestCase):

    def test_get_fc_geometry_type_point(self):
        fc = "GDA94_point"
        fc_path = os.path.join(fgdb, fc)
        self.assertEqual("Point", get_fc_geometry_type(fc_path))

    # not available in ArcGIS version 10.3
    # def test_get_fc_geometry_type_multipatch(self):
    #     fc = "GDA94_multipatch"
    #     fc_path = os.path.join(fgdb, fc)
    #     self.assertEqual("MultiPatch", get_fc_geometry_type(fc_path))

    def test_get_fc_geometry_type_multipoint(self):
        fc = "GDA94_multipoint"
        fc_path = os.path.join(fgdb, fc)
        self.assertEqual("Multipoint", get_fc_geometry_type(fc_path))

    def test_get_fc_geometry_type_polygon(self):
        fc = "GDA94_polygon"
        fc_path = os.path.join(fgdb, fc)
        self.assertEqual("Polygon", get_fc_geometry_type(fc_path))

    def test_get_fc_geometry_type_polyline(self):
        fc = "GDA94_polyline"
        fc_path = os.path.join(fgdb, fc)
        self.assertEqual("Polyline", get_fc_geometry_type(fc_path))


class Testget_fc_Z_values(TestCase):

    def test_is_fc_Z_enabled_does_have_z(self):
        fc = "MGAZ56_has_Z_polyline"
        fc_path = os.path.join(fgdb, fc)
        self.assertTrue(is_z_enabled(fc_path))

    def test_is_fc_Z_enabled_has_z_and_m(self):
        fc = "MGAZ56_has_Z_M_polyline"
        fc_path = os.path.join(fgdb, fc)
        self.assertTrue(is_z_enabled(fc_path))

    def test_is_fc_z_enabled_does_not_have_z(self):
        fc = "GDA94_point"
        fc_path = os.path.join(fgdb, fc)
        self.assertFalse(is_z_enabled(fc_path))


class Testget_fc_M_values(TestCase):

    def test_is_fc_M_enabled_does_have_m(self):
        fc = "MGAZ56_has_M_polyline"
        fc_path = os.path.join(fgdb, fc)
        self.assertTrue(is_m_enabled(fc_path))

    def test_is_fc_M_enabled_has_z_and_m(self):
        fc = "MGAZ56_has_Z_M_polyline"
        fc_path = os.path.join(fgdb, fc)
        self.assertTrue(is_m_enabled(fc_path))

    def test_is_fc_M_enabled_does_not_have_m(self):
        fc = "GDA94_point"
        fc_path = os.path.join(fgdb, fc)
        self.assertFalse(is_m_enabled(fc_path))


class Testget_fc_record_count(TestCase):

    def test_is_fc_zero_records(self):
        fc = "GDA94_point"
        fc_path = os.path.join(fgdb, fc)
        self.assertEquals(0, get_fc_total_record_count(fc_path))

    def test_is_fc_602_records(self):
        fc = "MGAZ56_602_rec_polyline"
        fc_path = os.path.join(fgdb, fc)
        self.assertEquals(602, get_fc_total_record_count(fc_path))

    def test_is_fc_M_5_million_records(self):
        fc = "MGAZ56_5_million_rec_polygon"
        fc_path = os.path.join(fgdb, fc)
        self.assertEquals(5000000, get_fc_total_record_count(fc_path))


class Testget_fc_field_count(TestCase):

    def test_is_fc_two_records(self):
        # two fields is the minimum expected in a new feature class
        fc = "GDA94_GA_Lambert_point"
        fc_path = os.path.join(fgdb, fc)
        self.assertEquals(2, get_fc_field_count(fc_path))

    def test_is_fc_four_records(self):
        fc = "MGAZ56_5_million_rec_polygon"
        fc_path = os.path.join(fgdb, fc)
        self.assertEquals(4, get_fc_field_count(fc_path))
