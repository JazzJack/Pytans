#!/usr/bin/python
# coding=utf-8
from __future__ import division, print_function, unicode_literals

from copy import copy

from PyQt4 import QtCore
from PyQt4.QtGui import QBrush, QColor
from bunch import Bunch


def convert2PyObject(obj):
    if isinstance(obj, QtCore.QVariant):
        return obj.toPyObject()
    else:
        return obj

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

    def rowCount(self, parent = None, *args, **kwargs):
        return len(self.rows)

    def columnCount(self, parent = None, *args, **kwargs):
        return len(self.columnHeaders)

    def data(self, index, role):
#        if not index.isValid():
#            return None
        row, col = index.row(), index.column()
        r = self.rows[row]
        if role == QtCore.Qt.EditRole or role == QtCore.Qt.DisplayRole:
            if len(self.columnAttributes) > col:
                return  r.__getattribute__(self.columnAttributes[col])
        elif role == QtCore.Qt.UserRole:
            if len(self.userAttributes) > col:
                return r.__getattribute__(self.userAttributes[col])
        elif role == QtCore.Qt.BackgroundRole:
            if hasattr(r, "background"):
                return QBrush(QColor(*self.rows[row].background))
        elif role == QtCore.Qt.TextAlignmentRole:
            return QtCore.Qt.AlignCenter


    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if index.isValid():
            row, col = index.row(), index.column()
            if role == QtCore.Qt.EditRole:
                self.rows[row].__setattr__(self.columnAttributes[col], convert2PyObject(value))
                indexLeft = self.index(row, 0)
                indexRight = self.index(row, len(self.columnAttributes) - 1)
                self.dataChanged.emit(indexLeft, indexRight)
                return True
            if role == QtCore.Qt.UserRole:
                self.rows[row].__setattr__(self.userAttributes[col], convert2PyObject(value))
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


    def index(self, row, column, parent = None, *args, **kwargs):
        return self.createIndex(row, column, self.rows[row].__getattribute__(self.columnAttributes[column]))


    def insertRows(self, position, rows, parent=QtCore.QModelIndex(), *args, **kwargs):
        self.beginInsertRows(parent, position, position + rows - 1)
        for row in range(rows):
            newRow = copy(self.defaultNode)
            self.rows.insert(position, newRow)
        self.endInsertRows()
        return True

    def removeRows(self, position, rows, parent=QtCore.QModelIndex(), *args, **kwargs):
        self.beginRemoveRows(parent, position, position + rows - 1)
        for row in range(rows):
            del self.rows[position]
        self.endRemoveRows()
        return True