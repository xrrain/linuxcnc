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
        self._textTemplate = '%s'
        self.feed_override = True
        self.rapid_override = False
        self.spindle_override = False
        self.jograte = False
        self.tool_number = False

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

    def _set_text(self, data):
            tmpl = lambda s: str(self._textTemplate) % s
            self.setText(tmpl(data))

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
        self._hal_init()
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

if __name__ == "__main__":

    import sys

    app = QApplication(sys.argv)
    label = Lcnc_State_Label()
    label.show()
    sys.exit(app.exec_())
