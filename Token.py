from Node import Node


class Token(Node):

    def __init__(self,word):
        self.word = word
        self.abs = ""
        self.allAlayses = list()
        self.surface = list()
        self.abstract = list()
        self.groupIndex = list()

    def addAnalysis(self, anl):
        self.allAlayses.append(anl)