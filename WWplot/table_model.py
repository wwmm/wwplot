# -*- coding: utf-8 -*-
"""
Table model class that will be exposed to QML
"""

from PySide2.QtCore import QAbstractTableModel, Qt


class TableModel(QAbstractTableModel):
    """
        Table Model used by the data table
    """

    def __init__(self):
        QAbstractTableModel.__init__(self)

        self.dados = [1, 2, 3, 4, 5]
        self.nrows = len(self.dados)
        self.ncols = 4

    def rowCount(self, parent):
        return self.nrows

    def columnCount(self, parent):
        return self.ncols

    def data(self, index, role):
        # if role == Qt.HeadingRole:
        #     print("oi")
        print(Qt.HeadingRole)

        if role == Qt.DisplayRole and index.row() >= 0 and index.row() < len(self.dados) and index.column() == 0:
            return 10

        return -1
