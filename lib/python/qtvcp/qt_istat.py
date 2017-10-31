import os
import linuxcnc


class IStat():

    def __init__(self):

        INIPATH = os.environ.get('INI_FILE_NAME', '/dev/null')
        self.inifile = linuxcnc.ini(INIPATH)
        self.MDI_HISTORY_PATH = '~/.axis_mdi_history'
        self.MACHINE_IS_LATHE = False
        self.MACHINE_IS_METRIC = False
        self.MACHINE_UNIT_CONVERSION = 1
        self.MACHINE_UNIT_CONVERSION_9 = [1]*9
        self.NO_HOME_REQUIRED = False
        self.JOG_INCREMENTS = None
        self.ANGULAR_INCREMENTS = None
        self.update()

    def update(self):
        self.MDI_HISTORY_PATH = self.inifile.find('DISPLAY', 'MDI_HISTORY_FILE') or '~/.axis_mdi_history'
        self.MACHINE_IS_LATHE = bool(self.inifile.find("DISPLAY", "LATHE"))

        try:
            # check the ini file if UNITS are set to mm"
            # first check the global settings
            units=self.inifile.find("TRAJ","LINEAR_UNITS")
            if units==None:
                # else then the X axis units
                units=self.inifile.find("AXIS_0","UNITS")
        except:
            units = "inch"
        # set up the conversion arrays based on what units we discovered
        if units=="mm" or units=="metric" or units == "1.0":
            self.MACHINE_IS_METRIC = True
            self.MACHINE_UNIT_CONVERSION = 1.0/25.4
            self.MACHINE_UNIT_CONVERSIO_9 = [1.0/25.4]*3+[1]*3+[1.0/25.4]*3
        else:
            self.MACHINE_IS_METRIC = False
            self.MACHINE_UNIT_CONVERSION = 25.4
            self.MACHINE_UNIT_CONVERSIO_9 = [25.4]*3+[1]*3+[25.4]*3

        self.NO_HOME_REQUIRED = int(self.inifile.find("TRAJ", "NO_FORCE_HOMING") or 0)

        # jogging increments
        increments = self.inifile.find("DISPLAY", "INCREMENTS")
        if increments:
            if not "continuous" in increments:
                increments +=",continuous"
            if "," in increments:
                self.JOG_INCREMENTS = [i.strip() for i in increments.split(",")]
            else:
                self.JOG_INCREMENTS = increments.split()
        else:
            if self.MACHINE_IS_METRIC:
                self.JOG_INCREMENTS = [".001 mm",".01 mm",".1 mm","1 mm","continuous"]
            else:
                self.JOG_INCREMENTS = [".0001 in",".001 in",".01 in",".1 in","continuous"]

        # angular jogging increments
        increments = self.inifile.find("DISPLAY", "ANGULAR_INCREMENTS")
        if increments:
            if not "continuous" in increments:
                increments +=",continuous"
            if "," in increments:
                self.ANGULAR_INCREMENTS = [i.strip() for i in increments.split(",")]
            else:
                self.data.angular_jog_increments = increments.split()
        else:
            self.ANGULAR_INCREMENTS = ["1","45","180","360","continuous"]

    def convert_units(self, data):
        return data * self.MACHINE_UNIT_CONVERSION

    def convert_units_9(self,v):
        c = self.MACHINE_UNIT_CONVERSION_9
        return map(lambda x,y: x*y, v, c)

