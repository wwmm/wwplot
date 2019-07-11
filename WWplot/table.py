# -*- coding: utf-8 -*-
"""
Table model class that will be exposed to QML
"""

from PySide2.QtCore import QAbstractTableModel, Qt
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QTableView


class Model(QAbstractTableModel):
    """
        Table Model used by the data table
    """

    def __init__(self):
        QAbstractTableModel.__init__(self)

        self.dados = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.nrows = len(self.dados)
        self.ncols = 4

    def rowCount(self, _):
        return self.nrows

    def columnCount(self, _):
        return self.ncols

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            return ("x", "xerr", "y", "yerr")[section]

        return "{}".format(section)

    def data(self, index, role):
        column = index.column()
        row = index.row()

        if role == Qt.DisplayRole:
            return index.column() + index.row()

        if role == Qt.BackgroundRole:
            return QColor(Qt.white)

        if role == Qt.TextAlignmentRole:
            return Qt.AlignRight


class Table(QTableView):
    """
        Class that creates each data table
    """

    def __init__(self):
        QTableView.__init__(self)

        self.setModel(Model())
