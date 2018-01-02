# -*- coding: utf-8 -*-

import gi
import numpy as np
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class ImportTable(object):
    '''Class that imports table files'''

    def __init__(self, window):
        super(ImportTable, self).__init__()

        self.table = None

        dialog = Gtk.FileChooserDialog('Import Table', window,
                                       Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL,
                                        Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        self.add_filters(dialog)

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            path = dialog.get_filename()
            filter_name = dialog.get_filter().get_name()

            if filter_name == 'TSV Table':
                self.table = np.genfromtxt(path, delimiter='\t')

        dialog.destroy()

    def add_filters(self, dialog):
        filter_csv = Gtk.FileFilter()
        filter_csv.set_name('TSV Table')
        filter_csv.add_mime_type('text/tab-separated-values')

        dialog.add_filter(filter_csv)
