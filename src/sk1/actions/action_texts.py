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

from sk1 import _
from sk1.actions.action_ids import *

action_text = {
SELECT_MODE : _('Selection mode'),
SHAPER_MODE : _('Edit mode'),
ZOOM_MODE : _('Zoom mode'),
FLEUR_MODE : _('Fleur mode'),
LINE_MODE : _('Create polyline'),
CURVE_MODE : _('Create paths'),
RECT_MODE : _('Create rectangle'),
ELLIPSE_MODE : _('Create ellipse'),
TEXT_MODE : _('Create text'),
POLYGON_MODE : _('Create polygon'),
ZOOM_OUT_MODE : _('Zoom out mode'),
MOVE_MODE : _('Move mode'),
COPY_MODE : _('Copy mode'),
NEW : _('_New'),
OPEN : _('_Open'),
IMPORT_IMAGE : _('_Import image'),
SAVE : _('_Save'),
SAVE_AS : _('Save _As...'),
SAVE_ALL : _('Save All'),
CLOSE : _('_Close'),
CLOSE_ALL : _('_Close All'),
PRINT : _('_Print...'),
PRINT_SETUP : _('Print Setup...'),
QUIT : _('_Exit'),
UNDO : _('_Undo'),
REDO : _('_Redo'),
CLEAR_HISTORY : _('Clear undo history'),
CUT : _('Cu_t'),
CUT2 : _('Cut'),
CUT3 : _('Cut'),
COPY : _('_Copy'),
PASTE : _('_Paste'),
PASTE2 : _('_Paste'),
PASTE3 : _('_Paste'),
DELETE : _('_Delete'),
DELETE2 : _('_Delete'),
SELECT_ALL : _('_Select All'),
DESELECT : _('_Deselect'),
ZOOM_IN : _('Zoom in'),
ZOOM_OUT : _('Zoom out'),
ZOOM_PAGE : _('Fit zoom to page'),
ZOOM_100 : _('Zoom 100%'),
ZOOM_SELECTED : _('Zoom selected'),
ZOOM_PREVIOUS : _('Previous zoom'),
FORCE_REDRAW : _('Redraw document'),
PAGE_FRAME : _('Create page frame'),
PAGE_GUIDE_FRAME : _('Guides along page border'),
REMOVE_ALL_GUIDES : _('Remove all guides'),
GUIDES_AT_CENTER : _('Guides at page center'),
INSERT_PG : _('Insert page...'),
DELETE_PG : _('Delete page...'),
GOTO_PG : _('Go to page...'),
NEXT_PG : _('Next page'),
NEXT_PG_KP : _('Next page'),
PREV_PG : _('Previous page'),
PREV_PG_KP : _('Previous page'),
COMBINE : _('_Combine'),
BREAK_APART : _('_Break apart'),
GROUP : _('_Group'),
UNGROUP : _('_Ungroup'),
UNGROUP_ALL : _('U_ngroup all'),
CONVERT_TO_CURVES : _('Con_vert to curves'),
EDIT_TEXT : _('_Edit text...'),
SET_CONTAINER : _('_Place into container'),
UNPACK_CONTAINER : _('_Extract from container'),
PAGES : _('_Pages'),
LAYERS : _('_Layers'),
DOM_VIEWER : _('_Object browser'),
PROPERTIES : _('Document Properties...'),
PREFERENCES : _('Preferences...'),
REPORT_BUG : _('_Report bug'),
PROJECT_WEBSITE : _('Project _web site'),
PROJECT_FORUM : _('Project _forum'),
ABOUT : _('_About sK1'),
ROTATE_LEFT : _('Rotate _Left'),
ROTATE_RIGHT : _('Rotate _Right'),
VERT_MIRROR : _('Flip _vertically'),
HOR_MIRROR : _('Flip _horizontally'),
STROKE_VIEW : _('Stroke View'),
DRAFT_VIEW : _('Draft View'),
SHOW_GRID : _('Show grid'),
SHOW_GUIDES : _('Show guides'),
SHOW_SNAP : _('Show active snapping'),
SHOW_PAGE : _('Show page border'),
SNAP_TO_GRID : _('Snap to grid'),
SNAP_TO_GUIDES : _('Snap to guides'),
SNAP_TO_OBJECTS : _('Snap to objects'),
SNAP_TO_PAGE : _('Snap to page'),
}

action_tooltip_text = {
NEW : _('New'),
OPEN : _('Open'),
IMPORT_IMAGE : _('Import image'),
SAVE : _('Save'),
SAVE_AS : _('Save As...'),
CLOSE : _('Close'),
CLOSE_ALL : _('Close All'),
PRINT : _('Print'),
PRINT_SETUP : _('Print Setup'),
QUIT : _('Exit'),
UNDO : _('Undo'),
REDO : _('Redo'),
CUT : _('Cut'),
COPY : _('Copy'),
PASTE : _('Paste'),
PASTE2 : _('Paste'),
PASTE3 : _('Paste'),
DELETE : _('Delete'),
DELETE2 : _('Delete'),
SELECT_ALL : _('Select All'),
DESELECT : _('Deselect'),
INSERT_PG : _('Insert page'),
DELETE_PG : _('Delete page'),
GOTO_PG : _('Go to page'),
COMBINE : _('Combine'),
BREAK_APART : _('Break apart'),
GROUP : _('Group'),
UNGROUP : _('Ungroup'),
UNGROUP_ALL : _('Ungroup all'),
CONVERT_TO_CURVES : _('Convert to curves'),
EDIT_TEXT : _('Edit text'),
SET_CONTAINER : _('Place into container'),
UNPACK_CONTAINER : _('Extract from container'),
PAGES : _('Pages'),
LAYERS : _('Close'),
DOM_VIEWER : _('Object browser'),
REPORT_BUG : _('Report bug'),
PROJECT_WEBSITE : _('Project web site'),
PROJECT_FORUM : _('Project forum'),
ABOUT : _('About sK1'),
ROTATE_LEFT : _('Rotate Left'),
ROTATE_RIGHT : _('Rotate Right'),
VERT_MIRROR : _('Flip vertically'),
HOR_MIRROR : _('Flip horizontally'),
}

def get_action_text(action):
	if action in action_text.keys():
		return action_text[action]
	else:
		return '???'

def get_action_tooltip_text(action):
	if action in action_tooltip_text.keys():
		return action_tooltip_text[action]
	else:
		return get_action_text(action)
