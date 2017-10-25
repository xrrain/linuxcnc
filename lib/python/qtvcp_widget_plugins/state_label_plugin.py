#!/usr/bin/python3

from PyQt4.QtGui import QIcon, QPixmap
from PyQt4.QtDesigner import QPyDesignerCustomWidgetPlugin
from qtvcp_widgets.state_label import Lcnc_State_Label
from qtvcp_widgets.qtvcp_icons import Icon
ICON = Icon()

class StateLabelPlugin(QPyDesignerCustomWidgetPlugin):

    def __init__(self, parent=None):
        super(StateLabelPlugin, self).__init__(parent)

        self.initialized = False

    def initialize(self, core):
        if self.initialized:
            return

        self.initialized = True

    def isInitialized(self):
        return self.initialized

    def createWidget(self, parent):
        return Lcnc_State_Label(parent)

    def name(self):
        return "Lcnc_State_Label"

    def group(self):
        return "Linuxcnc - Controller"

    def icon(self):
        return QIcon(QPixmap(ICON.get_path('lcnc_state_label')))

    def toolTip(self):
        return ""

    def whatsThis(self):
        return ""

    def isContainer(self):
        return False

    # Returns an XML description of a custom widget instance that describes
    # default values for its properties. Each custom widget created by this
    # plugin will be configured using this description.
    def domXml(self):
        return '<widget class="Lcnc_State_Label" name="lcnc_state_label" />\n'

    def includeFile(self):
        return "qtvcp_widgets.state_label"
