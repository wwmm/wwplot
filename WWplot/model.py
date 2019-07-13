# -*- coding: utf-8 -*-

import numpy as np
from PySide2.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide2.QtGui import QColor


class Model(QAbstractTableModel):
    def __init__(self):
        QAbstractTableModel.__init__(self)

        self.ncols = 4
        nrows = 5  # initial number of rows

        self.data_x = np.zeros(nrows)
        self.data_xerr = np.zeros(nrows)
        self.data_y = np.zeros(nrows)
        self.data_yerr = np.zeros(nrows)

    def rowCount(self, parent=QModelIndex()):
        return self.data_x.size

    def columnCount(self, parent=QModelIndex()):
        return self.ncols

    def flags(self, index):
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
                return "{0:.6e}".format(self.data_x[row])

            if column == 1:
                return "{0:.6e}".format(self.data_xerr[row])

            if column == 2:
                return "{0:.6e}".format(self.data_y[row])

            if column == 3:
                return "{0:.6e}".format(self.data_yerr[row])

    def sort(self, column, order):
        if column == 0:
            sorted_idx = self.data_x.argsort()

            if order == Qt.SortOrder.DescendingOrder:
                sorted_idx = sorted_idx[::-1]

            self.beginResetModel()

            self.data_x = self.data_x[sorted_idx]
            self.data_xerr = self.data_xerr[sorted_idx]
            self.data_y = self.data_y[sorted_idx]
            self.data_yerr = self.data_yerr[sorted_idx]

            self.endResetModel()

    def append_row(self):
        self.beginInsertRows(QModelIndex(), self.data_x.size, self.data_x.size)

        self.data_x = np.append(self.data_x, 0)
        self.data_xerr = np.append(self.data_xerr, 0)
        self.data_y = np.append(self.data_y, 0)
        self.data_yerr = np.append(self.data_yerr, 0)

        self.endInsertRows()

    def remove_rows(self, index_list):
        index_list.sort(reverse=True)

        for index in index_list:
            self.beginRemoveRows(QModelIndex(), index, index)
            self.endRemoveRows()

        self.data_x = np.delete(self.data_x, index_list)
        self.data_xerr = np.delete(self.data_xerr, index_list)
        self.data_y = np.delete(self.data_y, index_list)
        self.data_yerr = np.delete(self.data_yerr, index_list)
