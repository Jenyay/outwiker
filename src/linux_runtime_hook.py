# -*- coding: utf-8 -*-

import os
import sys

os.environ['GDK_PIXBUF_MODULE_FILE'] = sys._MEIPASS + '/lib/gdk-pixbuf/loaders.cache'
os.environ['LD_LIBRARY_PATH'] = sys._MEIPASS
# os.environ['GTK_THEME'] = 'Adwaita'

# print u'LD_LIBRARY_PATH = {}'.format(os.environ['LD_LIBRARY_PATH'])
# print u'GDK_PIXBUF_MODULE_FILE = {}'.format(os.environ['GDK_PIXBUF_MODULE_FILE'])
# print u'GTK_THEME = {}'.format(os.environ['GTK_THEME'])
