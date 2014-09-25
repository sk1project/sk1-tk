# -*- coding: utf-8 -*-
#
#	Copyright (C) 2012-2014 by Igor E. Novikov
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

import os
import gtk

from sk1 import _, config


STOCK_SK1_DOC = 'document-icon'
STOCK_DONT_SAVE = 'action-dont-save'
STOCK_ROTATE_LEFT = 'object-rotate-left'
STOCK_ROTATE_RIGHT = 'object-rotate-right'
STOCK_HOR_MIRROR = 'object-horizontal-mirror'
STOCK_VERT_MIRROR = 'object-vertical-mirror'
STOCK_TO_CURVE = 'object-to-curve'

STOCK_PLUGIN_LAYERS = 'plugin-layers'
STOCK_PLUGIN_DOM_VIEWER = 'plugin-dom-viewer'
STOCK_PLUGIN_PAGES = 'plugin-pages'

STOCK_SNAP_TO_GRID = 'snap-to-grid'
STOCK_SNAP_TO_GUIDES = 'snap-to-guides'
STOCK_SNAP_TO_OBJECTS = 'snap-to-objects'
STOCK_SNAP_TO_PAGE = 'snap-to-page'

STOCK_PAGE_FRAME = 'page-frame'
STOCK_PAGE_GUIDE_FRAME = 'page-guide-frame'
STOCK_GUIDES_AT_CENTER = 'guides-at-center'
STOCK_REMOVE_ALL_GUIDES = 'remove-all-guides'

FIXED16 = gtk.icon_size_register('FIXED16', 16, 16)
FIXED22 = gtk.icon_size_register('FIXED22', 22, 22)
FIXED24 = gtk.icon_size_register('FIXED24', 24, 24)
FIXED32 = gtk.icon_size_register('FIXED32', 32, 32)

def load_icons():

	items = [STOCK_ROTATE_LEFT, STOCK_ROTATE_RIGHT, STOCK_HOR_MIRROR,
			STOCK_VERT_MIRROR, STOCK_TO_CURVE, STOCK_PLUGIN_LAYERS,
			STOCK_PLUGIN_DOM_VIEWER, STOCK_PLUGIN_PAGES, STOCK_SNAP_TO_GRID,
			STOCK_SNAP_TO_GUIDES, STOCK_SNAP_TO_OBJECTS, STOCK_SNAP_TO_PAGE,
			STOCK_PAGE_FRAME, STOCK_PAGE_GUIDE_FRAME, STOCK_GUIDES_AT_CENTER,
			STOCK_REMOVE_ALL_GUIDES, STOCK_SK1_DOC]

	path = '' + os.path.join(config.resource_dir, 'icons')

	iconfactory = gtk.IconFactory()

	for item in items:
		gtk.stock_add([(item, '', 0, 0, ''), ])
		pixbuf = gtk.gdk.pixbuf_new_from_file(os.path.join(path, item + '.png'))
		source = gtk.IconSource()
		source.set_pixbuf(pixbuf)
		source.set_size_wildcarded(True)
		iconset = gtk.IconSet()
		iconset.add_source(source)
		iconfactory.add(item, iconset)

	#Creating aliased icons
	items = [(STOCK_DONT_SAVE, _("_Don't save"), 0, 0, None), ]

	aliases = [(STOCK_DONT_SAVE, gtk.STOCK_NO), ]

	gtk.stock_add(items)

	for item, alias in aliases:
		iconset = gtk.icon_factory_lookup_default(alias)
		iconfactory.add(item, iconset)

	iconfactory.add_default()
