#!/usr/bin/env python
# qtVcp actions
#
# Copyright (c) 2017  Chris Morley <chrisinnanaimo@hotmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# Action buttons are used to change linuxcnc behaivor do to button pushing.
# By making the button 'checkable' in the designer editor, the buton will toggle.
# In the designer editor, it is possible to select what the button will do.
#################################################################################

from PyQt4 import QtCore, QtGui
from qtvcp_widgets.simple_widgets import _HalWidgetBase
from qtvcp.qt_glib import GStat, Lcnc_Action

# Instiniate the libraries with global reference
# GSTAT gives us status messages from linuxcnc
# ACTION gives commands to linuxcnc
GSTAT = GStat()
ACTION = Lcnc_Action()

class Lcnc_ActionButton(QtGui.QPushButton, _HalWidgetBase):
    def __init__(self, parent = None):
        QtGui.QPushButton.__init__(self, parent)
        #self.setCheckable(False)
        self._block_signal = False
        self.estop = True
        self.machine_on = False
        self.home = False
        self.home_joint = -1 # all
        self.load_dialog = False


    # This gets called by qtvcp_makepins
    # It infers HAL involvement but there is none
    # GSTAT is used to synch the buttons in case
    # other entities change linuxcnc's state
    # also some buttons are disabled/enabled based on
    # linuxcnc state / possible actions
    #
    # _safecheck blocks the outgoing signal so
    # the buttons can be synced with linuxcnc
    # without setting an infinite loop
    def _hal_init(self):
        def _safecheck(state,data=None):
            self._block_signal = True
            self.setChecked(state)
            self._block_signal = False

        if self.estop:
            # Estop starts with button down - in estop which
            # backwards logic for the button...
            if self.isCheckable():_safecheck(True)
            GSTAT.connect('state-estop', lambda w: _safecheck(True))
            GSTAT.connect('state-estop-reset', lambda w: _safecheck(False))

        elif self.machine_on:
            #self.setEnabled(False)
            GSTAT.connect('state-estop', lambda w: self.setEnabled(False))
            GSTAT.connect('state-estop-reset', lambda w: self.setEnabled(True))
            GSTAT.connect('state-on', lambda w: _safecheck(True))
            GSTAT.connect('state-off', lambda w: _safecheck(False))

        elif self.home:
            #self.setEnabled(False)
            GSTAT.connect('state-off', lambda w: self.setEnabled(False))
            GSTAT.connect('state-estop', lambda w: self.setEnabled(False))
            GSTAT.connect('interp-idle', lambda w: self.setEnabled(GSTAT.machine_is_on()))
            GSTAT.connect('interp-run', lambda w: self.setEnabled(False))
            GSTAT.connect('all-homed', lambda w: _safecheck(True))
            GSTAT.connect('not-all-homed', lambda w, axis: _safecheck(False, axis))

        elif self.load_dialog:
            GSTAT.connect('state-off', lambda w: self.setEnabled(False))
            GSTAT.connect('state-estop', lambda w: self.setEnabled(False))
            GSTAT.connect('interp-idle', lambda w: self.setEnabled(GSTAT.machine_is_on()))
            GSTAT.connect('interp-run', lambda w: self.setEnabled(False))
            GSTAT.connect('all-homed', lambda w: _safecheck(True))

        # connect a signal and callback function to the button
        self.clicked[bool].connect(self.action)

    def action(self,state = None):
        # don't do anything if the signal is blocked
        if self._block_signal: return

        if self.estop:
            if self.isCheckable():
                ACTION.SET_ESTOP_STATE(state)
            else:
                ACTION.SET_ESTOP_STATE(GSTAT.estop_is_clear())

        elif self.machine_on:
           if self.isCheckable():
                ACTION.SET_MACHINE_STATE(state)
           else:
                print 'gstat:',GSTAT.machine_is_on
                ACTION.SET_MACHINE_STATE(not GSTAT.machine_is_on())

        elif self.home:
           if self.isCheckable():
                if state:
                    ACTION.SET_MACHINE_HOMING(self.home_joint)
                else:
                    ACTION.SET_MACHINE_UNHOMED(self.home_joint)
           else:
                if GSTAT.is_all_homed():
                    ACTION.SET_MACHINE_UNHOMED(self.home_joint)
                else:
                    ACTION.SET_MACHINE_HOMING(self.home_joint)

        elif self.load_dialog:
            GSTAT.emit('load-file-request')
        # defult error case
        else:
            print 'QTVCP: action button: * No action recognised *'


    #########################################################################
    # This is how designer can interact with our widget
    # designer will show the pyqtProperty properties in the editor
    # it will use the get set and reset calls to do those actions

    # estop_action
    def set_estop(self, data):
        self.estop = data
    def get_estop(self):
        return self.estop
    def reset_estop(self):
        self.estop = False
    estop_action = QtCore.pyqtProperty(bool, get_estop, set_estop, reset_estop)

    # machine_on_action
    def set_machine_on(self, data):
        self.machine_on = data
    def get_machine_on(self):
        return self.machine_on
    def reset_machine_on(self):
        self.machine_on = False
    machine_on_action = QtCore.pyqtProperty(bool, get_machine_on, set_machine_on, reset_machine_on)

   # home_action
    def set_home(self, data):
        self.home = data
    def get_home(self):
        return self.home
    def reset_home(self):
        self.home = False
    home_action = QtCore.pyqtProperty(bool, get_home, set_home, reset_home)

    # home_joint_number
    def set_home_joint(self, data):
        self.home_joint = data
    def get_home_joint(self):
        return self.home_joint
    def reset_home_joint(self):
        self.home_joint = -1
    home_joint_number = QtCore.pyqtProperty(int, get_home_joint, set_home_joint, reset_home_joint)

   # load_dialogaction
    def set_load_dialog(self, data):
        self.load_dialog = data
    def get_load_dialog(self):
        return self.load_dialog
    def reset_load_dialog(self):
        self.load_dialog = False
    load_dialog_action = QtCore.pyqtProperty(bool, get_load_dialog, set_load_dialog, reset_load_dialog)

if __name__ == "__main__":

    import sys
    from PyQt4.QtGui import QApplication
    app = QApplication(sys.argv)

    widget = Lcnc_ActionButton('Action')
    # this doesn't get called without qtvcp loading the widget
    widget._hal_init()

    widget.show()
    sys.exit(app.exec_())
