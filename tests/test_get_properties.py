from unittest import TestCase
from fc_properties import get_fc_name
import os

# self.assertEqual( <expected>, <actual>)


class Testget_fc_name(TestCase):

    def setUp(self):
        self.fgdb = r"C:\tmp\fc_profiler_testdata\fc_profiler_test.gdb"

    def test_get_fc_name_GDA94_GA_Lambert(self):
        fc = "GDA94_GA_Lambert_point"
        fc_path = os.path.join(self.fgdb, fc)
        self.assertEqual(fc, get_fc_name(fc_path))

    def test_get_fc_name_GDA94_LL(self):
        fc = "GDA94_point"
        fc_path = os.path.join(self.fgdb, fc)
        self.assertEqual(fc, get_fc_name(fc_path))

    def test_get_fc_name_WGS84_LL(self):
        fc = "WGS84_point"
        fc_path = os.path.join(self.fgdb, fc)
        self.assertEqual(fc, get_fc_name(fc_path))

    def test_get_fc_name_WGS_1984_Web_Mercator(self):
        fc = "Web_Mercator_point"
        fc_path = os.path.join(self.fgdb, fc)
        self.assertEqual(fc, get_fc_name(fc_path))

    def test_get_fc_name_MGAZ56(self):
        fc = "MGAZ56_point"
        fc_path = os.path.join(self.fgdb, fc)
        self.assertEqual(fc, get_fc_name(fc_path))

    def test_get_fc_name_NO_CRS(self):
        fc = "NO_CRS_point"
        fc_path = os.path.join(self.fgdb, fc)
        self.assertEqual(fc, get_fc_name(fc_path))
