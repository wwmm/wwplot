# -*- coding: utf-8 -*-

import os

import gi
import numpy as np
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class ExportTable(object):
    """Class that exports a CSV file"""

    def __init__(self, window, table):
        super(ExportTable, self).__init__()

        home_dir = os.path.expanduser('~')

        dialog = Gtk.FileChooserDialog("Export Table", window,
                                       Gtk.FileChooserAction.SAVE,
                                       (Gtk.STOCK_CANCEL,
                                        Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        dialog.set_current_folder(home_dir)

        self.add_filters(dialog)

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            path = dialog.get_filename()
            filter_name = dialog.get_filter().get_name()

            if not path.endswith(".csv"):
                path += ".csv"

            if filter_name == "CSV Table":
                np.savetxt(path, table, delimiter="\t")

        dialog.destroy()

    def add_filters(self, dialog):
        filter_csv = Gtk.FileFilter()
        filter_csv.set_name("CSV Table")
        filter_csv.add_mime_type("text/csv")

        dialog.add_filter(filter_csv)
