# -*- coding: utf-8 -*-

# Copyright (C) 2014 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

import cairo
import pangocairo

SURFACE = cairo.ImageSurface(cairo.FORMAT_RGB24, 1, 1)
CTX = cairo.Context(SURFACE)

PANGO_MATRIX = cairo.Matrix(1.0, 0.0, 0.0, -1.0, 0.0, 0.0)
PCCTX = pangocairo.CairoContext(CTX)
PANGO_LAYOUT = PCCTX.create_layout()

FAMILIES_LIST = []
FAMILIES_DICT = {}

def get_fonts(families_list, families_dict):
	fm = pangocairo.cairo_font_map_get_default()
	context = fm.create_context()
	families = context.list_families()
	for item in families:
		fcs = []
		scalable = True
		for face in item.list_faces():
			if not face.list_sizes() is None:
				scalable = False
			fcs.append(face.get_face_name())
		if scalable:
			fcs.sort()
			families_dict[item.get_name()] = fcs
			families_list.append(item.get_name())
	families_list.sort()

get_fonts(FAMILIES_LIST, FAMILIES_DICT)