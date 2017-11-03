#!/usr/bin/python3

from PyQt4.QtGui import QIcon, QPixmap
from PyQt4.QtDesigner import QPyDesignerCustomWidgetPlugin
from qtvcp_widgets.overlay_widget import LoadingOverlay
from qtvcp_widgets.qtvcp_icons import Icon
ICON = Icon()

class LoadingOverlayPlugin(QPyDesignerCustomWidgetPlugin):

    def __init__(self, parent=None):
        super(LoadingOverlayPlugin, self).__init__(parent)

        self.initialized = False

    def initialize(self, core):
        if self.initialized:
            return

        self.initialized = True

    def isInitialized(self):
        return self.initialized

    def createWidget(self, parent):
        return LoadingOverlay(parent)

    def name(self):
        return "LoadingOverlay"

    def group(self):
        return "Linuxcnc - HAL"

    def icon(self):
        return QIcon(QPixmap(ICON.get_path('loadingoverlay')))

    def toolTip(self):
        return ""

    def whatsThis(self):
        return ""

    def isContainer(self):
        return True

    # Returns an XML description of a custom widget instance that describes
    # default values for its properties. Each custom widget created by this
    # plugin will be configured using this description.
    def domXml(self):
        return '<widget class="LoadingOverlay" name="loadingoverlay" />\n'

    def includeFile(self):
        return "qtvcp_widgets.overlay_widget"
