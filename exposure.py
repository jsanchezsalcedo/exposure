import maya.cmds as cmds
from maya import OpenMayaUI as omui

from PySide2 import QtCore, QtWidgets
import shiboken2 as shiboken

mainWindow = None
__title__ = 'Exposure'
__version__ = 'v2.1.0'

print ' '
print ' > You have openned {} {} successfully.'.format(__title__,__version__)
print ' '

lightTypes = [
    'aiAreaLight',
    'aiSkyDomeLight',
    'aiPhotometricLight',
    'aiLightPortal',
    'ambientLight',
    'areaLight',
    'directionalLight',
    'pointLight',
    'spotLight',
    'volumeLight'
]

def getMainWindow():
    ptr = omui.MQtUtil.mainWindow()
    mainWindow = shiboken.wrapInstance(long(ptr), QtWidgets.QMainWindow)
    return mainWindow

class exposure(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(exposure, self).__init__(parent)
        self.setWindowTitle('{} {}'.format(__title__, __version__))
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setFixedWidth(225)
        self.createUI()

    def createUI(self):
        self.mainWidget = QtWidgets.QWidget()
        self.mainLayout = QtWidgets.QVBoxLayout(self.mainWidget)

        expLyt = QtWidgets.QGridLayout()
        plusExpLbl = QtWidgets.QLabel('Plus Exposure')
        plusExpLbl.setFixedWidth(90)
        expLyt.addWidget(plusExpLbl, 0, 0)
        self.plusExpLe = QtWidgets.QLineEdit('0.0')
        self.plusExpLe.setFixedWidth(110)
        expLyt.addWidget(self.plusExpLe, 0, 1)
        minExpLbl = QtWidgets.QLabel('Min Exposure')
        minExpLbl.setFixedWidth(90)
        expLyt.addWidget(minExpLbl, 1, 0)
        self.minExpLe = QtWidgets.QLineEdit('0.0')
        self.minExpLe.setFixedWidth(110)
        expLyt.addWidget(self.minExpLe, 1, 1)

        actionLyt = QtWidgets.QHBoxLayout()
        applyBtn = QtWidgets.QPushButton('Apply')
        actionLyt.addWidget(applyBtn)
        cancelBtn = QtWidgets.QPushButton('Cancel')
        actionLyt.addWidget(cancelBtn)

        self.mainLayout.addLayout(expLyt)
        self.mainLayout.addLayout(actionLyt)
        
        self.setLayout(self.mainLayout)

        applyBtn.clicked.connect(self.setVal)
        cancelBtn.clicked.connect(self.cancel)

    def setVal(self):
        plusValue = float(self.plusExpLe.text())
        minValue = float(self.minExpLe.text())

        for light in cmds.ls(sl=True, dag=True, typ=lightTypes):
            exposure = float(cmds.getAttr(light + '.aiExposure'))
            plusExposure = exposure + plusValue
            minExposure = exposure - minValue

            if plusExposure > exposure:
                cmds.setAttr(light + '.aiExposure', plusExposure)
                self.plusExpLe.setText(unicode(plusValue))
                self.close()

            elif minExposure < exposure:
                cmds.setAttr(light + '.aiExposure', minExposure)
                self.minExpLe.setText(unicode(minValue))
                self.close()
            else:
                print 'There is not new exposure value added for', light.getParent()


    def cancel(self):
        self.close()

def run():
    global mainWindow

    if not mainWindow or not cmds.window(mainWindow, q=True, e=True):
        mainWindow = exposure(parent=getMainWindow())

    mainWindow.show()
    mainWindow.raise_()
