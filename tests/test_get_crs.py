from unittest import TestCase
from fc_properties import get_crs_name
from fc_properties import get_crs_wkid
from fc_properties import get_crs_type
import os

# self.assertEqual( <expected>, <actual>)


class TestGet_crs_name(TestCase):

    def setUp(self):
        self.fgdb = r"C:\tmp\fc_profiler_testdata\fc_profiler_test.gdb"

    def test_get_crs_name_GDA94_GA_Lambert(self):
        fc = "GDA94_GA_Lambert_point"
        fc_path = os.path.join(self.fgdb, fc)
        self.assertEqual("GDA_1994_Geoscience_Australia_Lambert",
                         get_crs_name(fc_path))

    def test_get_crs_name_GDA94_LL(self):
        fc = "GDA94_point"
        fc_path = os.path.join(self.fgdb, fc)
        self.assertEqual("GCS_GDA_1994", get_crs_name(fc_path))

    def test_get_crs_name_WGS84_LL(self):
        fc = "WGS84_point"
        fc_path = os.path.join(self.fgdb, fc)
        self.assertEqual("GCS_WGS_1984",get_crs_name(fc_path))

    def test_get_crs_name_WGS_1984_Web_Mercator(self):
        fc = "Web_Mercator_point"
        fc_path = os.path.join(self.fgdb, fc)
        self.assertEqual("WGS_1984_Web_Mercator_Auxiliary_Sphere",
                         get_crs_name(fc_path))

    def test_get_crs_name_MGAZ56(self):
        fc = "MGAZ56_point"
        fc_path = os.path.join(self.fgdb, fc)
        self.assertEqual("GDA_1994_MGA_Zone_56", get_crs_name(fc_path))

    def test_get_crs_name_NO_CRS(self):
        fc = "NO_CRS_point"
        fc_path = os.path.join(self.fgdb, fc)
        self.assertEqual("Unknown", get_crs_name(fc_path))


class TestGet_crs_wkid(TestCase):

    def setUp(self):
        self.fgdb = r"C:\tmp\fc_profiler_testdata\fc_profiler_test.gdb"

    def test_get_crs_wkid_GDA94_GA_Lambert(self):
        fc = "GDA94_GA_Lambert_point"
        fc_path = os.path.join(self.fgdb, fc)
        self.assertEqual(3112, get_crs_wkid(fc_path))

    def test_get_crs_wkid_GDA94_LL(self):
        fc = "GDA94_point"
        fc_path = os.path.join(self.fgdb, fc)
        self.assertEqual(4283, get_crs_wkid(fc_path))

    def test_get_crs_wkid_WGS84_LL(self):
        fc = "WGS84_point"
        fc_path = os.path.join(self.fgdb, fc)
        self.assertEqual(4326, get_crs_wkid(fc_path))

    def test_get_crs_wkid_WGS_1984_Web_Mercator(self):
        fc = "Web_Mercator_point"
        fc_path = os.path.join(self.fgdb, fc)
        self.assertEqual(3857, get_crs_wkid(fc_path))

    def test_get_crs_wkid_MGAZ56(self):
        fc = "MGAZ56_point"
        fc_path = os.path.join(self.fgdb, fc)
        self.assertEqual(28356, get_crs_wkid(fc_path))

    def test_get_crs_wkid_NO_CRS(self):
        fc = "NO_CRS_point"
        fc_path = os.path.join(self.fgdb, fc)
        self.assertEqual("Unknown", get_crs_name(fc_path))


class TestGet_crs_type(TestCase):

    def setUp(self):
        self.fgdb = r"C:\tmp\fc_profiler_testdata\fc_profiler_test.gdb"

    def test_get_crs_type_GDA94_GA_Lambert(self):
        fc = "GDA94_GA_Lambert_point"
        fc_path = os.path.join(self.fgdb, fc)
        self.assertEqual("Projected", get_crs_type(fc_path))

    def test_get_crs_type_GDA94_LL(self):
        fc = "GDA94_point"
        fc_path = os.path.join(self.fgdb, fc)
        self.assertEqual("Geographic", get_crs_type(fc_path))

    def test_get_crs_type_WGS84_LL(self):
        fc = "WGS84_point"
        fc_path = os.path.join(self.fgdb, fc)
        self.assertEqual("Geographic", get_crs_type(fc_path))

    def test_get_crs_type_WGS_1984_Web_Mercator(self):
        fc = "Web_Mercator_point"
        fc_path = os.path.join(self.fgdb, fc)
        self.assertEqual("Projected", get_crs_type(fc_path))

    def test_get_crs_type_MGAZ56(self):
        fc = "MGAZ56_point"
        fc_path = os.path.join(self.fgdb, fc)
        self.assertEqual("Projected", get_crs_type(fc_path))

    def test_get_crs_type_NO_CRS(self):
        fc = "NO_CRS_point"
        fc_path = os.path.join(self.fgdb, fc)
        self.assertEqual("Unknown", get_crs_name(fc_path))
