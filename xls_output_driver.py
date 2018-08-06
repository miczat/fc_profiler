# -------------------------------------------
# driver for developing xls_output
# -------------------------------------------


from xls_output import write_fc_properties



data = [("Feature Class", "GDA94_polyline"),
       ("Parent fGDB", r"C:\tmp\fc_profiler_testdata\fc_profiler_test.gdb"),
       ("Geometry Type", "Polyline"),
       ("CRS Name", "GCS_GDA_1994"),
       ("CRS EPSG WKID", 4283),
       ("CRS Type", "Geographic"),
       ("CRS Units", "Degree")]

xls_path = r"C:\tmp\dev.xls"

print("writing...")
print(write_fc_properties(data, xls_path))



