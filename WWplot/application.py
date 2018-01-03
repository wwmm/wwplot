#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import gi
import numpy as np
gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Gdk, Gio, GLib, Gtk

from WWplot.export_table import ExportTable
from WWplot.fit import Fit
from WWplot.import_table import ImportTable
from WWplot.plot import Plot


class Application(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self, application_id='com.github.wwmm.wwplot')

        GLib.set_application_name('WWplot')

        GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, 2, self.quit)  # sigint

    def do_startup(self):
        Gtk.Application.do_startup(self)

        self.selected_row = None
        self.do_histogram = False
        self.show_grid = True
        self.xtitle = 'x'
        self.ytitle = 'y'
        self.plot_title = 'title'
        self.module_path = os.path.dirname(__file__)

        self.builder = Gtk.Builder()

        self.builder.add_from_file(self.module_path + '/ui/main_ui.glade')

        self.builder.connect_signals(self)

        self.window = self.builder.get_object('MainWindow')

        self.window.set_application(self)

        self.liststore = self.builder.get_object('liststore')

        self.fit_parameters_grid = self.builder.get_object(
            'fit_parameters_grid')

        self.xerr_column = self.builder.get_object('xerr_column')
        self.y_column = self.builder.get_object('y_column')
        self.yerr_column = self.builder.get_object('yerr_column')

        self.fitfunc = self.builder.get_object('fitfunc')

        self.button_switch_xy = self.builder.get_object('button_switch_xy')

        self.create_appmenu()

        self.init_plot()
        self.init_menu()
        self.init_fit()

        self.window.show_all()

        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

    def do_activate(self):
        self.window.present()

    def do_shutdown(self):
        Gtk.Application.do_shutdown(self)

    def create_appmenu(self):
        menu = Gio.Menu()

        menu.append('About', 'app.about')
        menu.append('Quit', 'app.quit')

        self.set_app_menu(menu)

        about_action = Gio.SimpleAction.new('about', None)
        about_action.connect('activate', self.onAbout)
        self.add_action(about_action)

        quit_action = Gio.SimpleAction.new('quit', None)
        quit_action.connect('activate', lambda action, parameter: self.quit())
        self.add_action(quit_action)

    def onXEdited(self, renderer, row_id, value):
        self.liststore[row_id][0] = float(value.replace(',', '.'))
        self.updatePlot()

    def onXerrEdited(self, renderer, row_id, value):
        self.liststore[row_id][1] = float(value.replace(',', '.'))
        self.updatePlot()

    def onYEdited(self, renderer, row_id, value):
        self.liststore[row_id][2] = float(value.replace(',', '.'))
        self.updatePlot()

    def onYerrEdited(self, renderer, row_id, value):
        self.liststore[row_id][3] = float(value.replace(',', '.'))
        self.updatePlot()

    def onAdd(self, button):
        self.liststore.append([0, 0, 0, 0])
        self.updatePlot()
        self.clear_fitlog()

    def onRemove(self, button):
        if self.selected_row is not None:
            self.liststore.remove(self.selected_row)
            self.updatePlot()
            self.clear_fitlog()

    def onImportTable(self, button):
        it = ImportTable(self.window)

        if it.table is not None:
            self.liststore.clear()

            if len(it.table.shape) == 2:
                n_rows, n_cols = it.table.shape

                for row in it.table:
                    self.liststore.append([row[0], row[1], row[2], row[3]])

            elif len(it.table.shape) == 1:
                for row in it.table:
                    self.liststore.append([row, 0, 0, 0])

            self.updatePlot()
            self.clear_fitlog()

    def onExportTable(self, button):
        n_rows = len(self.liststore)

        if n_rows > 0:
            if self.do_histogram is False:
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

            ExportTable(self.window, table)

    def onSwapColumns(self, button):
        row_iter = self.liststore.get_iter_first()

        while row_iter is not None:
            y, yerr, x, xerr = self.liststore.get(row_iter, 0, 1, 2, 3)

            self.liststore.set(row_iter, 0, x, 1, xerr, 2, y, 3, yerr)

            row_iter = self.liststore.iter_next(row_iter)

        self.updatePlot()
        self.clear_fitlog()

    def onSelectionChanged(self, selection):
        model, self.selected_row = selection.get_selected()

    def onKeyPressed(self, widget, event):
        if event.keyval == Gdk.keyval_from_name('c'):
            if (event.state == Gdk.ModifierType.CONTROL_MASK or
                    Gdk.ModifierType.MOD2_MASK):

                if self.selected_row is not None:
                    idx = self.selected_row

                    c0, c1, c2, c3 = self.liststore.get(idx, 0, 1, 2, 3)

                    row = [str(c0), str(c1), str(c2), str(c3)]

                    text = '\t'.join(row)

                    self.clipboard.set_text(text, -1)

        if event.keyval == Gdk.keyval_from_name('v'):
            if (event.state == Gdk.ModifierType.CONTROL_MASK or
                    Gdk.ModifierType.MOD2_MASK):

                if self.selected_row is not None:
                    idx = self.selected_row

                    text = self.clipboard.wait_for_text()

                    row = text.replace(',', '.').split('\t')

                    if len(row) == 4:
                        x, xerr, y, yerr = [float(i) for i in row]

                        self.liststore.set(idx, 0, x, 1, xerr, 2, y, 3, yerr)

                        self.updatePlot()
                        self.clear_fitlog()

    def init_menu(self):
        button = self.builder.get_object('popover_button')
        menu = self.builder.get_object('menu')
        xtitle = self.builder.get_object('xtitle')
        ytitle = self.builder.get_object('ytitle')
        plot_title = self.builder.get_object('plot_title')
        show_grid = self.builder.get_object('show_grid')

        self.xtitle = xtitle.get_text()
        self.ytitle = ytitle.get_text()
        self.plot_title = plot_title.get_text()

        show_grid.set_active(self.show_grid)

        popover = Gtk.Popover.new(button)
        popover.props.transitions_enabled = True
        popover.add(menu)

        def on_click(arg):
            if popover.get_visible():
                popover.hide()
            else:
                popover.show_all()

        button.connect('clicked', on_click)

    def init_plot(self):
        plot_box = self.builder.get_object('plot')

        self.x = np.array([])
        self.xerr = np.array([])
        self.y = np.array([])
        self.yerr = np.array([])

        # setting plot
        self.plot = Plot(self.window, plot_box)
        self.plot.set_grid(self.show_grid)
        self.plot.set_xlabel(self.xtitle)
        self.plot.set_ylabel(self.ytitle)
        self.plot.set_title(self.plot_title)
        self.plot.tight_layout()

    def updatePlot(self):
        self.plot.axes.clear()
        self.plot.set_grid(self.show_grid)
        self.plot.set_xlabel(self.xtitle)
        self.plot.set_ylabel(self.ytitle)
        self.plot.set_title(self.plot_title)

        row_iter = self.liststore.get_iter_first()

        x, xerr, y, yerr = [], [], [], []

        while row_iter is not None:
            c0, c1, c2, c3 = self.liststore.get(row_iter, 0, 1, 2, 3)

            x.append(c0)
            xerr.append(c1)
            y.append(c2)
            yerr.append(c3)

            row_iter = self.liststore.iter_next(row_iter)

        self.x = np.array(x)
        self.xerr = np.array(xerr)
        self.y = np.array(y)
        self.yerr = np.array(yerr)

        if self.do_histogram:
            self.plot.set_margins(0.0)

            self.hist_count, self.hist_bin, patches = self.plot.hist(self.x)
        else:
            self.plot.set_margins(0.1)

            self.plot.errorbar(self.x, self.xerr, self.y, self.yerr, 'bo')

        self.plot.update()

    def onXtitleChanged(self, button):
        self.xtitle = button.get_text()
        self.plot.set_xlabel(self.xtitle)
        self.plot.update()

    def onYtitleChanged(self, button):
        self.ytitle = button.get_text()
        self.plot.set_ylabel(self.ytitle)
        self.plot.update()

    def onTitleChanged(self, button):
        self.plot_title = button.get_text()
        self.plot.set_title(self.plot_title)
        self.plot.update()

    def on_show_grid_state_set(self, button, state):
        self.show_grid = state
        self.updatePlot()

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
            row.add(Gtk.Label(label))

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
        if len(self.x) > 1:
            self.updatePlot()

            if self.do_histogram is False:
                self.fit.set_data(self.x, self.y, self.xerr, self.yerr)
            else:
                self.fit.set_data(self.hist_bin[:-1], self.hist_count)

            stopreason = self.fit.run()

            result = self.fit.output
            result_err = self.fit.output_err

            self.build_fitlog(result, result_err, stopreason)

            func = self.fit.fit_function

            if self.do_histogram is False:
                self.plot.plot(self.x, func(result, self.x), 'r-')
            else:
                self.plot.plot(
                    self.hist_bin[:-1], func(result, self.hist_bin[:-1]), 'r-')

            self.plot.update()

    def onModeChanged(self, button, state):
        if state is True:  # do histogram
            self.do_histogram = True

            self.xerr_column.set_visible(False)
            self.y_column.set_visible(False)
            self.yerr_column.set_visible(False)

            equation = '(1.0 / (P[0] * sqrt(2 * pi))) * '
            equation = equation + 'exp(- (x - P[1])**2 / (2 * P[0]**2))'

            self.fitfunc.set_text(equation)

            self.button_switch_xy.hide()
        else:  # do xy plot
            self.do_histogram = False

            self.xerr_column.set_visible(True)
            self.y_column.set_visible(True)
            self.yerr_column.set_visible(True)

            equation = 'P[0] * x + P[1]'

            self.fitfunc.set_text(equation)

            self.button_switch_xy.show_all()

        self.updatePlot()
        self.clear_fitlog()

    def onAbout(self, action, parameter):
        builder = Gtk.Builder()

        builder.add_from_file('ui/about.glade')

        dialog = builder.get_object('about_dialog')

        dialog.set_transient_for(self.window)

        dialog.run()

        dialog.destroy()
