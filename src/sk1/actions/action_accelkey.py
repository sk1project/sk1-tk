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


from sk1.actions.action_ids import *

accelkeys = {
NEW : '<Control>N',
OPEN : '<Control>O',
SAVE : '<Control>S',
CLOSE : '<Control>W',
PRINT : '<Control>P',
QUIT : '<Alt>F4',
UNDO : '<Control>Z',
REDO : '<Control><Shift>Z',
CUT : '<Control>X',
CUT2 : '<Shift>Delete',
CUT3 : '<Shift>KP_Decimal',
COPY : '<Control>C',
PASTE : '<Control>V',
PASTE2 : '<Shift>Insert',
PASTE3 : '<Shift>KP_0',
DELETE : 'Delete',
DELETE2 : 'KP_Delete',
SELECT_ALL : '<Control>A',
DESELECT : '<Control><Shift>A',
ZOOM_IN : '<Control>equal',
ZOOM_OUT : '<Control>minus',
ZOOM_PAGE : '<Shift>F4',
ZOOM_SELECTED : 'F4',
ZOOM_PREVIOUS : 'F3',
FORCE_REDRAW : '<Alt>R',
NEXT_PG : 'Page_Down',
NEXT_PG_KP : 'KP_Page_Down',
PREV_PG : 'Page_Up',
PREV_PG_KP : 'KP_Page_Up',
COMBINE : '<Control>L',
BREAK_APART : '<Control>K',
GROUP : '<Control>G',
UNGROUP : '<Control>U',
CONVERT_TO_CURVES : '<Control>Q',
EDIT_TEXT : 'F8',
PAGES : '<Control>F7',
LAYERS : 'F7',
STROKE_VIEW : '<Shift>F9',
SNAP_TO_GRID : '<Control>Y',
SNAP_TO_GUIDES : '<Control>I',
}

def get_action_accelkey(action):
	if action in accelkeys.keys():
		return accelkeys[action]
	else:
		return None
