import json
import os
import subprocess
import sys

import requests
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication

from Model import Model
from View import View


class Controller:

    def run(self):
        app = QApplication(sys.argv)
        self.createDummy = False
        self.view = View()
        self.connectViewActions()
        self.model = Model()
        self.testServiceConnection()
        sys.exit(app.exec_())

    def connectViewActions(self):
        self.view.openFileMenuBtn.triggered.connect(self.openFile)
        self.view.addTag_button.clicked.connect(self.addTagAction)
        self.view.deleteTag_button.clicked.connect(self.deleteTagAction)
        self.view.fileList_Widget.doubleClicked.connect(self.loadFile)
        self.view.saveFileMenuBtn.triggered.connect(self.save)
        self.view.dumpRulesMenuBtn.triggered.connect(self.dumpRules)

    def testServiceConnection(self):
        try:
            input = {}
            input["wordList"] = ["a"]
            json_data = json.dumps(input, ensure_ascii=False)
            r = requests.post("http://ddil.isikun.edu.tr/syneditws/", json_data.encode('utf-8'), timeout=10)
            response = r.json()
        except :
            self.view.showWarning("Analyzer server is offline.")

    def dumpRules(self):
        self.model.generateRuleStats()

    #combobox->itemData(combobox->currentIndex())

    def save(self):
        indexList = self.view.gView.groupIndex_list
        print(indexList)
        if len(indexList[0]) != 0:
            self.model.updateIndexes(indexList)
            self.model.roots.clear()
            self.generateTreeModel()
            self.model.saveToFile()
            self.model.saveConfig()
            i,s = self.model.get_current_file_status()
            self.view.updateFileStatus(i, s)

    def generateTreeModel(self):
        self.model.roots.clear()
        for n in self.view.gView.group_list:
            tag = n.labelWidget.currentText()
            data = n.getSelectedLabels()
            currentRoot = self.model.addRoot(tag, data=data)
            self.generateTreeModelRec(n, currentRoot)

    def generateTreeModelRec(self, viewNode, modeNode):
        for c in viewNode.children:
            childLabel = c[1].labelWidget.currentText()
            childData = c[1].getSelectedLabels()
            modelChild = modeNode.addChild(childLabel, data=childData)
            self.generateTreeModelRec(c[1], modelChild)


    def loadTagList(self):
        for t in self.model.ntList:
            self.view.addToTagList(t)

    def addTagAction(self):
        added = self.view.addTag()
        self.updateFileStatus(added, mode=1)

    def deleteTagAction(self):
        deletedNT = self.view.deleteTag()
        self.updateFileStatus(deletedNT)

    def updateFileStatus(self, nt, mode=0):
        for fIndex in range(len(self.model.fileList)):
            if mode == 0 and nt in self.model.fileList[fIndex][2]:
                self.model.fileList[fIndex][1] = "3"
                print(self.model.fileList[fIndex])
                self.view.updateFileStatus(fIndex, "3")
            elif mode == 1 and nt in self.model.fileList[fIndex][2]:
                self.model.fileList[fIndex][1] = "1"
                print(self.model.fileList[fIndex])
                self.view.updateFileStatus(fIndex, "1")

    def loadFileList(self):
        for i in self.model.fileList:
            self.view.addToFileList(i)

    @QtCore.pyqtSlot("QModelIndex")
    def loadFile(self, selectedIndex):
        selectedItem = self.view.fileList_ListModel.item(selectedIndex.row())
        self.save()
        self.view.gView.clearScene()
        self.model.clearModel()
        self.model.loadFile(self.model.folderPath + "/" + selectedItem.text())
        self.loadContent()
        for t_index in range(len(self.model.tokens)):
            self.view.gView.groupIndex_list[t_index] = self.model.tokens[t_index].groupIndex
        for t in self.model.tokens:
            start = 0
            for end in t.groupIndex:
                self.view.gView.createGroupByIndex(self.model.tokens.index(t), start, end, anim=False)
                start = end + 1
        if len(self.model.roots) > 0:
            for r in self.model.roots:
                self.model2view_tree(r)

    def openFile(self):
        filePath = self.view.showFileDialog()
        self.model.loadModel(filePath)
        self.loadTagList()
        self.loadFileList()
        self.loadContent()
        for t_index in range(len(self.model.tokens)):
            self.view.gView.groupIndex_list[t_index] = self.model.tokens[t_index].groupIndex
        for t in self.model.tokens:
            start = 0
            for end in t.groupIndex:
                self.view.gView.createGroupByIndex(self.model.tokens.index(t), start, end, anim=False)
                start = end + 1
        if len(self.model.roots) > 0:
            for r in self.model.roots:
                self.model2view_tree(r)


    def model2view_tree(self, node):
        childView_list = list()
        for c in node.children:
            if len(c.children) == 0:
                leafView = self.view.gView.findLeaf(c)
                if leafView is None:
                    print("Not Found")
                    break
                childView_list.append(leafView)
            else:
                childView = self.model2view_tree(c)
                childView_list.append(childView)
        nodeView = self.view.gView.createParentFromModel(childView_list, node.label)
        return nodeView


    def loadContent(self):
        tokenMenu_list = self.view.gView.initializeTokens(self.model.getTokenStrings())
        for token_index in range(0,len(tokenMenu_list)):
            menu = tokenMenu_list[token_index]
            token = self.model.tokens[token_index]
            anl_index = 0
            for anl in token.allAlayses:
                act = menu.addAction(anl[0].replace("-",""), self.selectAnalysis)
                act.setProperty(*("token_id", token_index))
                act.setProperty(*("analysis_id", anl_index))
                anl_index += 1

    def selectAnalysis(self):
        self.view.gView.tokenAnimations.clear()
        action = self.view.sender()
        token_id = action.property("token_id")
        anlysis_id = action.property("analysis_id")
        surface, abstract = self.model.selectAnalysis(token_id, anlysis_id)

        self.view.gView.updateTokens(token_id, surface, abstract)
        self.view.gView.tokenAnimations.start()
        #self.view.moveElement(self.view.tokenLabel_list[token_id],300,100)

Controller().run()