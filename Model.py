import os
import subprocess
import json
import requests
import re
from Token import Token


class Model:

    def __init__(self):
        self.folderPath = ""    #cwd
        self.currentFile = ""   #path + name


        self.fileList = list()  #file names with NTs and states
        self.ntList = list()   #list of NTs
        self.defaultNTList = [["NS","DESC"],["VS","DESC"],["TPMG","DESC"],["CMG","DESC"],["ACCM","DESC"],["VMG","DESC"],["DNG","DESC"],["DVG","DESC"],["NPS","DESC"],["NP","DESC"],["VPS","DESC"],["VP","DESC"],["NPC","DESC"],["NPACC","DESC"],["ADV","DESC"],["S","DESC"]]

        self.sentence = list()
        self.tokens = list()
        self.roots = list()

        self.ruleCounts = {}

    def generateRuleStats(self):
        for fc in self.fileList:
            if fc[1] == "1":
                f = open(self.folderPath + "/" + fc[0], "r", encoding="utf-8")
                f_lines = f.readlines()
                treeLines = list()
                for l in f_lines:
                    if l == "\n":
                        break
                    treeLines.append(l)

                nt = re.findall(r"\((\w+)[\s]", treeLines[0])[0]
                root = self.addRoot(nt)
                self.text2Tree(treeLines, root, 1)

                self.getRuleCounts(root)

                self.roots.clear()

        self.calculateProbs()


    def getRuleCounts(self, node):
        rule = node.label + " -> "
        if len(node.children) == 0:
            return
        else:
            for c in node.children:
                rule += c.label + " "
                self.getRuleCounts(c)
            if self.ruleCounts.get(rule) is None:
                self.ruleCounts[rule] = 1
            else:
                self.ruleCounts[rule] += 1

    def get_current_file_status(self):
        p = self.currentFile.split("/")
        fname = p[len(p)-1]
        for i in range(len(self.fileList)):
            if fname == self.fileList[i][0]:
                return i, self.fileList[i][1]


    def calculateProbs(self):
        f = open(self.folderPath + "/rule_statixtics.txt", "w", encoding="utf-8")
        for selected_rule in self.ruleCounts:
            left_hand, right_hand = selected_rule.split(" -> ")
            l_count = 0
            lr_count = 0

            for r in self.ruleCounts:
                l2, r2 = r.split(" -> ")
                if left_hand == l2:
                    l_count += self.ruleCounts[r]
                if left_hand == l2 and len(set(r2.split(" ")).intersection(set(right_hand.split(" ")))) > 0:
                    lr_count += self.ruleCounts[r]

            prob = lr_count / lr_count
            f.write(selected_rule + "\t" + str(prob) + "\n")
        f.close()


    def loadModel(self, filePath):
        self.folderPath = filePath
        #self.detectFolderPath(filePath)
        fileList = os.listdir(self.folderPath)
        if "files.conf" in fileList and "nt.conf" in fileList:
            self.load()
        else:
            self.create()
        self.currentFile = self.folderPath + "/" + self.fileList[0][0]
        self.loadFile(self.currentFile)

    def clearModel(self):
        self.sentence.clear()
        self.tokens.clear()
        self.roots.clear()

    def load(self): #read conf files and load project
        filesconf_file = open(self.folderPath +  "/files.conf", "r", encoding="utf-8")
        ntconf_file = open(self.folderPath + "/nt.conf", "r", encoding="utf-8")

        filesconf_lines = filesconf_file.readlines()
        for line in filesconf_lines:
            fileName, state, NTs = line.split("\t")

            fileConfig = list()
            fileConfig.append(fileName)
            fileConfig.append(state)
            if NTs == "\n":
                fileConfig.append(list())
            else:
                fileConfig.append(NTs.split(","))
            self.fileList.append(fileConfig)

        ntconf_lines = ntconf_file.readlines()
        for l in ntconf_lines:
            nt, tt = l.replace("\n","").split("\t")
            self.ntList.append([nt, tt])
        filesconf_file.close()
        ntconf_file.close()

    def updateIndexes(self, indexList):
        for t_index in range(len(self.tokens)):
            self.tokens[t_index].groupIndex = indexList[t_index]

    def create(self): #create conf files and project
        self.ntList = self.defaultNTList

        fileList = os.listdir(self.folderPath)
        for fileName in fileList:
            file = open(self.folderPath + "/" + fileName, "r", encoding="utf-8")
            fileLines = file.readlines()
            fileConfig = list()
            if "(" in fileLines[0]: #file has a tree
                fileNTs = self.getFileNTs(fileLines)
                state = self.checkFileState(fileLines, fileNTs)

                fileConfig.append(fileName)
                fileConfig.append(state)
                fileConfig.append(fileNTs)

            else:
                fileConfig.append(fileName)
                fileConfig.append("2")
                fileConfig.append(list())

            self.fileList.append(fileConfig)

    def getFileNTs(self, fileLines):
        NTs = list()
        for line in fileLines:
            x = re.findall(r"\((\w+)", line)
            if len(x) > 0:
                print(x)
                NTs.append(x[0])
        return NTs

    def checkFileState(self, fileLines, fileNTs):
        ntList = list()
        for n in self.ntList:
            ntList.append(n[0])
        if [value for value in fileNTs  if value in set(ntList)] != fileNTs:
            return "3" #Unkown NT in file
        else:
            if fileLines[0] == "(S\n":
                return "1"
            return "2"

    def loadFile(self, filePath):
        #self.detectFolderPath(filePath[0])
        self.currentFile = filePath
        file = open(self.currentFile, "r", encoding="utf-8")
        file_lines = file.readlines()
        if "(" in file_lines[0]:#tree in file
            isTree = True
            treeLines = list()
            for l in file_lines:
                if l == "\n":
                    isTree = False
                    continue
                if isTree:
                    treeLines.append(l)
                else:
                    word, anl, indexStr = l.split("\t")
                    t = Token(word)
                    t.abs = anl.replace("\n","")
                    indexList = indexStr.replace("\n","").split(",")
                    for idx in indexList:
                        t.groupIndex.append(int(idx))
                    self.sentence.append(word)
                    self.tokens.append(t)
            nt = re.findall(r"\((\w+)[\s]", treeLines[0])[0] #birden fazla root varsa ?
            root = self.addRoot(nt)
            self.text2Tree(treeLines, root, 1)
        #print(filePath)
        else:
            for l in file_lines:
                l = l.replace("\n","")
                self.sentence.append(l)
                self.tokens.append(Token(l))
        self.analyseTokens()

    def detectFolderPath(self, filePath):
        p = filePath.split("/")
        folderPath = ""
        for i in range(len(p)-1):
            folderPath += p[i] + "/"
        self.folderPath = folderPath

    def analyseTokens(self):
        '''
        for s in range(len(self.sentence)):
            t = self.tokens[s]
            if self.sentence[s] == "ben":
                t.surace = ["ben","-","-","-"]
                t.abstract = ["ben<NOM>","-<Num:Sg>","-<Poss:No>","-<Case:Nom>"]
            if self.sentence[s] == "çabucak":
                t.surace = ["çabucak"]
                t.abstract = ["çabucak<ADV>"]
            if self.sentence[s] == "geleceğim":
                t.surface = ["gel", "-", "-eceğ", "-im"]
                t.abstract = ["gel<VS><Actv>","-<Pol:Pos>","-<Tns:Fut>","-<Prsn:1s>"]
        '''
        input = {}
        input["wordList"] = self.sentence
        json_data = json.dumps(input, ensure_ascii=False)
        r = requests.post("http://ddil.isikun.edu.tr/syneditws/", json_data.encode('utf-8'))
        response = r.json()
        for r in range(len(response['analyses'])):
            t = self.tokens[r] #Token(self.sentence[r])
            #self.tokens.append(t)
            for a in response['analyses'][r]:
                t.addAnalysis(a)
            if len(t.abs) > 0:
                for d in t.allAlayses:
                    if d[0] == t.abs:
                        t.surface = d[1].split("-")
                        t.abstract = d[0].split("-")
            #print(r)

    def getTokenStrings(self):
        tokenStrings = list()
        for t in self.tokens:
            tokenStrings.append((t.word, t.abstract, t.surface))
        return tokenStrings

    def selectAnalysis(self, token_id, analysis_id):
        token = self.tokens[token_id]
        analysis, surface = token.allAlayses[analysis_id]
        token.surface = surface.split("-")
        token.abstract = analysis.split("-")
        return token.surface, token.abstract

    def addRoot(self, label, data=None):
        r = NodeModel(label, data=data)
        self.roots.append(r)
        return r

    def saveConfig(self):
        filesconf_file = open(self.folderPath + "/files.conf", "w", encoding="utf-8")
        ntconf_file = open(self.folderPath + "/nt.conf", "w", encoding="utf-8")

        for fConfig in self.fileList:
            fname = fConfig[0]
            state = fConfig[1]
            ntlist = fConfig[2]

            filesconf_file.write(fname + "\t" + state + "\t")
            if len(ntlist) > 0:
                i=0
                for i in range(len(ntlist)-1):
                    filesconf_file.write(ntlist[i]+",")
                filesconf_file.write(ntlist[i])
            filesconf_file.write("\n")

        ntDuo_i = 0
        for ntDuo_i in range(len(self.ntList)-1):
            ntconf_file.write(self.ntList[ntDuo_i][0] + "\t" + self.ntList[ntDuo_i][1] + "\n")
        ntconf_file.write(self.ntList[ntDuo_i][0] + "\t" + self.ntList[ntDuo_i][1])

        filesconf_file.close()
        ntconf_file.close()

    def updateFileConf(self, fileLines):
        cf = self.currentFile.split("/")
        fileName = cf[len(cf)-1]

        for fConf in self.fileList:
            if fConf[0] == fileName:
                fConf[2] = self.getFileNTs(fileLines)
                break

    def saveToFile(self):
        file = open(self.currentFile, "w", encoding="utf-8")

        treeString = ""
        for r in self.roots:
            treeString = self.tree2Text(treeString, r, 0)
        file.write(treeString + "\n")

        self.updateFileConf(treeString.split("\n"))

        for t in self.tokens:
            file.write(t.word+"\t")
            file.write(t.abstract[0])
            for i in range(1, len(t.abstract)):
                file.write("-" + t.abstract[i])
            file.write("\t")
            j = 0
            while j < len(t.groupIndex)-1:
                file.write(str(t.groupIndex[j]) + ",")
                j += 1
            file.write(str(t.groupIndex[j]))
            file.write("\n")

        file.close()

    def tree2Text(self, str, node, depth):
        for i in range(depth):
            str +="\t"
        str += "(" + node.label
        if len(node.children) > 0:
            str += "\n"
            for c in node.children:
                str = self.tree2Text(str, c, depth+1)

            for i in range(depth):
                str += "\t"
            str += ")\n"
        else:
            for d in node.data:
                str += " " + d[0] + "{" + d[1] + "}"
            str += ")\n"
        return str

    def text2Tree(self, lines, node, lineIndex):
        while lineIndex < len(lines):
            if "(" in lines[lineIndex] and ")" in lines[lineIndex]:  # leaf
                elements = re.findall(r"\((.+)\)", lines[lineIndex])[0].split(" ")
                nt = elements[0]
                data = list()
                for i in range(1, len(elements)):
                    surf = elements[i].split("{")[0]
                    abs = re.findall(r"{(.+)}", elements[i])[0]
                    data.append([surf, abs])
                node.addChild(nt, data=data)
            elif "(" in lines[lineIndex] and ")" not in lines[lineIndex]:
                nt = re.findall(r"\((.+)\n", lines[lineIndex])[0]
                child = node.addChild(nt)
                lineIndex = self.text2Tree(lines, child, lineIndex + 1)
            elif "(" not in lines[lineIndex] and ")" in lines[lineIndex]:
                return lineIndex
            lineIndex += 1

class NodeModel:

    def __init__(self, label, data=None):
        self.label = label
        self.data = data
        self.children = list()

    def addChild(self, label, data=None):
        c = NodeModel(label, data)
        self.children.append(c)
        return c

