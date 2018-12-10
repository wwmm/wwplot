#!/usr/bin/python
# -*- coding: utf-8 -*-

from WWplot.plot import Plot
from WWplot.table import Table
from gi.repository import Gdk, Gio, GLib, Gtk
import os

import gi
import numpy as np
gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')


class Application(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self, application_id='com.github.wwmm.wwplot')

        GLib.set_application_name('WWplot')

        GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, 2, self.quit)  # sigint

    def do_startup(self):
        Gtk.Application.do_startup(self)

        self.do_histogram = False
        self.show_grid = True
        self.xtitle = 'x'
        self.ytitle = 'y'
        self.plot_title = 'title'
        self.tables = []

        self.module_path = os.path.dirname(__file__)

        self.builder = Gtk.Builder()

        self.builder.add_from_file(self.module_path + '/ui/main_ui.glade')

        self.builder.connect_signals(self)

        self.window = self.builder.get_object('MainWindow')

        self.window.set_application(self)

        self.table_stack = self.builder.get_object('table_stack')

        self.apply_css_style('listbox.css')

        self.init_plot()
        self.init_menu()

        self.window.show_all()

    def do_activate(self):
        self.window.present()

    def do_shutdown(self):
        Gtk.Application.do_shutdown(self)

    def apply_css_style(self, css_file):
        provider = Gtk.CssProvider()

        css_file = Gio.File.new_for_path(self.module_path + '/ui/' + css_file)

        provider.load_from_file(css_file)

        screen = Gdk.Screen.get_default()
        priority = Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION

        Gtk.StyleContext.add_provider_for_screen(screen, provider, priority)

    def onAddTable(self, button):
        self.tables.append(Table(self))

        n = len(self.tables) - 1

        self.table_stack.add_titled(
            self.tables[-1].ui, 'table' + str(n), 'Table ' + str(n))

    def onRemoveTable(self, button):
        visible_child = self.table_stack.get_visible_child()

        for t in self.tables:
            if t.ui == visible_child:
                self.table_stack.remove(visible_child)

                self.tables.remove(t)

                break

        for n in range(len(self.tables)):
            self.table_stack.child_set_property(self.tables[n].ui, 'name',
                                                'table' + str(n))

            self.table_stack.child_set_property(self.tables[n].ui, 'title',
                                                'Table ' + str(n))

        self.updatePlot()

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

        # self.x = np.array(x)
        # self.xerr = np.array(xerr)
        # self.y = np.array(y)
        # self.yerr = np.array(yerr)

        if self.do_histogram:
            self.plot.set_margins(0.0)

            self.hist_count, self.hist_bin, patches = self.plot.hist(self.x)
        else:
            self.plot.set_margins(0.1)

            for t, n in zip(self.tables, range(len(self.tables))):
                x, xerr, y, yerr = t.getColumns()

                self.plot.errorbar(x, xerr, y, yerr, n)

            # self.plot.errorbar(self.x, self.xerr, self.y, self.yerr, 'bo')

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

    def onAbout(self, obj):
        builder = Gtk.Builder()

        builder.add_from_file(self.module_path + '/ui/about.glade')

        dialog = builder.get_object('about_dialog')

        dialog.set_transient_for(self.window)

        dialog.run()

        dialog.destroy()
