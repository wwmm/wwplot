# -*- coding: utf-8 -*-

import os

import numpy as np
from PySide2.QtCore import QEvent, QObject, Qt
from PySide2.QtGui import QColor, QGuiApplication, QKeySequence
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import (QFileDialog, QFrame, QGraphicsDropShadowEffect,
                               QHeaderView, QPushButton, QTableView)

from model import Model


class Table(QObject):
    def __init__(self):
        QObject.__init__(self)

        loader = QUiLoader()

        self.main_widget = loader.load("ui/table.ui")

        self.table_view = self.main_widget.findChild(QTableView, "table_view")
        button_add_row = self.main_widget.findChild(QPushButton, "button_add_row")
        button_remove_row = self.main_widget.findChild(QPushButton, "button_remove_row")
        button_import = self.main_widget.findChild(QPushButton, "button_import")
        button_export = self.main_widget.findChild(QPushButton, "button_export")
        fit_frame = self.main_widget.findChild(QFrame, "fit_frame")

        button_add_row.clicked.connect(self.add_row)
        button_remove_row.clicked.connect(self.remove_selected_rows)
        button_import.clicked.connect(self.import_data)
        button_export.clicked.connect(self.export_data)

        self.table_view.installEventFilter(self)

        self.model = Model()

        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table_view.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table_view.setModel(self.model)

        # effects

        button_add_row.setGraphicsEffect(self.button_shadow())
        button_remove_row.setGraphicsEffect(self.button_shadow())
        button_import.setGraphicsEffect(self.button_shadow())
        button_export.setGraphicsEffect(self.button_shadow())
        fit_frame.setGraphicsEffect(self.card_shadow())

    def button_shadow(self):
        effect = QGraphicsDropShadowEffect(self.main_widget)

        effect.setColor(QColor(0, 0, 0, 100))
        effect.setXOffset(1)
        effect.setYOffset(1)
        effect.setBlurRadius(5)

        return effect

    def card_shadow(self):
        effect = QGraphicsDropShadowEffect(self.main_widget)

        effect.setColor(QColor(0, 0, 0, 100))
        effect.setXOffset(2)
        effect.setYOffset(2)
        effect.setBlurRadius(5)

        return effect

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Delete:
                self.remove_selected_rows()

                return True
            elif event.matches(QKeySequence.Copy):
                s_model = self.table_view.selectionModel()

                if s_model.hasSelection():
                    selection_range = s_model.selection().constFirst()

                    table_str = ""
                    clipboard = QGuiApplication.clipboard()

                    for i in range(selection_range.top(), selection_range.bottom() + 1):
                        row_value = []

                        for j in range(selection_range.left(), selection_range.right() + 1):
                            row_value.append(s_model.model().index(i, j).data())

                        table_str += "\t".join(row_value) + "\n"

                    clipboard.setText(table_str)

                return True
            elif event.matches(QKeySequence.Paste):
                s_model = self.table_view.selectionModel()

                if s_model.hasSelection():
                    clipboard = QGuiApplication.clipboard()

                    table_str = clipboard.text()
                    table_rows = table_str.splitlines()  # splitlines avoids an empty line at the end

                    selection_range = s_model.selection().constFirst()

                    first_row = selection_range.top()
                    first_col = selection_range.left()
                    last_col_idx = 0
                    last_row_idx = 0

                    for i in range(len(table_rows)):
                        model_i = first_row + i

                        if model_i < self.model.rowCount():
                            row_cols = table_rows[i].split("\t")

                            for j in range(len(row_cols)):
                                model_j = first_col + j

                                if model_j < self.model.columnCount():
                                    self.model.setData(self.model.index(model_i, model_j), row_cols[j], Qt.EditRole)

                                    if model_j > last_col_idx:
                                        last_col_idx = model_j

                            if model_i > last_row_idx:
                                last_row_idx = model_i

                    first_index = self.model.index(first_row, first_col)
                    last_index = self.model.index(last_row_idx, last_col_idx)

                    self.model.dataChanged.emit(first_index, last_index)

                return True
            else:
                return QObject.eventFilter(self, obj, event)
        else:
            return QObject.eventFilter(self, obj, event)

        return QObject.eventFilter(self, obj, event)

    def add_row(self):
        self.model.append_row()

    def remove_selected_rows(self):
        s_model = self.table_view.selectionModel()

        if s_model.hasSelection():
            index_list = s_model.selectedRows()
            int_index_list = []

            for index in index_list:
                int_index_list.append(index.row())

            self.model.remove_rows(int_index_list)

    def import_data(self):
        home = os.path.expanduser("~")

        path = QFileDialog.getOpenFileName(self.main_widget, "Open Table", home, "Tables (*.tsv)")[0]

        if path != "":
            table = np.genfromtxt(path, delimiter='\t')

            if len(table.shape) == 2:
                nrows, ncols = table.shape

                if ncols == 4 and nrows > 0:
                    self.model.beginResetModel()

                    self.model.data_x = table[:, 0]
                    self.model.data_xerr = table[:, 1]
                    self.model.data_y = table[:, 2]
                    self.model.data_yerr = table[:, 3]

                    self.model.endResetModel()

                    first_index = self.model.index(0, 0)
                    last_index = self.model.index(nrows - 1, ncols - 1)

                    self.model.dataChanged.emit(first_index, last_index)

    def export_data(self):
        home = os.path.expanduser("~")

        path = QFileDialog.getSaveFileName(self.main_widget, "Save Table",  home, "Tables (*.tsv)")[0]

        if path != "":
            if not path.endswith('.tsv'):
                path += '.tsv'

            np.savetxt(path,
                       np.transpose([self.model.data_x, self.model.data_xerr, self.model.data_y, self.model.data_yerr]),
                       delimiter="\t", fmt='%1.6e')
