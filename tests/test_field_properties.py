import os
from unittest import TestCase


# self.assertEqual( <expected>, <actual>)

fgdb = r"C:\tmp\fc_profiler_testdata\fc_profiler_test.gdb"


class TestSomething(TestCase):

    def test_something(self):
        fc = "GDA94_all_field_types_polyline"
        fc_path = os.path.join(fgdb, fc)
        # self.assertEqual(5, get_fc_name(get_field_by_name(field_name)))


