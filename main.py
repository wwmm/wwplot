#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

import gi
import numpy as np

gi.require_version('Gtk', '3.0')
from gi.repository import Gio, Gtk

from fit import Fit
from plot import Plot


class WWplot(Gtk.Application):
    """Main class."""

    def __init__(self):
        Gtk.Application.__init__(self, application_id="wwmm.wwplot")

        self.selected_row = None

    def do_startup(self):
        Gtk.Application.do_startup(self)

        main_ui_builder = Gtk.Builder()
        menu_builder = Gtk.Builder()

        main_ui_builder.add_from_file("ui.glade")
        menu_builder.add_from_file("menu.glade")

        handlers = {
            "onQuit": self.onQuit,
            "onXEdited": self.onXEdited,
            "onXerrEdited": self.onXerrEdited,
            "onYEdited": self.onYEdited,
            "onYerrEdited": self.onYerrEdited,
            "onAdd": self.onAdd,
            "onRemove": self.onRemove,
            "onSelectionChanged": self.onSelectionChanged,
            "onFitFunctionChanged": self.onFitFunctionChanged,
            "onFit": self.onFit
        }

        menu_handlers = {
            "onXtitleChanged": self.onXtitleChanged,
            "onYtitleChanged": self.onYtitleChanged
        }

        main_ui_builder.connect_signals(handlers)
        menu_builder.connect_signals(menu_handlers)

        self.window = main_ui_builder.get_object("MainWindow")

        headerbar = main_ui_builder.get_object("headerbar")

        self.window.set_titlebar(headerbar)
        self.window.set_application(self)

        self.create_appmenu()

        self.window.show_all()

        self.liststore = main_ui_builder.get_object("liststore")

        self.init_menu(main_ui_builder, menu_builder)
        self.init_plot(main_ui_builder)
        self.init_fit(main_ui_builder)

    def do_activate(self):
        self.window.present()

    def create_appmenu(self):
        menu = Gio.Menu()

        menu.append("About", "app.about")
        menu.append("Quit", "app.quit")

        self.set_app_menu(menu)

        # option "about"
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.onAbout)
        self.add_action(about_action)

        # option "quit"
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.onQuit)
        self.add_action(quit_action)

    def onQuit(self, event, data):
        self.quit()

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

    def onRemove(self, button):
        if self.selected_row is not None:
            self.liststore.remove(self.selected_row)

            self.updatePlot()

    def onSelectionChanged(self, selection):
        model, self.selected_row = selection.get_selected()

    def init_menu(self, main_ui_builder, menu_builder):
        button = main_ui_builder.get_object("popover_button")
        menu = menu_builder.get_object("menu")
        xtitle = menu_builder.get_object("xtitle")
        ytitle = menu_builder.get_object("ytitle")

        self.xtitle = xtitle.get_text()
        self.ytitle = ytitle.get_text()

        popover = Gtk.Popover.new(button)
        popover.props.transitions_enabled = True
        popover.add(menu)

        def on_click(arg):
            if popover.get_visible():
                popover.hide()
            else:
                popover.show_all()

        button.connect("clicked", on_click)

    def init_plot(self, main_ui_builder):
        plot_box = main_ui_builder.get_object("plot")

        self.x = np.array([])
        self.xerr = np.array([])
        self.y = np.array([])
        self.yerr = np.array([])

        # setting plot
        self.plot = Plot(self.window, plot_box)
        self.plot.set_grid(True)
        self.plot.set_xlabel(self.xtitle)
        self.plot.set_ylabel(self.ytitle)
        self.plot.tight_layout()

    def updatePlot(self):
        self.plot.axes.clear()
        self.plot.set_grid(True)
        self.plot.set_margins(0.03)
        self.plot.set_xlabel(self.xtitle)
        self.plot.set_ylabel(self.ytitle)

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

    def init_fit(self, main_ui_builder):
        fitfunc = main_ui_builder.get_object("fitfunc")
        self.fit_listbox = main_ui_builder.get_object("fit_listbox")

        self.fit = Fit()
        self.fit.init_function(fitfunc.get_text())

    def onFitFunctionChanged(self, button):
        self.fit.init_function(button.get_text())

    def build_fitlog(self, result, result_err):
        # First we clear the listbox
        children = self.fit_listbox.get_children()

        for child in children:
            self.fit_listbox.remove(child)

        row = Gtk.ListBoxRow()
        row.add(Gtk.Label("Fit Output"))

        self.fit_listbox.add(row)

        for n in range(0, len(result)):
            label = "P[" + str(n) + "] = " + '{:.6}'.format(result[n]) + " +- "
            label = label + '{:.6}'.format(result_err[n])

            row = Gtk.ListBoxRow()
            row.add(Gtk.Label(label))

            self.fit_listbox.add(row)

        self.fit_listbox.show_all()

    def onFit(self, button):
        if len(self.x) > 1:
            self.updatePlot()

            self.fit.set_data(self.x, self.y, self.xerr, self.yerr)

            self.fit.run()

            result = self.fit.output
            result_err = self.fit.output_err

            self.build_fitlog(result, result_err)

            func = self.fit.fit_function

            self.plot.plot(self.x, func(result, self.x), "r-")
            self.plot.update()

    def onAbout(self, action, parameter):
        builder = Gtk.Builder()

        builder.add_from_file("about.glade")

        dialog = builder.get_object("about_dialog")

        dialog.set_transient_for(self.window)

        dialog.show()

if __name__ == "__main__":
    w = WWplot()

    exit_status = w.run(sys.argv)

    sys.exit(exit_status)
