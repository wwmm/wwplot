# -*- coding: utf-8 -*-
"""
Table view and model classes
"""

import numpy as np
from PySide2.QtCore import QAbstractTableModel, Qt
from PySide2.QtGui import QColor
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QTableView


class Model(QAbstractTableModel):
    """
        Table Model used by the data table
    """

    def __init__(self):
        QAbstractTableModel.__init__(self)

        self.ncols = 4
        nrows = 5  # initial number of rows

        self.data_x = np.zeros(nrows)
        self.data_xerr = np.zeros(nrows)
        self.data_y = np.zeros(nrows)
        self.data_yerr = np.zeros(nrows)

    def rowCount(self, _):
        return self.data_x.size

    def columnCount(self, _):
        return self.ncols

    def flags(self, _):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def setData(self, index, value, role):
        if index.isValid() and role == Qt.EditRole:
            column = index.column()
            row = index.row()

            try:
                float_value = float(value)

                if column == 0:
                    self.data_x[row] = float_value

                if column == 1:
                    self.data_xerr[row] = float_value

                if column == 2:
                    self.data_y[row] = float_value

                if column == 3:
                    self.data_yerr[row] = float_value

                # sorting

                sorted_idx = self.data_x.argsort()

                self.data_x = self.data_x[sorted_idx]
                self.data_xerr = self.data_xerr[sorted_idx]
                self.data_y = self.data_y[sorted_idx]
                self.data_yerr = self.data_yerr[sorted_idx]

                return True
            except ValueError:
                return False

        return False

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            return ("x", "xerr", "y", "yerr")[section]

        return "{}".format(section)

    def data(self, index, role):
        if role == Qt.BackgroundRole:
            return QColor(Qt.white)

        elif role == Qt.TextAlignmentRole:
            return Qt.AlignRight

        elif role == Qt.DisplayRole:
            column = index.column()
            row = index.row()

            if column == 0:
                return "{}".format(self.data_x[row])

            if column == 1:
                return "{}".format(self.data_xerr[row])

            if column == 2:
                return "{}".format(self.data_y[row])

            if column == 3:
                return "{}".format(self.data_yerr[row])


class Table():
    """
        Class that creates each data table
    """

    def __init__(self):
        loader = QUiLoader()

        self.main_widget = loader.load("ui/table.ui")

        self.table_view = self.main_widget.findChild(QTableView, "table_view")

        self.table_view.setModel(Model())
