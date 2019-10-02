import time
from multiprocessing import Process

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5 import QtGui
from functools import partial

class View(QMainWindow):
    #rectChanged = pyqtSignal(QRect)


    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):


        self.statusBar()
        # openFile.setShortcut('Ctrl+O')
        # createProjectMenuBtn.triggered.connect(self.createProject)
        self.openFileMenuBtn = QAction('Open', self)
        self.openFileMenuBtn.setShortcut('Ctrl+O')
        self.openFileMenuBtn.setStatusTip('Open file')
        self.saveFileMenuBtn = QAction('Save', self)
        self.saveFileMenuBtn.setShortcut('Ctrl+S')
        self.saveFileMenuBtn.setStatusTip('Save file')
        self.dumpRulesMenuBtn = QAction('Dump Rules', self)
        self.dumpRulesMenuBtn.setShortcut('Ctrl+R')
        self.dumpRulesMenuBtn.setStatusTip('Dump rules into a txt file')

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(self.openFileMenuBtn)
        fileMenu.addAction(self.saveFileMenuBtn)
        fileMenu.addAction(self.dumpRulesMenuBtn)

        self.gView = graphicsView(parent=self)#QGraphicsView(self.scene, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        #self.gView.setFixedSize(self.gView.scene.width(), self.gView.scene.height())
        #self.gView.move(0,0)
        #self.gView.resize()


        self.tagList_Widget = QListView()
        self.tagList_ListModel = QStandardItemModel(self.tagList_Widget)
        self.tagList_Widget.setModel(self.tagList_ListModel)

        self.fileList_Widget = QListView()
        self.fileList_ListModel = QStandardItemModel(self.fileList_Widget)
        self.fileList_Widget.setModel(self.fileList_ListModel)

        #addTagBox = QHBoxLayout()
        #self.addTag_lineedit = QLineEdit()
        #self.addTag_lineedit.setPlaceholderText("Tag Label")
        #self.addTag_button = QPushButton("Add")
        #addTagBox.addWidget(self.addTag_lineedit,4)
        #addTagBox.addWidget(self.addTag_button,1)

        self.addTag_button = QPushButton("Add")
        self.deleteTag_button = QPushButton("Delete")

        vbox = QVBoxLayout()
        #vbox.addLayout(addTagBox)
        vbox.addWidget(self.tagList_Widget)
        vbox.addWidget(self.addTag_button)
        vbox.addWidget(self.deleteTag_button)
        vbox.addWidget(self.fileList_Widget)


        hbox = QHBoxLayout()
        hbox.addWidget(self.gView,5)
        hbox.addLayout(vbox,1)


        w = QWidget()
        w.setLayout(hbox)
        self.setCentralWidget(w)


        #self.view.setGeometry(0,0, 680, 500)
        #self.setCentralWidget(self.gView)
        #self.gView.setDragMode(QGraphicsView.RubberBandDrag)


        #self.rubberBand = QRubberBand(QRubberBand.Rectangle, self.view)
        #self.scene.addWidget(self.rubberBand)
        #self.view.setMouseTracking(True)
        #self.origin = QPoint()
        #self.changeRubberBand = False

        self.setGeometry(50, 50, 1000, 550)
        self.setWindowTitle('SynEdit')
        self.showMaximized()



    '''
    def mousePressEvent(self, event):
        self.lineItem = QGraphicsLineItem(10, 10, 400, 400)
        self.lineItem.setPen(QPen(QColor("black"), 2, Qt.SolidLine, Qt.SquareCap, Qt.RoundJoin, ))
        self.gView.scene.addItem(self.lineItem)
    '''

    def addTag(self):
        dialog = AddTagDialog()
        if dialog.exec():
            label, desc = dialog.getInputs()
            self.addToTagList((label, desc))
            self.gView.updateLabels(label)
            return label


    def addToFileList(self, fileInfo):
        item = QStandardItem(fileInfo[0])
        item.setEditable(False)
        item.setDropEnabled(False)
        if fileInfo[1] == "1":#valid
            item.setBackground(QBrush(QColor(0, 255, 0)))
        elif fileInfo[1] == "2":#incomplete
            item.setBackground(QBrush(QColor(255, 255, 0)))
        elif fileInfo[1] == "3":#unk NT
            item.setBackground(QBrush(QColor(255, 0, 0)))
        self.fileList_ListModel.appendRow(item)
        return item

    def updateFileStatus(self, fIndex, stat):
        if stat == "1":
            self.fileList_ListModel.item(fIndex).setBackground(QBrush(QColor(0, 255, 0)))
        elif stat == "2":
            self.fileList_ListModel.item(fIndex).setBackground(QBrush(QColor(255, 255, 0)))
        elif stat == "3":
            self.fileList_ListModel.item(fIndex).setBackground(QBrush(QColor(255, 0, 0)))

    def addToTagList(self, tag, tt = "Verbal Stem"):
        item = QStandardItem(tag[0])
        item.setEditable(False)
        item.setDropEnabled(False)
        #btn = QPushButton("Del")
        item.setToolTip(tag[1])
        #q = QWidget()
        #l = QHBoxLayout(q)
        #l.addWidget(btn, alignment=Qt.AlignRight)
        #l.setContentsMargins(0, 0, 0, 0)
        self.tagList_ListModel.appendRow(item)
        #self.tagList_Widget.setIndexWidget(item.index(),q)
        #btn.clicked.connect(partial(self.deleteTag, item.index()))

    def deleteTag(self):
        deleted = self.tagList_Widget.selectedIndexes()[0].row()
        deletedItem = self.tagList_ListModel.item(deleted).text()
        self.tagList_ListModel.removeRow(deleted)
        return deletedItem

    def showFileDialog(self):
        return QFileDialog.getExistingDirectory(self, 'Select Directory')

    def dummyAction(self):
        print("ACTİON")

    def showWarning(self, message):
        QMessageBox.about(self, "Warning", message)

class AddTagDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add Tag")
        self.first = QLineEdit(self)
        self.second = QLineEdit(self)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self);

        layout = QFormLayout(self)
        layout.addRow("Tag Label", self.first)
        layout.addRow("Tag Description", self.second)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def getInputs(self):
        return (self.first.text(), self.second.text())

class GroupHatWidget(QWidget):

    def __init__(self, a, h, bl, tl, tr, br):
        super().__init__(a)
        self.height = h
        self.bottomLeft = bl
        self.topLeft = tl
        self.topRight = tr
        self.bottomRight = br

    def paintEvent(self, event):
        self.painter = QPainter(self)
        self.path = QPainterPath()
        self.painter.begin(self)
        self.painter.setRenderHint(QPainter.Antialiasing)
        self.painter.setPen(QPen(Qt.black,  3, Qt.SolidLine))
        self.path.moveTo(self.bottomLeft.x() - 5, self.bottomLeft.y() - self.height / 2)
        self.path.lineTo(self.topLeft.x() - 5, self.topLeft.y() - 2)
        self.path.lineTo(self.topRight.x() + 5, self.topRight.y() - 2)
        self.path.lineTo(self.bottomRight.x() + 5, self.bottomRight.y() - self.height / 2)
        self.painter.translate(-self.path.boundingRect().topLeft())
        self.painter.drawPath(self.path)
        self.painter.end()

class TokenAreaWidget(QWidget):

    def __init__(self, a, x, y, w, h):
        super().__init__(a)
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.transparent)
        # Color Effect
        for i in range(0, 100):
            painter.setBrush(QColor(255 - i, 255 - i, 255 - i))
            #painter.setBrush(QColor(i * 2, 0, 0))
            painter.drawRect(self.x, 0+(i*round(self.h/100)), 10000, round(self.h/100))

