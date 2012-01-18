#!/usr/bin/python
# coding=utf-8
from __future__ import division, print_function, unicode_literals

from copy import copy

from PyQt4 import QtCore
from bunch import Bunch

class GenericTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data, headers, attributes, userAttributes = (), defaultNode = None, parent=None):
        QtCore.QAbstractItemModel.__init__(self, parent)
        self.rows = list(data)
        assert len(headers) <= len(attributes)
        assert len(headers) > 0
        self.columnHeaders = headers
        self.columnAttributes = attributes
        self.userAttributes = userAttributes
        if defaultNode is not None:
            self.defaultNode = defaultNode
        else :
            obj = Bunch()
            for att in self.columnAttributes:
                obj[att] = ""
            self.defaultNode = obj

    def rowCount(self, parent = None):
        return len(self.rows)

    def columnCount(self, parent = None):
        return len(self.columnHeaders)

    def data(self, index, role):
        if not index.isValid():
            return None
        row, col = index.row(), index.column()
        if role == QtCore.Qt.EditRole or role == QtCore.Qt.DisplayRole:
            if len(self.columnAttributes) > col:
                return  self.rows[row].__getattribute__(self.columnAttributes[col])
        elif role == QtCore.Qt.UserRole:
            if len(self.userAttributes) > col:
                return self.rows[row].__getattribute__(self.userAttributes[col])


    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if index.isValid():
            if role == QtCore.Qt.EditRole:
                row = index.row()
                self.rows[row].__setattr__(self.columnAttributes[index.column()], value.toPyObject())
                indexLeft = self.index(row, 0)
                indexRight = self.index(row, len(self.columnAttributes) - 1)
                self.dataChanged.emit(indexLeft, indexRight)
                return True
        return False

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole :
            if orientation == QtCore.Qt.Horizontal:
                return self.columnHeaders[section]
            else :
                return str(section + 1)

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable


    def index(self, row, column, parent = None):
        return self.createIndex(row, column, self.rows[row].__getattribute__(self.columnAttributes[column]))


#    def parent(self, index=None):
#        node = self.getNode(index)
#        parentNode = node.parent()
#
#        if parentNode == self._rootNode:
#            return QtCore.QModelIndex()
#
#        return self.createIndex(parentNode.row(), 0, parentNode)

    def insertRows(self, position, rows, parent=QtCore.QModelIndex()):
        self.beginInsertRows(parent, position, position + rows - 1)
        success = True
        for row in range(rows):
            newRow = copy(self.defaultNode)
            success &= self.rows.insert(position, newRow)
        self.endInsertRows()
        return success

    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        self.beginRemoveRows(parent, position, position + rows - 1)
        for row in range(rows):
            del self.rows[position]
        self.endRemoveRows()
        return True