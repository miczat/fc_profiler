from unittest import TestCase
from fc_properties import get_fc_name
from fc_properties import get_fc_geometry_type
import os

# self.assertEqual( <expected>, <actual>)

fgdb = r"C:\tmp\fc_profiler_testdata\fc_profiler_test.gdb"


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

    def test_get_fc_geometry_type_multipatch(self):
        fc = "GDA94_multipatch"
        fc_path = os.path.join(fgdb, fc)
        self.assertEqual("MultiPatch", get_fc_geometry_type(fc_path))

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