#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
from PyQt4 import QtCore, QtGui
from rules import defaultSkillTree

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s



def createRowFromSkill(skill):
    nameItem = QtGui.QStandardItem(skill.name)
    valueItem = QtGui.QStandardItem("%d"%skill.value)
    sumItem = QtGui.QStandardItem("%d"%skill.summed())
    return [nameItem, valueItem, sumItem]


def createSkillTreeModel():
    model = QtGui.QStandardItemModel()
    model.setHorizontalHeaderLabels(["Name", "Value", "Sum"])
    parent = model.invisibleRootItem()
    handwerkRow = createRowFromSkill(defaultSkillTree["Handwerk"])
    parent.appendRow(handwerkRow)
    parentItem = handwerkRow[0]
    for s in defaultSkillTree["Handwerk"].values():
        parentItem.appendRow(createRowFromSkill(s))
    return handwerkRow[0], model

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(692, 583)
        self.widget = QtGui.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(10, 10, 671, 561))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.treeView = QtGui.QTreeView(self.widget)
        self.treeView.setObjectName(_fromUtf8("treeView"))
        self.verticalLayout.addWidget(self.treeView)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Talentbaum", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    handwerk, model = createSkillTreeModel()
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    ui.treeView.setModel(model)
    Form.show()
    app.exec_()
    print(handwerk)
    sys.exit()
