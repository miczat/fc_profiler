import arcpy
import os

# TO DO add logging

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "fcProfiler"
        self.alias = "fcProfilerPyToolbox"

        # List of tool classes associated with this toolbox
        self.tools = [FcProfiler]


class FcProfiler(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "FcProfiler"
        self.description = "Generate a data profile for a feature class"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""

        # input feature class
        in_fc = arcpy.Parameter(
            displayName="Input Feature Class",
            name="in_fc",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input")
        in_fc.filter.list = ["Point", "Polyline", "Polygon"]

        # output folder
        # datatype="DEWorkspace" will allow folder selection, use str() to get name
        # datatype="DEFolder" is not used as the GUI allows for the selection of a file
        out_folder = arcpy.Parameter(
            displayName="Output Folder",
            name="out_folder",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input")
        out_folder.filter.list = ["File System"]


        if DEBUG:
            # debug message field
            debug = arcpy.Parameter(
                displayName="debug",
                name="debug",
                datatype="String",
                parameterType="Optional",
                direction="Input")

        params = [in_fc, out_folder, debug]
        return params


    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        # No known licencing dependencies
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""

        # Get Inputs
        out_folder = parameters[1]
        debug = parameters[2]

        debug.value = out_folder.valueAsText

        # check output folder write access  string to string comparison,
        # valueAsText returns unicode
        if not os.access(str(out_folder.valueAsText), os.W_OK):
            debug.value = "This folder is NOT writable"
        else:
            debug.value = "This folder IS writable"

        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        # TO DO - need to call other code with the full path to the FC and output folder

        return