class Node:

    def __init__(self, label=None, group=None, parent_view=None):
        self.labelWidget = label
        self.group = group
        self.children = list()
        self.viewParent = parent_view

        self.LMA_x = 0
        self.LMA_y = 0

        #self.groupArea.move(70,70)
        #self.widget.mouseReleaseEvent = lambda event, my_variable: self.myfunction(event, my_variable)

        if group is not None:
            xStart = self.labelWidget.geometry().x()
            if xStart > self.group.selectedlabel_list[0][1].geometry().topLeft().x():
                xStart = self.group.selectedlabel_list[0][1].geometry().topLeft().x()
            xEnd = self.labelWidget.geometry().bottomRight().x()
            if xEnd < self.group.selectedlabel_list[len(self.group.selectedlabel_list) - 1][1].geometry().bottomRight().x():
                xEnd = self.group.selectedlabel_list[len(self.group.selectedlabel_list) - 1][1].geometry().bottomRight().x()
            self.groupArea = GroupAreaWidget(
                QPoint(xStart - 5, self.labelWidget.geometry().y() - 5),
                QPoint(xEnd+5,
                       self.group.selectedlabel_list[len(self.group.selectedlabel_list) - 1][1].geometry().bottomRight().y() + 5),
                        parent=parent_view)
        else:
            self.groupArea = GroupAreaWidget(
                QPoint(self.labelWidget.geometry().topLeft().x()-5, self.labelWidget.geometry().topLeft().y()-15),
                QPoint(self.labelWidget.geometry().bottomRight().x()+5, self.labelWidget.geometry().bottomRight().y()+5),
                    parent=parent_view
            )

        self.level = self.groupArea.tlY
        self.viewParent.scene.addItem(self.groupArea.rectItem)

    def addChild(self, c):
        line = Line(self.labelWidget.geometry().x() + round(self.labelWidget.geometry().width()/2),
                    self.labelWidget.geometry().bottomRight().y()+5,
                    c.labelWidget.geometry().x() + round(c.labelWidget.geometry().width() / 2),
                    c.labelWidget.geometry().y() - 5, parent=self.viewParent)
        self.viewParent.scene.addItem(line.lineItem)
        self.children.append([line, c])

    def delete(self):
        self.labelWidget.setParent(None)
        self.viewParent.scene.removeItem(self.labelWidget.graphicsProxyWidget())
        self.labelWidget = None

        self.viewParent.scene.removeItem(self.groupArea.rectItem)
        self.groupArea = None

        if self.group is not None:
            self.group.hat_widget.setParent(None)
            self.viewParent.scene.removeItem(self.group.hat_widget.graphicsProxyWidget())
            self.group.hat_widget = None
            self.group.selectedlabel_list.clear()
            self.group = None

        for c in self.children:
            self.viewParent.scene.removeItem(c[0].lineItem)
            self.viewParent.group_list.append(c[1])

        self.children.clear()
        self.viewParent = None

    def move(self, dx, dy, anim=True):
        self.LMA_x = dx
        self.LMA_y = dy
        duration = 1000
        if self.group is not None:
            groupAnim = self.group.move(dx, dy, anim=anim)
            for ga in groupAnim:
                self.viewParent.treeAnimations.addAnimation(ga)

        if anim:
            anim_label = QPropertyAnimation(self.labelWidget, b"geometry")
            anim_label.setDuration(duration)
            anim_label.setStartValue(self.labelWidget.geometry())
            anim_label.setEndValue(
                QRect(self.labelWidget.geometry().x() + dx, self.labelWidget.geometry().y() + dy,
                      self.labelWidget.geometry().width(), self.labelWidget.geometry().height()))
            self.viewParent.treeAnimations.addAnimation(anim_label)
        else:
            self.labelWidget.move(self.labelWidget.geometry().x() + dx, self.labelWidget.geometry().y() + dy)
        self.groupArea.move(dx, dy, anim=anim)

    def getSelectedLabels(self):
        if self.group is not None:
            surfAbs = list()
            for duo in self.group.selectedlabel_list:
                surfAbs.append([duo[0].text(), duo[1].text()])
            return surfAbs

class GroupView:

    def __init__(self, sl, h, ti, gei):
        self.selectedlabel_list = sl
        self.hat_widget = h
        self.token_index = ti
        self.end_index = gei

    def move(self, displacementX, displacementY, anim=True):
        s = list()
        if anim:
            duration = 1000
            animation = QPropertyAnimation(self.hat_widget, b"geometry")
            animation.setDuration(duration)
            animation.setStartValue(self.hat_widget.geometry())
            animation.setEndValue(
                QRect(self.hat_widget.geometry().x()+displacementX, self.hat_widget.geometry().y()+displacementY,
                      self.hat_widget.geometry().width(), self.hat_widget.geometry().height()))
            s.append(animation)

            for sl in self.selectedlabel_list:
                animation = QPropertyAnimation(sl[0], b"geometry")
                animation.setDuration(duration)
                animation.setStartValue(sl[0].geometry())
                animation.setEndValue(
                    QRect(sl[0].geometry().x() + displacementX,
                          sl[0].geometry().y() + displacementY,
                          sl[0].geometry().width(),sl[0].geometry().height()))
                s.append(animation)

                animation = QPropertyAnimation(sl[1], b"geometry")
                animation.setDuration(duration)
                animation.setStartValue(sl[1].geometry())
                animation.setEndValue(
                    QRect(sl[1].geometry().x() + displacementX,
                          sl[1].geometry().y() + displacementY,
                          sl[1].geometry().width(), sl[1].geometry().height()))
                s.append(animation)
        else:
            self.hat_widget.move(self.hat_widget.geometry().x()+displacementX, self.hat_widget.geometry().y()+displacementY)
            for sl in self.selectedlabel_list:
                sl[0].move(sl[0].geometry().x() + displacementX,sl[0].geometry().y() + displacementY)
                sl[1].move(sl[1].geometry().x() + displacementX, sl[1].geometry().y() + displacementY)

        return s

