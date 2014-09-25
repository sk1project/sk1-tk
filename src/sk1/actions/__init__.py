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

from sk1.events import CLIPBOARD, DOC_CHANGED, PAGE_CHANGED, \
DOC_CLOSED, DOC_MODIFIED, DOC_SAVED, NO_DOCS, SELECTION_CHANGED, connect

from action_ids import *
from action_icons import get_action_icon
from action_texts import get_action_text, get_action_tooltip_text
from action_accelkey import get_action_accelkey

def create_actions(app):
	insp = app.inspector
	proxy = app.proxy
	actions = []
	doc_chnl = [connect, NO_DOCS, DOC_CHANGED]
	docm_chnl = [connect, NO_DOCS, DOC_CHANGED, DOC_MODIFIED]
	page_chnl = docm_chnl + [PAGE_CHANGED]
	sel_chnl = [connect, NO_DOCS, DOC_CHANGED, SELECTION_CHANGED]
	entries = [
#	id, callable, [channels], validator, args
#	name, label, tooltip, icon, shortcut, callable, [channels], validator, args
#gtk.accelerator_name(ord('+'),gtk.gdk.CONTROL_MASK)
[SELECT_MODE, proxy.set_select_mode, doc_chnl, insp.is_doc],
[SHAPER_MODE, proxy.set_shaper_mode, doc_chnl, insp.is_doc],
[ZOOM_MODE, proxy.set_zoom_mode, doc_chnl, insp.is_doc],
[FLEUR_MODE, proxy.set_fleur_mode, doc_chnl, insp.is_doc],
[LINE_MODE, proxy.set_line_mode, doc_chnl, insp.is_doc],
[CURVE_MODE, proxy.set_curve_mode, doc_chnl, insp.is_doc],
[RECT_MODE, proxy.set_rect_mode, doc_chnl, insp.is_doc],
[ELLIPSE_MODE, proxy.set_ellipse_mode, doc_chnl, insp.is_doc],
[TEXT_MODE, proxy.set_text_mode, doc_chnl, insp.is_doc],
[POLYGON_MODE, proxy.set_polygon_mode, doc_chnl, insp.is_doc],
[ZOOM_OUT_MODE, proxy.set_zoom_out_mode, doc_chnl, insp.is_doc],
[MOVE_MODE, proxy.set_move_mode, doc_chnl, insp.is_doc],
[COPY_MODE, proxy.set_copy_mode, doc_chnl, insp.is_doc],
[NEW, proxy.new, None, None],
[OPEN, proxy.open, None, None],
[IMPORT_IMAGE, proxy.import_image, None, None],
[SAVE, proxy.save, docm_chnl + [DOC_SAVED, ], insp.is_doc_not_saved],
[SAVE_AS, proxy.save_as, doc_chnl, insp.is_doc],
[SAVE_ALL, proxy.save_all, docm_chnl + [DOC_SAVED, ], insp.is_any_doc_not_saved],
[CLOSE, proxy.close, doc_chnl, insp.is_doc],
[CLOSE_ALL, proxy.close_all, doc_chnl, insp.is_doc],
[PRINT, proxy.do_print, doc_chnl, insp.is_doc],
[PRINT_SETUP, proxy.do_print_setup, doc_chnl, insp.is_doc],
[QUIT, proxy.exit, None, None],
[UNDO, proxy.undo, docm_chnl + [DOC_CLOSED, ], insp.is_undo],
[REDO, proxy.redo, docm_chnl + [DOC_CLOSED, ], insp.is_redo],
[CLEAR_HISTORY, proxy.clear_history, docm_chnl + [DOC_CLOSED, ], insp.is_history],
[CUT, proxy.cut, sel_chnl, insp.is_selection],
[CUT2, proxy.cut, sel_chnl, insp.is_selection],
[CUT3, proxy.cut, sel_chnl, insp.is_selection],
[COPY, proxy.copy, sel_chnl, insp.is_selection],
[PASTE, proxy.paste, [connect, NO_DOCS, CLIPBOARD], insp.is_clipboard],
[PASTE2, proxy.paste, [connect, NO_DOCS, CLIPBOARD], insp.is_clipboard],
[PASTE3, proxy.paste, [connect, NO_DOCS, CLIPBOARD], insp.is_clipboard],
[DELETE, proxy.delete, sel_chnl, insp.is_selection],
[DELETE2, proxy.delete, sel_chnl, insp.is_selection],
[SELECT_ALL, proxy.select_all, doc_chnl, insp.is_doc],
[DESELECT, proxy.deselect, sel_chnl, insp.is_selection],
[ZOOM_IN, proxy.zoom_in, doc_chnl, insp.is_doc],
[ZOOM_OUT, proxy.zoom_out, doc_chnl, insp.is_doc],
[ZOOM_PAGE, proxy.fit_zoom_to_page, doc_chnl, insp.is_doc],
[ZOOM_100, proxy.zoom_100, doc_chnl, insp.is_doc],
[ZOOM_SELECTED, proxy.zoom_selected, sel_chnl, insp.is_selection],
[ZOOM_PREVIOUS, proxy.zoom_previous, doc_chnl, insp.is_doc],
[FORCE_REDRAW, proxy.force_redraw, doc_chnl, insp.is_doc],
[PAGE_FRAME, proxy.create_page_border, doc_chnl, insp.is_doc],
[PAGE_GUIDE_FRAME, proxy.create_guide_border, doc_chnl, insp.is_doc],
[REMOVE_ALL_GUIDES, proxy.remove_all_guides, doc_chnl, insp.is_doc],
[GUIDES_AT_CENTER, proxy.create_guides_at_center, doc_chnl, insp.is_doc],
[INSERT_PG, proxy.insert_page, doc_chnl, insp.is_doc],
[DELETE_PG, proxy.delete_page, docm_chnl, insp.can_delete_page],
[GOTO_PG, proxy.goto_page, docm_chnl, insp.can_goto_page],
[NEXT_PG, proxy.next_page, page_chnl, insp.can_be_next_page],
[NEXT_PG_KP, proxy.next_page, page_chnl, insp.can_be_next_page],
[PREV_PG, proxy.previous_page, page_chnl, insp.can_be_previous_page],
[PREV_PG_KP, proxy.previous_page, page_chnl, insp.can_be_previous_page],
[COMBINE, proxy.combine_selected, sel_chnl, insp.can_be_combined],
[BREAK_APART, proxy.break_apart_selected, sel_chnl, insp.can_be_breaked],
[GROUP, proxy.group, sel_chnl, insp.can_be_grouped],
[UNGROUP, proxy.ungroup, sel_chnl, insp.can_be_ungrouped],
[UNGROUP_ALL, proxy.ungroup_all, sel_chnl, insp.can_be_ungrouped_all],
[CONVERT_TO_CURVES, proxy.convert_to_curve, sel_chnl, insp.can_be_curve],
[EDIT_TEXT, proxy.edit_text, sel_chnl, insp.is_text_selected],
[SET_CONTAINER, proxy.set_container, sel_chnl, insp.is_selection],
[UNPACK_CONTAINER, proxy.unpack_container, sel_chnl, insp.is_container_selected],
[PAGES, proxy.load_pages_plg, doc_chnl, insp.is_doc],
[LAYERS, proxy.load_layers_plg, doc_chnl, insp.is_doc],
[DOM_VIEWER, proxy.load_dom_plg, doc_chnl, insp.is_doc],
[PROPERTIES, proxy.properties, doc_chnl, insp.is_doc],
[PREFERENCES, proxy.preferences, None, None],
[REPORT_BUG, proxy.report_bug, None, None],
[PROJECT_WEBSITE, proxy.project_website, None, None],
[PROJECT_FORUM, proxy.project_forum, None, None],
[ABOUT, proxy.about, None, None],
[ROTATE_LEFT, proxy.rotate_left, sel_chnl, insp.is_selection],
[ROTATE_RIGHT, proxy.rotate_right, sel_chnl, insp.is_selection],
[VERT_MIRROR, proxy.vertical_mirror, sel_chnl, insp.is_selection],
[HOR_MIRROR, proxy.horizontal_mirror, sel_chnl, insp.is_selection],
[STROKE_VIEW, proxy.stroke_view, doc_chnl, insp.is_doc, insp.is_stroke_view],
[DRAFT_VIEW, proxy.draft_view, doc_chnl, insp.is_doc, insp.is_draft_view],
[SHOW_GRID, proxy.show_grid, doc_chnl, insp.is_doc, insp.is_grid_visible],
[SHOW_GUIDES, proxy.show_guides, doc_chnl, insp.is_doc, insp.is_guides_visible],
[SHOW_SNAP, proxy.show_snapping, doc_chnl, insp.is_doc, insp.is_show_snapping],
[SHOW_PAGE, proxy.draw_page_border, doc_chnl, insp.is_doc, insp.is_draw_page_border],
[SNAP_TO_GRID, proxy.snap_to_grid, doc_chnl, insp.is_doc, insp.is_snap_to_grid],
[SNAP_TO_GUIDES, proxy.snap_to_guides, doc_chnl, insp.is_doc, insp.is_snap_to_guides],
[SNAP_TO_OBJECTS, proxy.snap_to_objects, doc_chnl, insp.is_doc, insp.is_snap_to_objects],
[SNAP_TO_PAGE, proxy.snap_to_page, doc_chnl, insp.is_doc, insp.is_snap_to_page],

	]

	for entry in entries:
		actions.append([entry[0],
				get_action_text(entry[0]),
				get_action_tooltip_text(entry[0]),
				get_action_icon(entry[0]),
				get_action_accelkey(entry[0])] + entry[1:])


	return actions
