#!/usr/bin/python2.7

from PyQt4.QtCore import pyqtProperty
from qtvcp_widgets.ledwidget import Lcnc_Led
from qtvcp.qt_glib import GStat
GSTAT = GStat()

class Lcnc_State_Led(Lcnc_Led,):

    def __init__(self, parent=None):

        super(Lcnc_State_Led, self).__init__(parent)
        self.has_hal_pins = False
        self.setState(False)

        self.is_estopped = False
        self.is_on = False
        self.is_homed = False
        self.is_idle = False
        self.is_paused = False
        self.invert_state = False

    def _hal_init(self):
        def _f(data):
            print data, self.flash
            if self.invert_state:
                data = not data
            self.change_state(data)

        if self.is_estopped:
            GSTAT.connect('state-estop', lambda w: _f(True))
            GSTAT.connect('state-estop-reset', lambda w: _f(False))
        elif self.is_on:
            GSTAT.connect('state-on', lambda w: _f(True))
            GSTAT.connect('state-off', lambda w: _f(False))
        elif self.is_homed:
            GSTAT.connect('all-homed', lambda w: _f(True) )
            GSTAT.connect('not-all-homed', lambda w,axis: _f(False) )
        elif self.is_idle:
            GSTAT.connect('interp-idle', lambda w: _f(False) )
            GSTAT.connect('interp-run', lambda w: _f(False) )
        elif self.is_paused:
            GSTAT.connect( 'program-pause-changed', lambda w,data: _f(data))



# property getter/setters

    # invert status 
    def set_invert_state(self, data):
        self.invert_state = data
    def get_invert_state(self):
        return self.invert_state
    def reset_invert_state(self):
        self.invert_state = False
    invert_state_status = pyqtProperty(bool, get_invert_state, set_invert_state, reset_invert_state)

    # machine is paused status 
    def set_is_paused(self, data):
        self.is_paused = data
    def get_is_paused(self):
        return self.is_paused
    def reset_is_paused(self):
        self.is_paused = False
    is_paused_status = pyqtProperty(bool, get_is_paused, set_is_paused, reset_is_paused)

    # machine is estopped status 
    def set_is_estopped(self, data):
        self.is_estopped = data
    def get_is_estopped(self):
        return self.is_estopped
    def reset_is_estopped(self):
        self.is_estopped = False
    is_estopped_status = pyqtProperty(bool, get_is_estopped, set_is_estopped, reset_is_estopped)

    # machine is on status 
    def set_is_on(self, data):
        self.is_on = data
    def get_is_on(self):
        return self.is_on
    def reset_is_on(self):
        self.is_on = False
    is_on_status = pyqtProperty(bool, get_is_on, set_is_on, reset_is_on)

    # machine is idle status 
    def set_is_idle(self, data):
        self.is_idle = data
        if (data and self.is_not_idle):
            self.is_not_idle = False
    def get_is_idle(self):
        return self.is_idle
    def reset_is_idle(self):
        self.is_idle = False
    is_idle_status = pyqtProperty(bool, get_is_idle, set_is_idle, reset_is_idle)

    # machine is homed status 
    def set_is_homed(self, data):
        self.is_homed = data
    def get_is_homed(self):
        return self.is_homed
    def reset_is_homed(self):
        self.is_homed = False
    is_homed_status = pyqtProperty(bool, get_is_homed, set_is_homed, reset_is_homed)

if __name__ == "__main__":

    import sys
    from PyQt4.QtGui import QApplication
    app = QApplication(sys.argv)
    led = Lcnc_State_Led()
    led.show()
    #led.startFlashing()
    sys.exit(app.exec_())
