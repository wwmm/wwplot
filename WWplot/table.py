# -*- coding: utf-8 -*-
"""
Table view and model classes
"""

import os

import numpy as np
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import (QFileDialog, QHeaderView, QPushButton,
                               QTableView, QToolButton)

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
        button_export = self.main_widget.findChild(QPushButton, "button_export")

        button_add_row.clicked.connect(self.add_row)
        button_remove_row.clicked.connect(self.remove_row)
        button_import.clicked.connect(self.import_data)
        button_export.clicked.connect(self.export_data)

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
        home = os.path.expanduser("~")

        path = QFileDialog.getOpenFileName(self.main_widget, "Open Table", home, "Tables (*.tsv)")[0]

        if path != "":
            table = np.genfromtxt(path, delimiter='\t')

            self.model.beginResetModel()

            self.model.data_x = table[:, 0]
            self.model.data_xerr = table[:, 1]
            self.model.data_y = table[:, 2]
            self.model.data_yerr = table[:, 3]

            self.model.endResetModel()

    def export_data(self):
        home = os.path.expanduser("~")

        path = QFileDialog.getSaveFileName(self.main_widget, "Save Table",  home, "Tables (*.tsv)")[0]

        if path != "":
            if not path.endswith('.tsv'):
                path += '.tsv'

            np.savetxt(path,
                       np.transpose([self.model.data_x, self.model.data_xerr, self.model.data_y, self.model.data_yerr]),
                       delimiter="\t", fmt='%1.6e')
