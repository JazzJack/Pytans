#!/usr/bin/python
# coding=utf-8
from __future__ import division, print_function, unicode_literals

import sys
from PyQt4 import QtGui, QtCore, uic
from fighter import Fighter
from TableModel import GenericTableModel


base, form = uic.loadUiType("CombatManager.ui")

def writeModelToFile(model, filename):
    with open(filename, "w") as f:
        for row in range(model.rowCount()):
            line = []
            for col in range(model.columnCount()):
                line.append(str(model.index( row, col, QtCore.QModelIndex() ).data( QtCore.Qt.DisplayRole ).toString()))
            f.write(", ".join(line) + "\n")

def loadCSVAndAppendToModel(filename, model, convert = ()):
    with open(filename, "r") as f:
        lines = f.readlines()
        for l in lines:
            i = model.rowCount()
            model.insertRows(i, 1)
            for col, val in enumerate(l.split(", ")):
                if col in convert:
                    val = convert[col](val)
                index = model.index(i, col)
                model.setData(index, val, role=QtCore.Qt.EditRole)


class CombatManagerMain(base, form):
    def __init__(self, model, parent=None, sortCol = 0):
        super(base, self).__init__(parent)
        self.setupUi(self)

        self.model = model
        self.proxyModel = QtGui.QSortFilterProxyModel()
        self.proxyModel.setSourceModel(model)
        self.proxyModel.setDynamicSortFilter(True)
        self.proxyModel.setSortRole(QtCore.Qt.UserRole)
        self.proxyModel.sort(sortCol)
        self.combatTable.setModel(self.proxyModel)
        self.combatTable.resizeColumnsToContents()
        #self.combatTable.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.selectionModel = self.combatTable.selectionModel()
        self.round = 1
        self.statusbar.showMessage('Runde: %d'%self.round)

        self.actionAdd.triggered.connect(self.on_add_action)
        self.actionRemove.triggered.connect(self.on_remove_action)
        self.actionNext.triggered.connect(self.on_next_action)
        self.actionNew.triggered.connect(self.on_new_action)
        self.actionOpen.triggered.connect(self.on_open_action)
        self.actionSave.triggered.connect(self.on_save_action)
        self.actionReset.triggered.connect(self.on_reset_action)


    def setData(self, row, attr, value):
        if attr in self.model.userAttributes:
            col = self.model.userAttributes.index(attr)
            role = QtCore.Qt.UserRole
        elif attr in self.model.columnAttributes:
            col = self.model.columnAttributes.index(attr)
            role = QtCore.Qt.DisplayRole
        else :
            return
        model_index = self.model.index(row, col)
        self.model.setData(model_index, value, role)

    def getData(self, row, attr):
        if attr in self.model.userAttributes:
            col = self.model.userAttributes.index(attr)
            role = QtCore.Qt.UserRole
        elif attr in self.model.columnAttributes:
            col = self.model.columnAttributes.index(attr)
            role = QtCore.Qt.DisplayRole
        else :
            return
        model_index = self.model.index(row, col)
        return self.model.data(model_index, role)


    def on_add_action(self):
        rowCnt = self.model.rowCount()
        self.model.insertRows(rowCnt, 1)

    def on_remove_action(self):
        selectedRows = [self.proxyModel.mapToSource(index).row() for index in self.selectionModel.selectedRows()]
        for s in selectedRows:
            self.model.removeRows(s, 1)

    def on_next_action(self):
        row_of_first = self.proxyModel.mapToSource(self.proxyModel.index(0, 0)).row()
        # if first one is active : end his turn!
        if self.getData(row_of_first, "active"):
            self.setData(row_of_first, "active", False)
            self.setData(row_of_first, "acted", True)

        # if new first one hasn't acted yet : start his turn
        row_of_first = self.proxyModel.mapToSource(self.proxyModel.index(0, 0)).row()
        if not self.getData(row_of_first, "acted"):
            ap = self.getData(row_of_first, "AP")
            apGain = self.getData(row_of_first, "APGain")
            apMax = self.getData(row_of_first, "GE")
            self.setData(row_of_first, "active", True)
            self.setData(row_of_first, "AP", min(apMax, ap + apGain))
        else :
            # start new round
            for i in range(self.model.rowCount()):
                self.setData(i, "acted", False)
            self.round += 1
            self.statusbar.showMessage('Runde: %d'%self.round)
        self.selectionModel.clearSelection()

    def on_new_action(self):
        self.model.removeRows(0, self.model.rowCount())
        self.round = 1
        self.statusbar.showMessage('Runde: %d'%self.round)

    def on_open_action(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File', '.')
        loadCSVAndAppendToModel(filename, self.model, {1: int, 2: int, 3: int, 4: int, 5: str2bool, 6:str2bool})

    def on_save_action(self):
        filename = QtGui.QFileDialog.getSaveFileName(self, "Save File", ".")
        writeModelToFile(self.model, filename)

    def on_reset_action(self):
        # start new round
        self.round = 1
        self.statusbar.showMessage('Runde: %d'%self.round)
        for i in range(self.model.rowCount()):
            self.setData(i, "acted", False)
            self.setData(i, "active", False)



def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    model = GenericTableModel(
        data= [],
        headers= ["               Name               ", "SN", "GE", "IN", "Aktionspunkte", "Acted", "Active"],
        attributes= ["name", "SN", "GE", "IN", "AP", "acted", "active"],
        userAttributes= ["priority", "active", "acted", "AP", "APGain"],
        defaultNode= Fighter(""))
    w = CombatManagerMain(model)
    w.show()
    sys.exit(app.exec_())

