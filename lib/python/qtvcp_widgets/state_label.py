#!/usr/bin/python2.7

from PyQt4 import QtCore, QtGui
import os
import linuxcnc
from qtvcp_widgets.simple_widgets import _HalWidgetBase
from qtvcp.qt_glib import GStat
GSTAT = GStat()

class Lcnc_State_Label(QtGui.QLabel, _HalWidgetBase):

    def __init__(self, parent=None):

        super(Lcnc_State_Label, self).__init__(parent)

        # if 'NO_FORCE_HOMING' is true, MDI  commands are allowed before homing.
        self.inifile = os.environ.get('INI_FILE_NAME', '/dev/null')
        self.ini = linuxcnc.ini(self.inifile)
        self.no_home_required = int(self.ini.find("TRAJ", "NO_FORCE_HOMING") or 0)

        self.display_units_mm=0
        self.machine_units_mm=0
        self.unit_convert=1
        try:
            self.inifile = self.emc.ini(INIPATH)
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
            self.machine_units_mm=1
            conversion=1.0/25.4
        else:
            self.machine_units_mm=0
            conversion=25.4
        self._set_machine_units(self.machine_units_mm,conversion)

        self._textTemplate = '%s'
        self.feed_override = True
        self.rapid_override = False
        self.spindle_override = False
        self.jograte = False
        self.tool_number = False
        self.current_feedrate = False
        self.requested_spindle_speed = False
        self.user_system = False

    def _hal_init(self):
        def _f(data):
            self._set_text(data)
        if self.feed_override:
            GSTAT.connect('feed-override-changed', lambda w,data: _f(data))
        elif self.rapid_override:
            GSTAT.connect('rapid-override-changed', lambda w,data: _f(data))
        elif self.spindle_override:
            GSTAT.connect('spindle-override-changed', lambda w,data: _f(data))
        elif self.jograte:
            GSTAT.connect('jograte-changed', lambda w,data: _f(data))
        elif self.tool_number:
            GSTAT.connect('tool-in-spindle-changed', lambda w,data: _f(data))
        elif self.current_feedrate:
            GSTAT.connect('current-feed-rate', self._set_feedrate_text)
            GSTAT.connect('metric-mode-changed',self._switch_units)
        elif self.requested_spindle_speed:
            GSTAT.connect('requested-spindle-speed-changed', lambda w,data: _f(data))
        elif self.user_system:
            GSTAT.connect('user-system-changed', self._set_user_system_text)

    def _set_text(self, data):
            tmpl = lambda s: str(self._textTemplate) % s
            self.setText(tmpl(data))

    def _set_feedrate_text(self, widget, data):
        if self.display_units_mm != self.machine_units_mm:
            data = data * self.unit_convert
        self._set_text(data)

    def _set_user_system_text(self, widgets, data):
        self._set_text(int(data)+53)

    def _set_machine_units(self,u,c):
        self.machine_units_mm = u
        self.unit_convert = c

    def _switch_units(self, widget, data):
        if data:
            self.display_units_mm = 1
        else:
            self.display_units_mm = 0

# property getter/setters

    def set_textTemplate(self, data):
        self._textTemplate = data
        try:
            self._set_text(100.0)
        except:
            self.setText('Error')
    def get_textTemplate(self):
        return self._textTemplate
    def reset_textTemplate(self):
        self._textTemplate = '%s'
    textTemplate = QtCore.pyqtProperty(str, get_textTemplate, set_textTemplate, reset_textTemplate)

    # feed override status 
    def set_feed_override(self, data):
        self.feed_override = data
    def get_feed_override(self):
        return self.feed_override
    def reset_feed_override(self):
        self.feed_override = False
    feed_override_status = QtCore.pyqtProperty(bool, get_feed_override, set_feed_override, reset_feed_override)

    # rapid override status 
    def set_rapid_override(self, data):
        self.rapid_override = data
    def get_rapid_override(self):
        return self.rapid_override
    def reset_rapid_override(self):
        self.rapid_override = False
    rapid_override_status = QtCore.pyqtProperty(bool, get_rapid_override, set_rapid_override, reset_rapid_override)

    # spindle override status 
    def set_spindle_override(self, data):
        self.spindle_override = data
    def get_spindle_override(self):
        return self.spindle_override
    def reset_spindle_override(self):
        self.spindle_override = False
    spindle_override_status = QtCore.pyqtProperty(bool, get_spindle_override, set_spindle_override, reset_spindle_override)

    # jograte status 
    def set_jograte(self, data):
        self.jograte = data
    def get_jograte(self):
        return self.jograte
    def reset_jograte(self):
        self.jograte = False
    jograte_status = QtCore.pyqtProperty(bool, get_jograte, set_jograte, reset_jograte)

    # tool number status 
    def set_tool_number(self, data):
        self.tool_number = data
    def get_tool_number(self):
        return self.tool_number
    def reset_tool_number(self):
        self.tool_number = False
    tool_number_status = QtCore.pyqtProperty(bool, get_tool_number, set_tool_number, reset_tool_number)

    # current feedrate status 
    def set_current_feedrate(self, data):
        self.current_feedrate = data
    def get_current_feedrate(self):
        return self.current_feedrate
    def reset_current_feedrate(self):
        self.current_feedrate = False
    current_feedrate_status = QtCore.pyqtProperty(bool, get_current_feedrate, set_current_feedrate, reset_current_feedrate)

    # spindle speed status 
    def set_requested_spindle_speed(self, data):
        self.requested_spindle_speed = data
    def get_requested_spindle_speed(self):
        return self.requested_spindle_speed
    def reset_requested_spindle_speed(self):
        self.requested_spindle_speed = False
    requested_spindle_speed_status = QtCore.pyqtProperty(bool, get_requested_spindle_speed, set_requested_spindle_speed, reset_requested_spindle_speed)

    # user_system status 
    def set_user_system(self, data):
        self.user_system = data
    def get_user_system(self):
        return self.user_system
    def reset_user_system(self):
        self.user_system = False
    user_system_status = QtCore.pyqtProperty(bool, get_user_system, set_user_system, reset_user_system)

if __name__ == "__main__":

    import sys

    app = QApplication(sys.argv)
    label = Lcnc_State_Label()
    label.show()
    sys.exit(app.exec_())
