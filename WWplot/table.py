# -*- coding: utf-8 -*-

import os

import numpy as np
from PySide2.QtCore import QEvent, QObject, Qt
from PySide2.QtGui import (QColor, QDoubleValidator, QGuiApplication,
                           QKeySequence)
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import (QFileDialog, QFrame, QGraphicsDropShadowEffect,
                               QGridLayout, QHeaderView, QLabel, QLineEdit,
                               QPushButton, QRadioButton, QSizePolicy,
                               QTableView)
from WWplot.fit import Fit
from WWplot.model import Model


class Table(QObject):
    def __init__(self):
        QObject.__init__(self)

        self.do_histogram = False

        self.module_path = os.path.dirname(__file__)

        loader = QUiLoader()

        self.main_widget = loader.load(self.module_path + "/ui/table.ui")

        self.table_view = self.main_widget.findChild(QTableView, "table_view")
        button_add_row = self.main_widget.findChild(QPushButton, "button_add_row")
        button_import = self.main_widget.findChild(QPushButton, "button_import")
        button_export = self.main_widget.findChild(QPushButton, "button_export")
        button_fit = self.main_widget.findChild(QPushButton, "button_fit")
        button_calc = self.main_widget.findChild(QPushButton, "button_calc")
        fit_frame = self.main_widget.findChild(QFrame, "fit_frame")
        table_cfg_frame = self.main_widget.findChild(QFrame, "table_cfg_frame")
        self.equation = self.main_widget.findChild(QLineEdit, "equation")
        self.legend = self.main_widget.findChild(QLineEdit, "legend_name")
        self.fit_params_layout = self.main_widget.findChild(QGridLayout, "fit_params_layout")
        self.radio_xy = self.main_widget.findChild(QRadioButton, "radio_xy")
        self.radio_histogram = self.main_widget.findChild(QRadioButton, "radio_histogram")

        self.model = Model()

        button_add_row.clicked.connect(self.add_row)
        button_import.clicked.connect(self.import_data)
        button_export.clicked.connect(self.export_data)
        button_fit.clicked.connect(self.run_fit)
        button_calc.clicked.connect(self.calc_equation)
        self.equation.returnPressed.connect(self.init_fit_params)
        self.model.dataChanged.connect(self.data_changed)
        self.radio_xy.toggled.connect(self.on_chart_type_toggled)
        self.radio_histogram.toggled.connect(self.on_chart_type_toggled)

        self.table_view.installEventFilter(self)

        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table_view.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table_view.setModel(self.model)

        # effects

        button_add_row.setGraphicsEffect(self.button_shadow())
        button_import.setGraphicsEffect(self.button_shadow())
        button_export.setGraphicsEffect(self.button_shadow())
        button_fit.setGraphicsEffect(self.button_shadow())
        button_calc.setGraphicsEffect(self.button_shadow())
        fit_frame.setGraphicsEffect(self.card_shadow())
        table_cfg_frame.setGraphicsEffect(self.card_shadow())

        # fit

        self.show_fit_curve = False
        self.fit = Fit()

        self.init_fit_params()

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

    def data_changed(self):
        self.show_fit_curve = False

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

    def run_fit(self):
        if self.model.data_x.size > 1:
            self.fit.set_data(self.model.data_x, self.model.data_y, self.model.data_xerr, self.model.data_yerr)

            self.show_fit_curve = True

            self.fit.run()

            self.view_fit_output()

    def init_fit_output_layout(self):
        ncols = self.fit_params_layout.columnCount()
        nrows = self.fit_params_layout.rowCount()
        nparams = len(self.fit.parameters)

        for i in range(nrows):
            for j in range(ncols):
                item = self.fit_params_layout.itemAtPosition(i, j)

                if item:
                    widget = item.widget()

                    if widget:
                        if i > nparams - 1:
                            widget.setVisible(False)
                        else:
                            widget.setVisible(True)

                            if j == 1:
                                widget.setText(str(self.fit.parameters[i]))

                            if j == 2:
                                widget.setText("Error = +- 0")

        if nparams > nrows:
            first_idx = 0

            if nrows > 1:
                first_idx = nrows

            for n in range(first_idx, nparams):
                size_policy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
                size_policy1.setHorizontalStretch(0)
                size_policy1.setVerticalStretch(0)

                p_label = QLabel("P[" + str(n) + "]")
                p_label.setAlignment(Qt.AlignJustify | Qt.AlignVCenter)
                p_label.setSizePolicy(size_policy1)

                self.fit_params_layout.addWidget(p_label, n, 0)

                size_policy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
                size_policy2.setHorizontalStretch(1)
                size_policy2.setVerticalStretch(0)

                validator = QDoubleValidator()
                validator.setDecimals(6)
                validator.setNotation(QDoubleValidator.StandardNotation)

                p_value = QLineEdit()
                p_value.setValidator(validator)
                p_value.setText(str(self.fit.parameters[i]))
                p_value.setSizePolicy(size_policy2)
                p_value.returnPressed.connect(self.calc_equation)

                self.fit_params_layout.addWidget(p_value, n, 1)

                size_policy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
                size_policy3.setHorizontalStretch(0)
                size_policy3.setVerticalStretch(0)

                error_label = QLabel("Error = +- 0")
                error_label.setSizePolicy(size_policy3)

                self.fit_params_layout.addWidget(error_label, n, 2)

    def init_fit_params(self):
        self.fit.init_function(self.equation.displayText())

        self.init_fit_output_layout()

    def view_fit_output(self):
        ncols = self.fit_params_layout.columnCount()

        for i in range(len(self.fit.parameters)):
            for j in range(1, ncols):
                item = self.fit_params_layout.itemAtPosition(i, j)

                if item:
                    widget = item.widget()

                    if widget:
                        if j == 1:
                            widget.setText("{0:.6e}".format(self.fit.parameters[i]))

                        if j == 2:
                            widget.setText("Error = +- {0:.6e}".format(self.fit.parameters_err[i]))

    def calc_equation(self):
        ncols = self.fit_params_layout.columnCount()

        for i in range(len(self.fit.parameters)):
            for j in range(1, ncols):
                item = self.fit_params_layout.itemAtPosition(i, j)

                if item:
                    widget = item.widget()

                    if widget:
                        if j == 1:
                            self.fit.parameters[i] = float(widget.text())

        self.show_fit_curve = True
        self.fit.finished.emit()  # updating the plot

    def on_chart_type_toggled(self, state):
        if state:
            if self.radio_xy.isChecked():
                self.table_view.setColumnHidden(1, False)
                self.table_view.setColumnHidden(2, False)
                self.table_view.setColumnHidden(3, False)

                self.do_histogram = False
            else:
                self.table_view.setColumnHidden(1, True)
                self.table_view.setColumnHidden(2, True)
                self.table_view.setColumnHidden(3, True)

                self.do_histogram = True
