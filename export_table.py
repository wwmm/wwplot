# -*- coding: utf-8 -*-

import gi
import numpy as np
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class ExportTable(object):
    """docstring for ExportTable."""

    def __init__(self, window):
        super(ExportTable, self).__init__()
