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

        # GetInputs
        in_fc = parameters[0]
        out_folder = parameters[1]
        debug = parameters[2]

        # DEBUG check
        debug.value = str(in_fc.valueAsText) + "; " + str(out_folder.valueAsText)

        return


    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        # Get Inputs
        out_folder = parameters[1]

        # Check output folder write access
        # .valueAsText returns unicode, so cast for string to string comparison,
        if not os.access(str(out_folder.valueAsText), os.W_OK):
            out_folder.setErrorMessage("The selected folder cannot be written to.\n"
                                       "Please choose another folder.")
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        # TO DO - need to call other code with the full path to the FC and output folder

        return
