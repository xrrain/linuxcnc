#!/usr/bin/python2.7

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qtvcp_widgets.simple_widgets import _HalWidgetBase, hal, hal_pin_changed_signal

class Lcnc_Led(QWidget, _HalWidgetBase):

    def __init__(self, parent=None):

        super(Lcnc_Led, self).__init__(parent)

        self._diamX = 0
        self._diamY = 0
        self._diameter = 30
        self._color = QColor("red")
        self._alignment = Qt.AlignCenter
        self._state = True
        self._state_flashing = False
        self._flashing = False
        self._flashRate = 200

        self._timer = QTimer()
        self._timer.timeout.connect(self.toggleState)

        self.setDiameter(self._diameter)

        self.has_hal_pins = True

    def _hal_init(self):
        if (self.has_hal_pins):
            _HalWidgetBase._hal_init(self)
            self.hal_pin = self.hal.newpin(self.hal_name, hal.HAL_BIT, hal.HAL_IN)
            def _f(data):
                if data and self._state_flashing:
                    self.setFlashing(True)
                elif data and not self._state_flashing:
                    self.setState(True)
                else:
                    self.setFlashing(False)
                    self.setState(False)

            self.hal_pin.value_changed.connect( lambda s: _f(s))
            # not sure we need a flash pin
            #self.hal_pin_flash = self.hal.newpin(self.hal_name+'-flash', hal.HAL_BIT, hal.HAL_IN)
            #self.hal_pin_flash.value_changed.connect( lambda s: self.setFlashing(s))

    def paintEvent(self, event):
        painter = QPainter()
        x = 0
        y = 0
        if self._alignment & Qt.AlignLeft:
            x = 0
        elif self._alignment & Qt.AlignRight:
            x = self.width() - self._diameter
        elif self._alignment & Qt.AlignHCenter:
            x = (self.width() - self._diameter) / 2
        elif self._alignment & Qt.AlignJustify:
            x = 0

        if self._alignment & Qt.AlignTop:
            y = 0
        elif self._alignment & Qt.AlignBottom:
            y = self.height() - self._diameter
        elif self._alignment & Qt.AlignVCenter:
            y = (self.height() - self._diameter) / 2

        gradient = QRadialGradient(x + self._diameter / 2, y + self._diameter / 2,
                                   self._diameter * 0.4, self._diameter * 0.4, self._diameter * 0.4)
        gradient.setColorAt(0, Qt.white)

        if self._state:
            gradient.setColorAt(1, self._color)
        else:
            gradient.setColorAt(1, Qt.black)

        painter.begin(self)
        brush = QBrush(gradient)
        painter.setPen(self._color)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setBrush(brush)
        painter.drawEllipse(x, y, self._diameter - 1, self._diameter - 1)

        if self._flashRate > 0 and self._flashing:
            self._timer.start(self._flashRate)
        else:
            self._timer.stop()

        painter.end()

    def minimumSizeHint(self):
        return QSize(self._diameter, self._diameter)

    def sizeHint(self):
        return QSize(self._diameter, self._diameter)

    def getDiameter(self):
        return self._diameter

    @pyqtSlot(int)
    def setDiameter(self, value):
        self._diameter = value
        self.update()

    def getColor(self):
        return self._color

    @pyqtSlot(QColor)
    def setColor(self, value):
        self._color = value
        self.update()

    def getAlignment(self):
        return self._alignment

    @pyqtSlot(Qt.Alignment)
    def setAlignment(self, value):
        self._alignment = value
        self.update()

    def getState(self):
        return self._alignment

    @pyqtSlot(bool)
    def setState(self, value):
        self._state = value
        self.update()

    @pyqtSlot()
    def toggleState(self):
        self._state = not self._state
        self.update()

    def isFlashing(self):
        return self._flashing

    @pyqtSlot(bool)
    def setFlashing(self, value):
        self._flashing = value
        print "value",value
        self.update()

    def getFlashRate(self):
        return self._flashRate

    @pyqtSlot(int)
    def setFlashRate(self, value):
        self._flashRate = value
        self.update()

    @pyqtSlot()
    def startFlashing(self):
        self.setFlashing(True)

    @pyqtSlot()
    def stopFlashing(self):
        self.setFlashing(False)

    diameter = pyqtProperty(int, getDiameter, setDiameter)
    color = pyqtProperty(QColor, getColor, setColor)
    alignment = pyqtProperty(Qt.Alignment, getAlignment, setAlignment)
    state = pyqtProperty(bool, getState, setState)
    flashing = pyqtProperty(bool, isFlashing, setFlashing)
    flashRate = pyqtProperty(int, getFlashRate, setFlashRate)

if __name__ == "__main__":

    import sys

    app = QApplication(sys.argv)
    led = Lcnc_Led()
    led.show()
    led.startFlashing()
    sys.exit(app.exec_())
