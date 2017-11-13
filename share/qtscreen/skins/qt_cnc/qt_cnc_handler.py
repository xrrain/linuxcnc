############################
# **** IMPORT SECTION **** #
############################

from PyQt4 import QtCore
from PyQt4 import QtGui
from qtscreen.keybindings import Keylookup
from qtscreen.notify import Notify
from qtscreen.message import Message
from qtscreen.preferences import Access
from qtvcp.qt_glib import GStat

import linuxcnc
import sys
import os

###########################################
# **** instantiate libraries section **** #
###########################################

KEYBIND = Keylookup()
GSTAT = GStat()
NOTE = Notify()
MSG = Message()
PREFS = Access()

###################################
# **** HANDLER CLASS SECTION **** #
###################################

class HandlerClass:

    ########################
    # **** INITIALIZE **** #
    ########################
    # widgets allows access to  widgets from the qtvcp files
    # at this point the widgets and hal pins are not instantiated
    def __init__(self, halcomp,widgets,paths):
        self.hal = halcomp
        self.w = widgets
        self.stat = linuxcnc.stat()
        self.cmnd = linuxcnc.command()
        self.error = linuxcnc.error_channel()
        self.PATH = paths.CONFIGPATH
        self.IMAGE_PATH = paths.IMAGEDIR

        # Read user preferences
        self.desktop_notify = PREFS.getpref('desktop_notify', True, bool)
        self.shutdown_check = PREFS.getpref('shutdown_check', True, bool)

    ##########################################
    # Special Functions called from QTSCREEN
    ##########################################

    # at this point:
    # the widgets are instantiated.
    # the HAL pins are built but HAL is not set ready
    def initialized__(self):
        # Give notify library a reference to the statusbar
        NOTE.statusbar = self.w.statusBar
        if self.desktop_notify:
            NOTE.notify('Welcome','This is a test screen for Qtscreen',None,4)
        GSTAT.forced_update()

        # add a backgrund image
        self.w.setObjectName("MainWindow")
        bgpath = self.IMAGE_PATH+'/hazzy_bg_black.png'
        self.w.setStyleSheet("#MainWindow { background-image: url(%s) 0 0 0 0 stretch stretch; }"%bgpath)
        bgpath = self.IMAGE_PATH+'/frame_bg_blue.png'
        self.w.frame.setStyleSheet("#frame { border-image: url(%s) 0 0 0 0 stretch stretch; }"%bgpath)
        bgpath = self.IMAGE_PATH+'/frame_bg_grey.png'
        self.w.frame_2.setStyleSheet("QFrame { border-image: url(%s) 0 0 0 0 stretch stretch; }"%bgpath)

    def processed_key_event__(self,receiver,event,is_pressed,key,code,shift,cntrl):
        # when typing in MDI, we don't want keybinding to call functions
        # so we catch and process the events directly.
        # We do want ESC, F1 and F2 to call keybinding functions though
        if self.w.mdi_line == receiver and code not in(16777216,16777264,16777216):
            if is_pressed:
                self.w.mdi_line.keyPressEvent(event)
                event.accept()
            return True
        try:
            KEYBIND.call(self,event,is_pressed,shift,cntrl)
            return True
        except AttributeError:
            print 'Error in, or no function for: %s in handler file for-%s'%(KEYBIND.convert(event),key)
            #print 'from %s'% receiver
            return False

    ########################
    # callbacks from GSTAT #
    ########################

    #######################
    # callbacks from form #
    #######################

    #####################
    # general functions #
    #####################

    #####################
    # KEY BINDING CALLS #
    #####################
    def on_keycall_ABORT(self,event,state,shift,cntrl):
        if state:
            print 'abort'
            if GSTAT.stat.interp_state == linuxcnc.INTERP_IDLE:
                print 'close'
                self.w.close()
            else:
                print 'abort'
                self.cmnd.abort()

    def on_keycall_ESTOP(self,event,state,shift,cntrl):
        if state:
            self.w.button_estop.click()
    def on_keycall_POWER(self,event,state,shift,cntrl):
        if state:
            self.w.button_machineon.click()
    def on_keycall_HOME(self,event,state,shift,cntrl):
        if state:
            self.w.button_home.click()

    def on_keycall_XPOS(self,event,state,shift,cntrl):
        if state:
            self.w.jog_pos_x.pressed.emit()
        else:
            self.w.jog_pos_x.released.emit()
    def on_keycall_XNEG(self,event,state,shift,cntrl):
        if state:
            self.w.jog_neg_x.pressed.emit()
        else:
            self.w.jog_neg_x.released.emit()

    def on_keycall_YPOS(self,event,state,shift,cntrl):
        if state:
            self.w.jog_pos_y.pressed.emit()
        else:
            self.w.jog_pos_y.released.emit()

    def on_keycall_YNEG(self,event,state,shift,cntrl):
        if state:
            self.w.jog_neg_y.pressed.emit()
        else:
            self.w.jog_neg_y.released.emit()

    def on_keycall_ZPOS(self,event,state,shift,cntrl):
        if state:
            self.w.jog_pos_z.pressed.emit()
        else:
            self.w.jog_pos_z.released.emit()
    def on_keycall_ZNEG(self,event,state,shift,cntrl):
        if state:
            self.w.jog_neg_z.pressed.emit()
        else:
            self.w.jog_neg_z.released.emit()

    ###########################
    # **** closing event **** #
    ###########################

    ##############################
    # required class boiler code #
    ##############################

    def __getitem__(self, item):
        return getattr(self, item)
    def __setitem__(self, item, value):
        return setattr(self, item, value)

################################
# required handler boiler code #
################################

def get_handlers(halcomp,widgets,paths):
     return [HandlerClass(halcomp,widgets,paths)]
