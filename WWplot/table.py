# -*- coding: utf-8 -*-
"""
Table view and model classes
"""

import numpy as np
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QFileDialog, QPushButton, QTableView, QToolButton, QHeaderView

from model import Model


class Table():
    """
        Class that creates each data table
    """

    def __init__(self):
        loader = QUiLoader()

        self.main_widget = loader.load("ui/table.ui")

        self.table_view = self.main_widget.findChild(QTableView, "table_view")
        button_add_row = self.main_widget.findChild(QToolButton, "button_add_row")
        button_remove_row = self.main_widget.findChild(QToolButton, "button_remove_row")
        button_import = self.main_widget.findChild(QPushButton, "button_import")

        button_add_row.clicked.connect(self.add_row)
        button_remove_row.clicked.connect(self.remove_row)
        button_import.clicked.connect(self.import_data)

        self.model = Model()

        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table_view.setModel(self.model)

    def add_row(self):
        self.model.append_row()

    def remove_row(self):
        index_list = self.table_view.selectedIndexes()

        if len(index_list) >= 4:
            int_index_list = set()
            columns = set()

            for index in index_list:
                int_index_list.add(index.row())
                columns.add(index.column())

            if 0 in columns and 1 in columns and 2 in columns and 3 in columns:
                self.model.remove_rows(list(int_index_list))

    def import_data(self):
        path = QFileDialog.getOpenFileName(None, "Open File", "/home", "Tables (*.tsv)")

        if path[0] != "":
            table = np.genfromtxt(path[0], delimiter='\t')

            self.model.beginResetModel()

            self.model.data_x = table[:, 0]
            self.model.data_xerr = table[:, 1]
            self.model.data_y = table[:, 2]
            self.model.data_yerr = table[:, 3]

            self.model.endResetModel()
