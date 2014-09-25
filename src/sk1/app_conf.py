# -*- coding: utf-8 -*-
#
#	Copyright (C) 2011-2014 by Igor E. Novikov
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

from uc2.uc_conf import UCConfig, UCData
from uc2 import uc2const
from uc2.utils import system
from uc2.utils.fs import expanduser_unicode
from uc2.formats.pdxf.const import DOC_STRUCTURE

from sk1 import events, const

class AppData(UCData):

	app_name = 'sK1'
	app_proc = 'sk1'
	app_org = 'sK1 Project'
	app_domain = 'sk1project.org'
	app_icon = None
	doc_icon = None
	version = "1.0"
	app_config_dir = expanduser_unicode(os.path.join('~', '.config', 'sk1-tk'))

	def __init__(self):

		UCData.__init__(self)

		#Check clipboard directory
		self.app_clipboard_dir = os.path.join(self.app_config_dir, 'clipboard')
		if not os.path.lexists(self.app_clipboard_dir):
			os.makedirs(self.app_clipboard_dir)
		for item in DOC_STRUCTURE:
			path = os.path.join(self.app_clipboard_dir, item)
			if not os.path.lexists(path):
				os.makedirs(path)



class AppConfig(UCConfig):

	def __init__(self, path):
		UCConfig.__init__(self)

	def __setattr__(self, attr, value):
		if attr == 'filename': return
		if not hasattr(self, attr) or getattr(self, attr) != value:
			self.__dict__[attr] = value
			events.emit(events.CONFIG_MODIFIED, attr, value)

	def get_defaults(self):
		defaults = AppConfig.__dict__
		defaults.update(UCConfig.get_defaults(self))
		return defaults

	#============== GENERIC SECTION ===================
	new_doc_on_start = False
	show_cairo_splash = True

	mw_disable_global_menu = True
	mw_store_size = True
	mw_maximized = False
	mw_keep_maximized = False
	mw_size = (1000, 700)
	mw_min_size = (1000, 700)

	mw_width = 1000
	mw_height = 700
	mw_min_width = 1000
	mw_min_height = 700

	#============== RULER OPTIONS ================
	ruler_size = 20
	ruler_bgcolor = (1.0, 1.0, 1.0)
	ruler_fgcolor = (0.0, 0.0, 0.0)
	ruler_font_size = 5
	ruler_text_tick = 10
	ruler_small_tick = 5
	ruler_text_shift = 0

	#============== PALETTE OPTIONS ================
	palette_visible = True
	palette_orientation = const.HORIZONTAL
	palette_in_use = ''
	hpalette_cell_vertical = 18
	hpalette_cell_horizontal = 40
	vpalette_cell_vertical = 18
	vpalette_cell_horizontal = 18

	palette_hcell_vertical = 18
	palette_hcell_horizontal = 40
	palette_vcell_vertical = 18
	palette_vcell_horizontal = 18

	#============== CANVAS SECTION ===================
	default_unit = uc2const.UNIT_MM

	obj_jump = 1.0 * uc2const.mm_to_pt

	sel_frame_visible = 1
	sel_frame_offset = 10.0
	sel_frame_color = (0.0, 0.0, 0.0)
	sel_frame_dash = [5, 5]

	sel_bbox_visible = 0
	sel_bbox_color = (0.0, 0.0, 0.0)
	sel_bbox_bgcolor = (1.0, 1.0, 1.0)
	sel_bbox_dash = [5, 5]

	sel_marker_size = 9.0
	sel_marker_frame_color = (0.62745, 0.62745, 0.64314)
	sel_marker_frame_bgcolor = (1.0, 1.0, 1.0)
	sel_marker_frame_dash = [5, 5]
	sel_marker_fill = (1.0, 1.0, 1.0)
	sel_marker_stroke = (0.0, 0.3, 1.0)
	sel_object_marker_color = (0.0, 0.0, 0.0)

	rotation_step = 5.0#in degrees
	stroke_sensitive_size = 5.0#in pixels

	#============== SNAPPING OPTIONS ================

	snap_distance = 10.0#in pixels
	snap_order = [const.SNAP_TO_GUIDES,
				const.SNAP_TO_GRID,
				const.SNAP_TO_OBJECTS,
				const.SNAP_TO_PAGE]
	snap_to_grid = False
	snap_to_guides = True
	snap_to_objects = False
	snap_to_page = False

	show_snap = True
	snap_line_dash = [5, 5]
	snap_line_color = (1.0, 0.0, 0.0, 1.0)

	guide_line_dash = [5, 5]
	guide_line_dragging_color = (0.0, 0.0, 0.0, 0.25)

	#============== BEZIER CURVE OPTIONS ================
	curve_autoclose_flag = 0

	curve_stroke_color = (0.0, 0.0, 0.0)
	curve_stroke_width = 0.7
	curve_trace_color = (1.0, 0.0, 0.0)
	curve_point_sensitivity_size = 9.0

	curve_start_point_size = 5.0
	curve_start_point_fill = (1.0, 1.0, 1.0)
	curve_start_point_stroke = (0.0, 0.0, 0.0)
	curve_start_point_stroke_width = 2.0

	curve_point_size = 5.0
	curve_point_fill = (1.0, 1.0, 1.0)
	curve_point_stroke = (0.0, 0.3, 1.0)
	curve_point_stroke_width = 1.0

	curve_last_point_size = 5.0
	curve_last_point_fill = (1.0, 1.0, 1.0)
	curve_last_point_stroke = (0.0, 0.3, 1.0)
	curve_last_point_stroke_width = 2.0

	control_point_size = 5.0
	control_point_fill = (1.0, 1.0, 1.0)
	control_point_stroke = (0.0, 0.0, 0.0)
	control_point_stroke_width = 1.0

	control_line_stroke_color = (0.0, 0.5, 0.0)
	control_line_stroke_width = 0.7
	control_line_stroke_dash = [5, 5]

	#============== I/O SECTION ===================
	open_dir = '~'
	save_dir = '~'
	import_dir = '~'
	export_dir = '~'
	make_backup = 1
	resource_dir = ''
	profile_import_dir = '~'

	#============== COLOR MANAGEMENT SECTION ===================
	default_rgb_profile = ''
	default_cmyk_profile = ''
	default_lab_profile = ''
	default_gray_profile = ''




class LinuxConfig(AppConfig):
	os = system.LINUX

class MacosxConfig(AppConfig):
	os = system.MACOSX
	mw_maximized = 0
	set_doc_icon = 0
	ruler_style = 0

class WinConfig(AppConfig):
	os = system.WINDOWS
	ruler_style = 0



def get_app_config(path):
	os_family = system.get_os_family()
	if os_family == system.MACOSX:
		return MacosxConfig(path)
	elif os_family == system.WINDOWS:
		return WinConfig(path)
	else:
		return LinuxConfig(path)
