# -*- coding: utf-8 -*-
#
#	Copyright (C) 2014 by Igor E. Novikov
#
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os, gtk
from sk1 import config

IMG_APP_ICON = 'sk1-app-icon'
IMG_CAIRO_BANNER = 'sk1-cairo-banner'
IMG_SPLASH_TRIADA = 'sk1-splash-triada'

IMG_RULER_BG = 'sk1-ruler-corner-bg'
IMG_RULER_DO_LL = 'sk1-ruler-docorigin-ll'
IMG_RULER_DO_LU = 'sk1-ruler-docorigin-lu'
IMG_RULER_DO_C = 'sk1-ruler-docorigin-c'

IMG_PAGER_END = 'sk1-pager-end'
IMG_PAGER_NEXT = 'sk1-pager-next'
IMG_PAGER_PREV = 'sk1-pager-prev'
IMG_PAGER_START = 'sk1-pager-start'

IMG_PREFS_CMS = 'sk1-prefs-cms'
IMG_PREFS_CMS_BANNER = 'sk1-prefs-cms-banner'
IMG_PREFS_RULER = 'sk1-prefs-ruler'
IMG_PREFS_PALETTE = 'sk1-prefs-palette'

IMG_CTX_JUMP = 'sk1-ctx-jump'
IMG_CTX_UNITS = 'sk1-ctx-units'
IMG_CTX_LANDSCAPE = 'sk1-ctx-page-landscape'
IMG_CTX_PORTRAIT = 'sk1-ctx-page-portrait'
IMG_CTX_ROTATE = 'sk1-ctx-rotate-selection'
IMG_KEEP_RATIO = 'sk1-ctx-keep-ratio'
IMG_DONT_KEEP_RATIO = 'sk1-ctx-dont-keep-ratio'

def get_image_path(image_id):
	imgdir = os.path.join(config.resource_dir, 'images')
	imgname = image_id + '.png'
	return os.path.join(imgdir, imgname)

def get_pixbuf(image_id):
	loader = gtk.gdk.pixbuf_new_from_file
	return loader(get_image_path(image_id))

def get_stock_pixbuf(image_id, size):
	return gtk.Image().render_icon(image_id, size)

def get_image(image_id):
	image = gtk.Image()
	image.set_from_pixbuf(get_pixbuf(image_id))
	return image

def get_stock_image(image_id, size):
	image = gtk.Image()
	image.set_from_pixbuf(get_stock_pixbuf(image_id, size))
	return image