class Line(QObject):

    def __init__(self, x1, y1, x2, y2, parent=None):
        super(Line, self).__init__(parent)
        self.lineF = QLineF()
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.lineItem = QGraphicsLineItem(x1, y1, x2, y2)
        self.lineItem.setPen(QPen(QColor("black"),2, Qt.SolidLine, Qt.SquareCap, Qt.RoundJoin,))
        self.viewParent = parent

    def p1(self):
        return self.lineF.p1()

    def setP1(self, p1):
        self.lineF.setP1(p1)
        self.lineItem.setLine(self.lineF)

    def moveP1(self, dx, dy):
        b = QPropertyAnimation(
            self,
            b"p1",
            parent=self,
            startValue=QPointF(self.x1, self.y1),
            endValue=QPointF(self.x1+dx, self.y1+dy),
            duration=1000,
        )
        self.viewParent.treeAnimations.addAnimation(b)
        a = QPropertyAnimation(
            self,
            b"p2",
            parent=self,
            startValue=QPointF(self.x2, self.y2),
            endValue=QPointF(self.x2, self.y2),
            duration=1000,
        )
        self.x1 = self.x1+dx
        self.y1 = self.y1+dy
        #self.viewParent.treeAnimations.addAnimation(aa)
        self.viewParent.treeAnimations.addAnimation(a)

    def p2(self):
        return self.lineF.p2()

    def setP2(self, p2):
        self.lineF.setP2(p2)
        self.lineItem.setLine(self.lineF)

    def moveP2(self, dx, dy, anim=True):
        if anim:
            b = QPropertyAnimation(
                self,
                b"p1",
                parent=self,
                startValue=QPointF(self.x1, self.y1),
                endValue=QPointF(self.x1, self.y1),
                duration=1000,
            )
            self.viewParent.treeAnimations.addAnimation(b)
            a = QPropertyAnimation(
                self,
                b"p2",
                parent=self,
                startValue=QPointF(self.x2, self.y2),
                endValue=QPointF(self.x2+dx, self.y2+dy),
                duration=1000,
            )

            self.viewParent.treeAnimations.addAnimation(a)
        else:
            self.setP1(QPointF(self.x1, self.y1))
            self.setP2(QPointF(self.x2+dx, self.y2+dy))
        self.x2 = self.x2 + dx
        self.y2 = self.y2 + dy


    p1 = QtCore.pyqtProperty(QPointF, fget=p1, fset=setP1)
    p2 = QtCore.pyqtProperty(QPointF, fget=p2, fset=setP2)

    def move(self, dx, dy, anim=True):
        if anim:
            b = QPropertyAnimation(
                self,
                b"p1",
                parent=self,
                startValue=QPointF(self.x1, self.y1),
                endValue=QPointF(self.x1 + dx, self.y1 + dy),
                duration=1000,
            )
            self.viewParent.treeAnimations.addAnimation(b)
            a = QPropertyAnimation(
                self,
                b"p2",
                parent=self,
                startValue=QPointF(self.x2, self.y2),
                endValue=QPointF(self.x2+dx, self.y2+dy),
                duration=1000,
            )
            self.viewParent.treeAnimations.addAnimation(a)

        else:
            self.setP1(QPointF(self.x1 + dx, self.y1 + dy))
            self.setP2(QPointF(self.x2+dx, self.y2+dy))
        self.x1 = self.x1 + dx
        self.y1 = self.y1 + dy
        self.x2 = self.x2 + dx
        self.y2 = self.y2 + dy

class GroupAreaWidget(QObject):
    def __init__(self, tl, br, parent=None):
        super(GroupAreaWidget, self).__init__(parent)
        #self.setGeometry(QRect(tl,br))
        self.rectF = QRectF()
        self.rectItem = QGraphicsRectItem(QRectF(QRect(tl,br)))
        self.rectItem.setPen(QPen(QColor("black"),1, Qt.SolidLine, Qt.SquareCap, Qt.RoundJoin,))
        self.tlX = tl.x()
        self.tlY = tl.y()
        self.brX = br.x()
        self.brY = br.y()
        self.viewParent = parent
        #self.rectItem.setBrush(QBrush(QColor("lightRed")))
        #self.setWindowOpacity(0)

    def tl(self):
        return self.rectF.topLeft()

    def setTL(self, p1):
        self.rectF.setTopLeft(p1)
        self.rectItem.setRect(self.rectF)

    def br(self):
        return self.rectF.bottomRight()

    def setBR(self, p2):
        self.rectF.setBottomRight(p2)
        self.rectItem.setRect(self.rectF)

    def move(self, dx, dy, anim=True):
        if anim:
            b = QPropertyAnimation(
                self,
                b"tl",
                parent=self,
                startValue=QPointF(self.tlX, self.tlY),
                endValue=QPointF(self.tlX+dx, self.tlY+dy),
                duration=1000,
            )
            self.viewParent.treeAnimations.addAnimation(b)
            a = QPropertyAnimation(
                self,
                b"br",
                parent=self,
                startValue=QPointF(self.brX, self.brY),
                endValue=QPointF(self.brX + dx, self.brY + dy),
                duration=1000,
            )
            # self.viewParent.treeAnimations.addAnimation(aa)
            self.viewParent.treeAnimations.addAnimation(a)
        else:
            self.setTL(QPointF(self.tlX+dx, self.tlY+dy))
            self.setBR(QPointF(self.brX + dx, self.brY + dy))

        self.tlX = self.tlX + dx
        self.tlY = self.tlY + dy
        self.brX = self.brX + dx
        self.brY = self.brY + dy
    tl = QtCore.pyqtProperty(QPointF, fget=tl, fset=setTL)
    br = QtCore.pyqtProperty(QPointF, fget=br, fset=setBR)

