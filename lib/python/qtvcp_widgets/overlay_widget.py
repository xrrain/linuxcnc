#!/usr/bin/python2.7

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qtvcp_widgets.simple_widgets import _HalWidgetBase
from qtvcp.qt_glib import GStat
GSTAT = GStat()

class OverlayWidget(QWidget, _HalWidgetBase):
    def __init__(self, parent=None):
        self.last = None
        self.top_level = parent
        super(OverlayWidget, self).__init__(parent)
        self.parent = parent
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setWindowFlags( self.windowFlags() |Qt.Tool |
                        Qt.FramelessWindowHint | Qt.Dialog |
                             Qt.WindowStaysOnTopHint |Qt.WindowSystemMenuHint)

    # Find the top level widget and add an event filter
    def newParent(self):
        if not self.parent: return
        self.parent = self.top_level
        if not self.last == None:
            #print 'last removed:',self.last
            self.last.removeEventFilter(self)
        self.parent.installEventFilter(self)
        self.last = self.parent
        self.raise_()

    def eventFilter(self, obj, event):
        #print event,'parent',self.parent
        if obj == self.parent:
            #Catches resize and child events from the parent widget
            if event.type() == QEvent.Resize:
                self.resize(QResizeEvent.size(event))
                self.raise_()
            elif event.type() == QEvent.Move:
                self.move(QMoveEvent.pos(event))
                self.raise_()
            elif(event.type() == QEvent.ChildAdded):
                print 'CHILD',QChildEvent.child(event)
                if not QChildEvent.child(event) is QDialog:
                    self.raise_()
            if event.type() == QEvent.Close:
                self.hide()
                self.closeEvent(event)
                event.accept()
        return super(OverlayWidget,self).eventFilter(obj, event)

    # Tracks parent widget changes
    def event(self, event):
        #print 'overlay:',event
        if event.type() == QEvent.ParentAboutToChange:
            print 'REMOVE FILTER'
            self.parent.removeEventFilter()
            return True
        if event.type() == QEvent.ParentChange:
            print 'parentEVENT:', self.parentWidget()
            self.newParent()
            return True
        if event.type() == QEvent.Paint:
            self.paintEvent(event)
            return True
        return False

class LoadingOverlay(OverlayWidget):
    def __init__(self, parent=None):
        super(LoadingOverlay, self).__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.bg_color = QColor(0, 0, 0,150)
        self.text_color = QColor(0,0,0)
        self.dialog_color = QColor(255,255,255)
        self.font = QFont("arial,helvetica", 40)
        self.text = "Loading..."
        self.box()
        self._state = False

    def _hal_init(self):
        def _f(data,text,color):
            if data:
                if color:
                    self.bg_color = color
                else:
                    self.bg_color = QColor(0, 0, 0,150)
                if text:
                    self.text = text
                self.show()

            else:
                self.hide()
        GSTAT.connect('focus-overlay-changed', lambda w,data,text,color: _f(data,text,color))

    # Seems the only way to consistantly get the top level widget
    def qtvcp_special_init(self,window):
        self.top_level = window
        self.newParent()

    def box(self):

        #okButton = QPushButton("OK")
        #okButton.pressed.connect(self.changecheck)
        #cancelButton = QPushButton("Cancel")
        self.mb=QLabel('<html><head/><body><p><span style=" font-size:30pt; font-weight:600;">%s</span></p></body></html>'%self.text,self)
        self.mb.setStyleSheet("background-color: black; color: white")
        self.mb.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        #hbox.addWidget(okButton)
        #hbox.addWidget(cancelButton)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.mb)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 300, 150)
        #self.show()

    def changecheck(self):
        print 'hide'
        self.hide()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.colorBackground(qp)
        self.drawText(event, qp)
        qp.end()
        self.mb.setText('<html><head/><body><p><span style=" font-size:30pt; font-weight:600;">%s</span></p></body></html>'%self.text)

    def colorBackground(self, qp):
        qp.fillRect(self.rect(),self.bg_color)

    def drawText(self, event, qp):
        return
        size = self.size()
        w = size.width()
        h = size.height()
        #qp.fillRect(100,100,w/2,h/2,self.dialog_color)
        qp.setPen(self.text_color)
        qp.setFont(self.font)
        qp.drawText(self.rect(), Qt.AlignCenter, self.text)

    @pyqtSlot(bool)
    def setState(self, value):
        self._state = value
        if value:
            self.show()
        else:
            self.hide()

    def getState(self):
        return self._state

    def resetState(self):
        self._state = False

    def getOverayColor(self):
        return self.bg_color

    @pyqtSlot(QColor)
    def setOverayColor(self, value):
        self.bg_color = value
    def resetOverayColor(self, value):
        self.bg_color = value

    overlay_color = pyqtProperty(QColor, getOverayColor, setOverayColor,resetOverayColor)
    state = pyqtProperty(bool, getState, setState, resetState)


def main():
    import sys
    app = QApplication(sys.argv)

    w = QWidget()
    #w.setWindowFlags( Qt.FramelessWindowHint | Qt.Dialog | Qt.WindowStaysOnTopHint )
    w.setGeometry(300, 300, 250, 150)
    w.setWindowTitle('Test')

    l = QLabel('Hello, world!',w)
    l.show()
    print l

    o = LoadingOverlay(l)
    o.setObjectName("overlay")
    w.show()
    #o.show()


    timer2 = QTimer()
    timer2.timeout.connect(lambda : o.show())
    timer2.start(1500)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


