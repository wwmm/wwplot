# -*- coding: utf-8 -*-

import os

import numpy as np
from gi.repository import Gdk, Gtk
from WWplot.export_table import ExportTable
from WWplot.fit import Fit
from WWplot.import_table import ImportTable

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')


class Table():

    def __init__(self, app):
        self.app = app

        self.selected_row = None
        self.fit_x = np.array([])
        self.fit_y = np.array([])
        self.hist_x = np.array([])
        self.hist_count = np.array([])

        self.module_path = os.path.dirname(__file__)

        self.builder = Gtk.Builder()

        self.builder.add_from_file(self.module_path + '/ui/table_ui.glade')

        self.builder.connect_signals(self)

        self.ui = self.builder.get_object('table_ui')
        self.liststore = self.builder.get_object('liststore')
        self.treeview = self.builder.get_object('treeview')

        self.button_switch_xy = self.builder.get_object('button_switch_xy')
        self.xerr_column = self.builder.get_object('xerr_column')
        self.y_column = self.builder.get_object('y_column')
        self.yerr_column = self.builder.get_object('yerr_column')

        self.fit_parameters_grid = self.builder.get_object(
            'fit_parameters_grid')
        self.fitfunc = self.builder.get_object('fitfunc')

        self.liststore.set_sort_column_id(0, Gtk.SortType.ASCENDING)

        self.init_fit()

        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

    def onXEdited(self, renderer, row_id, value):
        self.liststore[row_id][0] = float(value.replace(',', '.'))

        self.clear_fitlog()
        self.app.updatePlot()

    def onXerrEdited(self, renderer, row_id, value):
        self.liststore[row_id][1] = float(value.replace(',', '.'))

        self.clear_fitlog()
        self.app.updatePlot()

    def onYEdited(self, renderer, row_id, value):
        self.liststore[row_id][2] = float(value.replace(',', '.'))

        self.clear_fitlog()
        self.app.updatePlot()

    def onYerrEdited(self, renderer, row_id, value):
        self.liststore[row_id][3] = float(value.replace(',', '.'))

        self.clear_fitlog()
        self.app.updatePlot()

    def onAdd(self, button):
        self.liststore.append([0, 0, 0, 0])

        self.clear_fitlog()
        self.app.updatePlot()

    def onRemove(self, button):
        if self.selected_row is not None:
            self.liststore.remove(self.selected_row)

            self.clear_fitlog()
            self.app.updatePlot()

    def onSwapColumns(self, button):
        self.liststore.set_sort_column_id(
            Gtk.TREE_SORTABLE_UNSORTED_SORT_COLUMN_ID, Gtk.SortType.ASCENDING)

        row_iter = self.liststore.get_iter_first()

        while row_iter is not None:
            y, yerr, x, xerr = self.liststore.get(row_iter, 0, 1, 2, 3)

            self.liststore.set(row_iter, 0, x, 1, xerr, 2, y, 3, yerr)

            row_iter = self.liststore.iter_next(row_iter)

        self.liststore.set_sort_column_id(0, Gtk.SortType.ASCENDING)

        self.clear_fitlog()
        self.app.updatePlot()

    def getColumns(self):
        row_iter = self.liststore.get_iter_first()

        x, xerr, y, yerr = [], [], [], []

        while row_iter is not None:
            c0, c1, c2, c3 = self.liststore.get(row_iter, 0, 1, 2, 3)

            x.append(c0)
            xerr.append(c1)
            y.append(c2)
            yerr.append(c3)

            row_iter = self.liststore.iter_next(row_iter)

        return np.array(x), np.array(xerr), np.array(y), np.array(yerr)

    def onSelectionChanged(self, selection):
        model, self.selected_row = selection.get_selected()

    def onImportTable(self, button):
        it = ImportTable(self.app.window)

        if it.table is not None:
            self.liststore.clear()

            if len(it.table.shape) == 2:
                n_rows, n_cols = it.table.shape

                for row in it.table:
                    self.liststore.append([row[0], row[1], row[2], row[3]])

            elif len(it.table.shape) == 1:
                for row in it.table:
                    self.liststore.append([row, 0, 0, 0])

            self.clear_fitlog()
            self.app.updatePlot()

    def onExportTable(self, button):
        n_rows = len(self.liststore)

        if n_rows > 0:
            if self.app.do_histogram is False:
                n_cols = self.liststore.get_n_columns()
            else:
                n_cols = 1

            table = np.empty([n_rows, n_cols], dtype=float)

            row_iter = self.liststore.get_iter_first()

            idx = 0

            while row_iter is not None:
                c0, c1, c2, c3 = self.liststore.get(row_iter, 0, 1, 2, 3)

                if n_cols == 4:
                    table[idx, 0] = c0
                    table[idx, 1] = c1
                    table[idx, 2] = c2
                    table[idx, 3] = c3
                elif n_cols == 1:
                    table[idx, 0] = c0

                idx = idx + 1

                row_iter = self.liststore.iter_next(row_iter)

            ExportTable(self.app.window, table)

    def onKeyPressed(self, widget, event):
        if event.keyval == Gdk.keyval_from_name('c'):
            if (event.state == Gdk.ModifierType.CONTROL_MASK or
                    Gdk.ModifierType.MOD2_MASK):

                if self.selected_row is not None:
                    c0, c1, c2, c3 = self.liststore.get(self.selected_row, 0,
                                                        1, 2, 3)

                    row = [str(c0), str(c1), str(c2), str(c3)]

                    text = '\t'.join(row)

                    self.clipboard.set_text(text, -1)

        if event.keyval == Gdk.keyval_from_name('v'):
            if (event.state == Gdk.ModifierType.CONTROL_MASK
                    or Gdk.ModifierType.MOD2_MASK):

                if self.selected_row is not None:
                    text = self.clipboard.wait_for_text()

                    row = text.replace(',', '.').split('\t')

                    if len(row) == 4:
                        x, xerr, y, yerr = [float(i) for i in row]

                        self.liststore.set(self.selected_row, 0, x, 1, xerr, 2,
                                           y, 3, yerr)

                        self.clear_fitlog()
                        self.app.updatePlot()

    def init_fit(self):
        fitfunc = self.builder.get_object('fitfunc')
        self.fit_listbox = self.builder.get_object('fit_listbox')

        self.fit = Fit(maxit=200)

        self.fit.init_function(fitfunc.get_text())
        self.init_fit_parameters()

    def init_fit_parameters(self):
        grid_children = self.fit_parameters_grid.get_children()

        for child in grid_children:
            child.destroy()

        for n in range(len(self.fit.initial_P)):
            builder = Gtk.Builder()

            builder.add_from_file(self.module_path + '/ui/fit_parameter.glade')

            label = builder.get_object('parameter_label')
            spin = builder.get_object('parameter_value')
            parameter = builder.get_object('parameter')

            label.set_text('P[' + str(n) + ']')
            spin.set_value(self.fit.initial_P[n])

            self.fit_parameters_grid.attach(parameter, n, 0, 1, 1)

            spin.connect('value-changed', self.fit.on_parameter_changed, n)

            setattr(self, 'ui_fit_p' + str(n), spin)

    def onFitFunctionChanged(self, entry):
        self.fit.init_function(entry.get_text())
        self.init_fit_parameters()

    def clear_fitlog(self):
        self.fit_x = np.array([])
        self.fit_y = np.array([])

        children = self.fit_listbox.get_children()

        for child in children:
            self.fit_listbox.remove(child)

    def build_fitlog(self, result, result_err, stopreason):
        self.clear_fitlog()

        row = Gtk.ListBoxRow()
        row.add(Gtk.Label('Fit Output'))

        self.fit_listbox.add(row)

        for n in range(0, len(result)):
            label = 'P[' + str(n) + '] = ' + '{:.6}'.format(result[n]) + ' +- '
            label = label + '{:.6}'.format(result_err[n])

            row = Gtk.ListBoxRow()

            Label = Gtk.Label(label)
            Label.set_halign(Gtk.Align.START)

            row.add(Label)

            self.fit_listbox.add(row)

            ui_fit_p = getattr(self, 'ui_fit_p' + str(n))

            ui_fit_p.set_value(round(result[n], 2))

        row = Gtk.ListBoxRow()
        row.add(Gtk.Label())

        self.fit_listbox.add(row)

        for reason in stopreason:
            row = Gtk.ListBoxRow()
            row.add(Gtk.Label(reason))

            self.fit_listbox.add(row)

        self.fit_listbox.show_all()

    def onFit(self, button):
        self.clear_fitlog()

        x, xerr, y, yerr = self.getColumns()

        if len(x) > 1:
            if not self.app.do_histogram:
                self.fit.set_data(x, y, xerr, yerr)
            else:
                self.fit.set_data(self.hist_x, self.hist_count)

            stopreason = self.fit.run()

            result = self.fit.output
            result_err = self.fit.output_err

            self.build_fitlog(result, result_err, stopreason)

            func = self.fit.fit_function

            self.fit_x = x
            self.fit_y = func(result, x)

            self.app.updatePlot()
