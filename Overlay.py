import sys
import threading

from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QMainWindow, QColorDialog
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QCoreApplication, Qt, QPointO

from pynput import keyboard

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            #stay on top so it always appears visibly when we active with keyboard shortcut
            QtCore.Qt.WindowStaysOnTopHint |
            #we want to have minimal top bar so it looks clean, but still be resizable so not a frameless window
            QtCore.Qt.CustomizeWindowHint
        )

        #initialise starting state
        self.showing = False
        self.dialog = False
        self.loadDefaultColor()

        #set window color, position and size
        self.setStyleSheet("background-color: " + self.color.name() + ";")
        self.setWindowOpacity(self.color.alpha() / 255)
        self.oldPos = self.pos()
        self.setGeometry(0, 0, 500, 500)
        self.center()
        

        #need to show then hide otherwise program just ends if we do nothing
        self.show()
        self.hide()

    #when keyboard shortcut is pressed, show/hide accordingly
    def on_activate(self):
        if self.showing:
            self.hide()
        else:
            self.show()
        self.showing = not self.showing

    #just puts the window in the centre of the screen
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    #called when a colour is selected in the color dialog
    def updateColor(self, color):
        self.show()
        if color.isValid():
            self.setStyleSheet("background-color: "+ color.name()+";")
            self.setWindowOpacity(color.alpha() / 255)
            self.color = color
            self.saveDefaultColor()

    #saves color to settings.txt so it can be restored when program is next ran
    def saveDefaultColor(self):
        with open("settings.txt", "w") as f:
            s = ",".join([str(self.color.alpha()), str(self.color.red()), str(self.color.green()), str(self.color.blue())])
            f.write(s)

    #load most recent colour from last time
    def loadDefaultColor(self):
        with open("settings.txt", "r") as f:
            s = f.read().split(",")
            self.color = QtGui.QColor(int(s[1]), int(s[2]), int(s[3]))
            self.color.setAlpha(int(s[0]))
    
    #when color dialog is rejected (cancel is pressed)
    #need to still reshow the overlay
    def dialogClosed(self):
        self.dialog.done(0)
        self.show()
        self.showing = True

    #when we click on the overlay
    def mousePressEvent(self, event):
        #if left, we are dragging and moving the overlay
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()
        #if right, we open color dialog
        elif event.button() == Qt.RightButton:
            self.hide()
            showing = False

            #initialise and show color dialog, with current colour as default
            self.dialog = QColorDialog(self)
            self.dialog.setStyleSheet("background-color: #dddddd;")
            self.dialog.setOption(QColorDialog.ShowAlphaChannel)
            self.dialog.reject = self.dialogClosed
            self.dialog.setCurrentColor(self.color)
            self.dialog.colorSelected.connect(self.updateColor)
            self.dialog.show()
            
    #when mouse is moved, we move overlay accordingly
    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

#sets up the keyboard shortcut to hide/show overlay
def setup_hotkey(gui):

    #create the hotkey object, set to win+shift+o
    hotkey = keyboard.HotKey(keyboard.HotKey.parse('<cmd>+<shift>+o'), gui.on_activate)

    #from pynput docs, cleans up key modifiers before we pass to the hotkey instance
    def for_canonical(f):
        return lambda k: f(l.canonical(k))

    #create and deploy the keyboard instance
    with keyboard.Listener(
            on_press=for_canonical(hotkey.press),
            on_release=for_canonical(hotkey.release)) as l:
            
            l.join()

def main():
    #creare app and instance of overlay
    app = QApplication(sys.argv)
    app.setStyleSheet("QMainWindow{background-color: darkgray;border: 1px solid black}")

    ex = MainWindow()

    #hot key setup is done in separate thread because the last call in it to listener.join() is blocking
    x = threading.Thread(target=setup_hotkey, args=(ex,))
    x.start()

    #also blocking so done after hotkey setup, runs pyqt app and ends when app ends
    sys.exit(app.exec_())
   
    
if __name__ == '__main__':
    print("Running overlay program...")
    main()
