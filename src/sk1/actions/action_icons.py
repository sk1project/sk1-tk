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

import gtk
from sk1 import rc
from sk1.actions.action_ids import *

action_icon = {
NEW : gtk.STOCK_NEW,
OPEN : gtk.STOCK_OPEN,
SAVE : gtk.STOCK_SAVE,
SAVE_AS : gtk.STOCK_SAVE_AS,
CLOSE : gtk.STOCK_CLOSE,
PRINT : gtk.STOCK_PRINT,
PRINT_SETUP : gtk.STOCK_PRINT_PREVIEW,
QUIT : gtk.STOCK_QUIT,
UNDO : gtk.STOCK_UNDO,
REDO : gtk.STOCK_REDO,
CUT : gtk.STOCK_CUT,
CUT2 : gtk.STOCK_CUT,
CUT3 : gtk.STOCK_CUT,
COPY : gtk.STOCK_COPY,
PASTE : gtk.STOCK_PASTE,
DELETE : gtk.STOCK_DELETE,
SELECT_ALL : gtk.STOCK_SELECT_ALL,
ZOOM_IN : gtk.STOCK_ZOOM_IN,
ZOOM_OUT : gtk.STOCK_ZOOM_OUT,
ZOOM_PAGE : gtk.STOCK_FILE,
ZOOM_100 : gtk.STOCK_ZOOM_100,
ZOOM_SELECTED : gtk.STOCK_ZOOM_FIT,
FORCE_REDRAW : gtk.STOCK_REFRESH,
PAGE_FRAME : rc.STOCK_PAGE_FRAME,
PAGE_GUIDE_FRAME : rc.STOCK_PAGE_GUIDE_FRAME,
REMOVE_ALL_GUIDES : rc.STOCK_REMOVE_ALL_GUIDES,
GUIDES_AT_CENTER : rc.STOCK_GUIDES_AT_CENTER,
CONVERT_TO_CURVES : rc.STOCK_TO_CURVE,
PAGES : rc.STOCK_PLUGIN_PAGES,
LAYERS : rc.STOCK_PLUGIN_LAYERS,
DOM_VIEWER : rc.STOCK_PLUGIN_DOM_VIEWER,
PROPERTIES : gtk.STOCK_PROPERTIES,
PREFERENCES : gtk.STOCK_PREFERENCES,
REPORT_BUG : gtk.STOCK_DIALOG_WARNING,
ABOUT : gtk.STOCK_ABOUT,
ROTATE_LEFT : rc.STOCK_ROTATE_LEFT,
ROTATE_RIGHT : rc.STOCK_ROTATE_RIGHT,
VERT_MIRROR : rc.STOCK_VERT_MIRROR,
HOR_MIRROR : rc.STOCK_HOR_MIRROR,
SNAP_TO_GRID : rc.STOCK_SNAP_TO_GRID,
SNAP_TO_GUIDES : rc.STOCK_SNAP_TO_GUIDES,
SNAP_TO_OBJECTS : rc.STOCK_SNAP_TO_OBJECTS,
SNAP_TO_PAGE : rc.STOCK_SNAP_TO_PAGE,
}

def get_action_icon(action):
	if action in action_icon.keys():
		return action_icon[action]
	else:
		return None