class graphicsView(QGraphicsView):
    rectChanged = pyqtSignal(QRect)

    def __init__ (self, parent=None):
        super(graphicsView, self).__init__ (parent)
        self.p = parent
        self.shiftPressed = False
        self.initialTokenLabel_list = list() # list of primal words
        self.initialTokenLabel_defaultPos = list()
        self.tokenButton_list = list() # list of analysis selection buttons
        self.tokenAreaList = list()
        self.childTokenLabel_list = list() # list of fragmented words
        self.groupIndex_list = list()
        self.group_list = list() #list of non-parented nodes + most-grand parents
        self.selectedNode_list = list() # list to use in parent creation
        self.treeAnimations = QParallelAnimationGroup()
        self.tokenAnimations = QParallelAnimationGroup()
        #self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        #self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)



        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 500, 500)
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.setScene(self.scene)


        #self.t = GroupAreaWidget(QPoint(0, ), QPoint(500, 100), parent=self)
        #self.scene.addItem(self.t.rectItem)
        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.setMouseTracking(True)
        self.origin = QPoint()
        self.changeRubberBand = False

    def mousePressEvent(self, event):
        if self.shiftPressed == False:
            if event.button() == Qt.LeftButton:
                self.origin = event.pos()
                self.rubberBand.setGeometry(QRect(self.origin, QSize()))
                self.rectChanged.emit(self.rubberBand.geometry())
                self.rubberBand.show()
                self.changeRubberBand = True
            else:
                self.deleteNode(event)
        else:
            self.selectNode(event)

    def mouseMoveEvent(self, event):
        if self.changeRubberBand:
            self.rubberBand.setGeometry(QRect(self.origin, event.pos()).normalized())
            self.rectChanged.emit(self.rubberBand.geometry())
            QGraphicsView.mouseMoveEvent(self, event)
            super(graphicsView, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.shiftPressed == False and event.button() == Qt.LeftButton:
            self.changeRubberBand = False
            selectedLabels, token_index, group_end_index = self.findIntersected()
            self.createGroup(selectedLabels, token_index, group_end_index)
            QGraphicsView.mouseReleaseEvent(self, event)
            self.rubberBand.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Shift or event.key() == Qt.Key_Control:
            self.shiftPressed = True

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Shift and len(self.selectedNode_list) > 0:
            self.createParent()
        elif event.key() == Qt.Key_Control and len(self.selectedNode_list) == 2:
            self.connect_to_parent()
        self.selectedNode_list.clear()
        self.shiftPressed = False




    def deleteNode(self, event):
        g = ""
        for g in self.group_list:
            if g.groupArea.rectItem.contains(event.pos()):
                self.treeAnimations.clear()
                for c in g.children:
                    dx = 0
                    dy =c[1].LMA_y*-1
                    c[1].move(dx, dy)
                    self.moveChildrenRec(c[1].children, dx, dy)
                if g.group is not None:
                    self.groupIndex_list[g.group.token_index].remove(g.group.end_index)
                g.delete()
                self.treeAnimations.start()
                self.group_list.remove(g)
                break
        g = None

    def addLabels(self, cBox):
        cBox.addItem("Select")
        for i in range(0,self.p.tagList_ListModel.rowCount()):
            item = self.p.tagList_ListModel.item(i)
            cBox.addItem(item.text())

    def updateLabels(self, added=None, deleted=None):
        if added is not None:
            for n in self.group_list:
                n.labelWidget.addItem(added)
                if len(n.children) > 0:
                    self.addLabelRec(added, n)
        elif deleted is not None:
            return

    def addLabelRec(self, added, n):
        for c in n.children:
            c[1].labelWidget.addItem(added)
            self.addLabelRec(added, c[1])

    def findLeaf(self, node):
        for g_view in self.group_list:
            if  g_view.group is None :
                continue
            labels_of_g = g_view.group.selectedlabel_list
            i = 0
            check = True
            while i < len(node.data):
                if node.data[i][0] != labels_of_g[i][0].text() or node.data[i][1] != labels_of_g[i][1].text():
                    check = False
                    break
                i += 1
            if check:
                label_index = g_view.labelWidget.findText(node.label, Qt.MatchFixedString)
                if label_index >= 0:
                    g_view.labelWidget.setCurrentIndex(label_index)
                return g_view
        return None

    def createParentFromModel(self, childrenList, label):
        for c in childrenList:
            self.selectedNode_list.append(c)
        p = self.createParent(anim=False)
        label_index = p.labelWidget.findText(label, Qt.MatchFixedString)
        if label_index >= 0:
            p.labelWidget.setCurrentIndex(label_index)
        self.selectedNode_list.clear()
        return p

    def createParent(self, anim = True):
        self.treeAnimations.clear()
        label = QComboBox(self)
        self.addLabels(label)
        #label.addItems(["NS","VS","TPMG","CMG","ACCM","VMG","DNG","DVG","NPS","NP","VPS","VP","NPC","NPACC","ADV","S"])
        label.adjustSize()
        #label.move(100, 40)
        x,y = self.calculateParentLocation()
        label.move(x, y)
        self.scene.addWidget(label)
        label.show()

        parent = Node(label=label, parent_view=self)
        #parent.groupArea.mouseReleaseEvent = lambda event, parent: self.selectNode(event, parent)
        for n in self.selectedNode_list:
            self.group_list.remove(n)
            parent.addChild(n)
            n.groupArea.rectItem.setPen(QPen(QColor("black"), 1, Qt.SolidLine, Qt.SquareCap, Qt.RoundJoin, ))

        self.group_list.append(parent)
        self.moveChildren(parent, anim=anim)
        if anim:
            self.treeAnimations.start()
        return parent

    def connect_to_parent(self, anim=True):
        parent = self.selectedNode_list[1]
        parent.groupArea.rectItem.setPen(QPen(QColor("black"), 1, Qt.SolidLine, Qt.SquareCap, Qt.RoundJoin, ))
        self.selectedNode_list.remove(parent)

        self.treeAnimations.clear()
        self.group_list.remove(self.selectedNode_list[0])
        parent.addChild(self.selectedNode_list[0])
        self.moveChildren(parent, anim=anim)
        if anim:
            self.treeAnimations.start()

    def calculateParentLocation(self):
        x = 0
        y = 0

        #find min x
        min_x = self.selectedNode_list[0].labelWidget.geometry().topLeft().x()
        max_x = self.selectedNode_list[0].labelWidget.geometry().topRight().x()
        min_y = self.selectedNode_list[0].labelWidget.geometry().topLeft().y()
        for n in self.selectedNode_list:
            if min_x > n.labelWidget.geometry().topLeft().x():
                min_x = n.labelWidget.geometry().topLeft().x()

            if max_x < n.labelWidget.geometry().topRight().x():
                max_x = n.labelWidget.geometry().topRight().x()

            if min_y > n.labelWidget.geometry().topLeft().y():
                min_y =  n.labelWidget.geometry().topLeft().y()

        x = min_x + round((max_x-min_x)/2)
        y = min_y - 100

        return x,y

    def moveChildren(self, n, anim = True):
        moveRequired = False
        #firstChild_y = n.children[0][1].labelWidget.geometry().y()
        firstChild_y = n.children[0][1].groupArea.tlY
        for c in n.children:
            if c[1].groupArea.tlY != firstChild_y:
                moveRequired = True
                break
        if moveRequired:
            min_y = firstChild_y
            for c in n.children:
                if c[1].groupArea.tlY < min_y:
                    min_y = c[1].groupArea.tlY

            dx = 0
            for c in n.children:
                dy = min_y - c[1].groupArea.tlY
                c[0].moveP2(dx, dy, anim=anim)
                c[1].move(dx, dy, anim=anim)
                self.moveChildrenRec(c[1].children, dx, dy, anim=anim)

    def moveChildrenRec(self, children, dx, dy, anim=True):
        for c in children:
            c[0].move(dx, dy, anim=anim)
            c[1].move(dx, dy, anim=anim)
            self.moveChildrenRec(c[1].children, dx, dy, anim=anim)

    def selectNode(self, event):
        for g in self.group_list:
            if g.groupArea.rectItem.contains(event.pos()) and g not in self.selectedNode_list:
                #print(g)
                g.groupArea.rectItem.setPen(QPen(QColor("red"), 1, Qt.SolidLine, Qt.SquareCap, Qt.RoundJoin, ))
                self.selectedNode_list.append(g)
            #else:
                #print(event.pos())
                #print(self.mapToScene(g.groupArea.rect()).boundingRect())

    def createGroup(self, selectedlabels, token_index,  group_end_index):
        if len(selectedlabels) != 0:
            hat = self.drawGroupHat(selectedlabels)
            label = self.putGroupLabel(hat)
            group = GroupView(selectedlabels, hat, token_index, group_end_index)
            node = Node(label=label,group=group, parent_view=self)
            self.group_list.append(node)

    def createGroupByIndex(self, token, start, end, anim=True):
        selecteedLabels = list()
        for i in range(start, end+1):
            selecteedLabels.append(self.childTokenLabel_list[token][i])
        self.createGroup(selecteedLabels, token, end)

    def putGroupLabel(self, hat):
        label = QComboBox(self)
        #label.addItems(["NS","VS","TPMG","CMG","ACCM","VMG","DNG","DVG","NPS","NP","VPS","VP","NPC","NPACC","ADV","S"])
        self.addLabels(label)
        label.adjustSize()
        hatGeo = hat.geometry()
        label.move(hatGeo.topLeft().x()+round(hatGeo.width()/2)-round(label.geometry().width()/2), hatGeo.topLeft().y()-label.geometry().height()-5)
        self.scene.addWidget(label)
        label.show()
        return label

    def drawGroupHat(self, selectedLabels):
        if len(selectedLabels) == 0:
            return 0

        height =selectedLabels[0][0].geometry().height()
        bottomLeft = selectedLabels[0][0].geometry().bottomLeft()
        topLeft = selectedLabels[0][0].geometry().topLeft()
        topRight =  selectedLabels[len(selectedLabels)-1][0].geometry().topRight()
        bottomRight =  selectedLabels[len(selectedLabels)-1][0].geometry().bottomRight()


        hat = GroupHatWidget(self, height, bottomLeft, topLeft, topRight, bottomRight)
        hat.move(topLeft.x()-5, topLeft.y()-2)
        hat.resize(topRight.x()-topLeft.x()+10, bottomRight.y()-topRight.y())
        self.scene.addWidget(hat)
        hat.show()
        self.scene.update()
        return hat

    def findIntersected(self):
        intersected = list()
        check = False
        max_index = 0
        token_index = 0
        for token_index in range(0, len(self.childTokenLabel_list)):
            for c in self.childTokenLabel_list[token_index]:
                surface_label = c[0]
                if not self.rubberBand.geometry().intersected(surface_label.geometry()).isEmpty():
                    intersected.append(c)
                    check = True
                    index = self.childTokenLabel_list[token_index].index(c)
                    if index > max_index:
                        max_index = index

            if check:
                self.groupIndex_list[token_index].append(max_index)
                self.groupIndex_list[token_index].sort()
                break

        return intersected, token_index, max_index

    def addTokenArea(self, label, btn):
        # print(label.geometry().topLeft().x())
        w = btn.geometry().topRight().x() - label.geometry().topLeft().x() + 10
        h = btn.geometry().bottomLeft().y() + 5
        ta = TokenAreaWidget(self, 0, 0, w, h)

        ta.move(label.geometry().topLeft().x() - 5, 20)
        ta.resize(w, h)
        # print(ta.geometry().topLeft().x())
        self.scene.addWidget(ta)
        ta.show()
        # ta.stackUnder(label)
        ta.lower()
        self.scene.update()
        self.tokenAreaList.append(ta)

    def initializeTokens(self, tokens):
        token_x = 50
        token_y = self.height() - 50
        menu_list = list()
        for token in tokens:
            token_label = QLabel(self)
            self.initialTokenLabel_list.append(token_label)
            self.childTokenLabel_list.append(list())
            self.groupIndex_list.append(list())
            token_label.setText(token[0])
            token_label.move(token_x, token_y)
            token_label.adjustSize()
            self.initialTokenLabel_defaultPos.append([token_label.pos().x(), token_label.pos().y()])
            pushbutton = QPushButton(self)
            self.tokenButton_list.append(pushbutton)
            button_x = token_x + token_label.geometry().width() + 10
            button_y = token_label.pos().y()
            pushbutton.move(button_x, button_y)
            pushbutton.resize(20, 20)
            token_x = button_x + pushbutton.geometry().width() + 10
            menu = QMenu()
            menu_list.append(menu)
            pushbutton.setMenu(menu)
            self.scene.addWidget(token_label)
            token_label.show()
            self.scene.addWidget(pushbutton)
            pushbutton.show()
            self.addTokenArea(token_label, pushbutton)
            self.scene.update()

        for token in tokens:
            if len(token[1]) > 0 and len(token[2]) > 0:
                self.updateTokens(tokens.index(token), token[2], token[1], anim=False)

        return menu_list

    def updateTokens(self, token_id, surface, abstract, anim=True):
        old_end = self.tokenButton_list[token_id].pos().x() + self.tokenButton_list[token_id].geometry().width() - 10
        if len(self.childTokenLabel_list[token_id]) > 0:
            for c in self.childTokenLabel_list[token_id]:
                c[0].setParent(None)
                c[1].setParent(None)
                old_end = c[1].pos().x() + c[1].geometry().width() - 10
            self.childTokenLabel_list[token_id].clear()

        initialToken_label = self.initialTokenLabel_list[token_id]
        x = self.initialTokenLabel_defaultPos[token_id][0]
        y = self.initialTokenLabel_defaultPos[token_id][1]
        children = list()
        for i in range(0, len(surface)):
            if surface[i] != "":
                abs_label = QLabel(self)
                abs_label.setText(abstract[i])
                abs_label.move(x, y - 30)
                abs_label.adjustSize()
                self.scene.addWidget(abs_label)
                abs_label.show()

                surface_label = QLabel(self)
                if i == 0:
                    surface_label.setText(surface[i])
                else:
                    surface_label.setText("-" + surface[i])
                surface_label.adjustSize()
                surface_label.move(abs_label.geometry().x() + int(abs_label.geometry().width() / 2)-int(surface_label.geometry().width()/2), y - 50)

                self.scene.addWidget(surface_label)
                surface_label.show()

                children.append([surface_label, abs_label])

                x = x + abs_label.geometry().width() + 20

        self.childTokenLabel_list[token_id] = children

        token_displacementX = int(
            (x - 10 - self.initialTokenLabel_defaultPos[token_id][0] - initialToken_label.geometry().width()) / 2) - (
                              initialToken_label.pos().x() - self.initialTokenLabel_defaultPos[token_id][
                                  0])  # int((x-10 - initialToken_label.pos().x())/4)
        token_displacementY = 0  # self.initialTokenLabel_defaultPos[token_id][1]-initialToken_label.pos().y()+40
        rest_displacementX = x - old_end


        self.moveElement(initialToken_label, token_displacementX, token_displacementY, anim=anim)
        self.moveElement(self.tokenButton_list[token_id], token_displacementX, 0, anim=anim)
        self.resizeElement(self.tokenAreaList[token_id], rest_displacementX, 0, anim=anim)
        for i in range(token_id + 1, len(self.initialTokenLabel_list)):
            self.initialTokenLabel_defaultPos[i][0] += rest_displacementX
            self.moveElement(self.initialTokenLabel_list[i], rest_displacementX, 0, anim=anim)
            self.moveElement(self.tokenButton_list[i], rest_displacementX, 0, anim=anim)
            self.moveElement(self.tokenAreaList[i], rest_displacementX, 0, anim=anim)
            for c in self.childTokenLabel_list[i]:
                self.moveElement(c[0], rest_displacementX, 0, anim=anim)
                self.moveElement(c[1], rest_displacementX, 0, anim=anim)

    def moveElement(self, element, amountX, amountY, anim=True):
        # element.move(newX, newY)
        geo = element.geometry()
        if anim:
            animation = QPropertyAnimation(element, b"geometry")
            animation.setDuration(1000)
            animation.setStartValue(geo)
            animation.setEndValue(QRect(geo.x() + amountX, geo.y() + amountY, geo.width(), geo.height()))
            self.tokenAnimations.addAnimation(animation)
        else:
            element.move(geo.x() + amountX, geo.y() + amountY)
        # self.animation.start()

    def resizeElement(self, element, amountW, amounthH, anim=True):
        geo = element.geometry()
        if anim:
            self.animation = QPropertyAnimation(element, b"geometry")
            self.animation.setDuration(1000)
            self.animation.setStartValue(geo)
            self.animation.setEndValue(QRect(geo.x(), geo.y(), geo.width() + amountW, geo.height() + amounthH))
            self.tokenAnimations.addAnimation(self.animation)
        else:
            element.resize(geo.width() + amountW, geo.height() + amounthH)

    def clearScene(self):
        for n in self.group_list:
            n.delete()
        print(self.childTokenLabel_list)
        for token in self.childTokenLabel_list:
            for c in token:
                self.scene.removeItem(c[0].graphicsProxyWidget())
                c[0].setParent(None)
                self.scene.removeItem(c[1].graphicsProxyWidget())
                c[1].setParent(None)
        self.childTokenLabel_list.clear()
        for token in self.initialTokenLabel_list:
            self.scene.removeItem(token.graphicsProxyWidget())
            token.setParent(None)
        self.initialTokenLabel_list.clear()
        for btn in self.tokenButton_list:
            self.scene.removeItem(btn.graphicsProxyWidget())
            btn.setParent(None)
        self.tokenButton_list.clear()
        self.group_list.clear()
        self.groupIndex_list.clear()
        self.initialTokenLabel_defaultPos.clear()


