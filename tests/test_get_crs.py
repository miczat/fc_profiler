from unittest import TestCase
from fc_properties import get_crs_name
from fc_properties import get_crs_wkid
import os


class TestGet_crs_name(TestCase):

    def setUp(self):
        self.fgdb = r"C:\tmp\fc_profiler_testdata\fc_profiler_test.gdb"

    def test_get_crs_name_GDA94_GA_Lambert(self):
        fc = "GDA94_GA_Lambert_point"
        fc_path = os.path.join(self.fgdb, fc)
        self.assertEqual(get_crs_name(fc_path),
                         "GDA_1994_Geoscience_Australia_Lambert")

    def test_get_crs_name_GDA94_LL(self):
        fc = "GDA94_point"
        fc_path = os.path.join(self.fgdb, fc)
        self.assertEqual(get_crs_name(fc_path), "GCS_GDA_1994")

    def test_get_crs_name_WGS84_LL(self):
        fc = "WGS84_point"
        fc_path = os.path.join(self.fgdb, fc)
        self.assertEqual(get_crs_name(fc_path), "GCS_WGS_1984")

    def test_get_crs_name_WGS_1984_Web_Mercator(self):
        fc = "Web_Mercator_point"
        fc_path = os.path.join(self.fgdb, fc)
        self.assertEqual(get_crs_name(fc_path),
                         "WGS_1984_Web_Mercator_Auxiliary_Sphere")

    def test_get_crs_name_MGAZ56(self):
        fc = "MGAZ56_point"
        fc_path = os.path.join(self.fgdb, fc)
        self.assertEqual(get_crs_name(fc_path), "GDA_1994_MGA_Zone_56")

    def test_get_crs_name_NO_CRS(self):
        fc = "NO_CRS_point"
        fc_path = os.path.join(self.fgdb, fc)
        self.assertEqual(get_crs_name(fc_path), "Unknown")



class TestGet_crs_wkid(TestCase):

    def setUp(self):
        self.fgdb = r"C:\tmp\fc_profiler_testdata\fc_profiler_test.gdb"

    def test_get_crs_wkid_GDA94_GA_Lambert(self):
        fc = "GDA94_GA_Lambert_point"
        fc_path = os.path.join(self.fgdb, fc)
        self.assertEqual(get_crs_wkid(fc_path), 3112)

    def test_get_crs_wkid_GDA94_LL(self):
        fc = "GDA94_point"
        fc_path = os.path.join(self.fgdb, fc)
        self.assertEqual(get_crs_wkid(fc_path), 4283)

    def test_get_crs_wkid_WGS84_LL(self):
        fc = "WGS84_point"
        fc_path = os.path.join(self.fgdb, fc)
        self.assertEqual(get_crs_wkid(fc_path), 4326)

    def test_get_crs_wkid_WGS_1984_Web_Mercator(self):
        fc = "Web_Mercator_point"
        fc_path = os.path.join(self.fgdb, fc)
        self.assertEqual(get_crs_wkid(fc_path),3857)

    def test_get_crs_wkid_MGAZ56(self):
        fc = "MGAZ56_point"
        fc_path = os.path.join(self.fgdb, fc)
        self.assertEqual(get_crs_wkid(fc_path), 28356)

    def test_get_crs_wkid_NO_CRS(self):
        fc = "NO_CRS_point"
        fc_path = os.path.join(self.fgdb, fc)
        self.assertEqual(get_crs_name(fc_path), "Unknown")
