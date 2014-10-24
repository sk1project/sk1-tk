# -*- coding: utf-8 -*-

# Copyright (C) 2014 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

import cairo
import pangocairo
import pango
from uc import libcairo

SURFACE = cairo.ImageSurface(cairo.FORMAT_RGB24, 1000, 1000)
CTX = cairo.Context(SURFACE)

DIRECT_MATRIX = cairo.Matrix()

PANGO_MATRIX = cairo.Matrix(1.0, 0.0, 0.0, -1.0, 0.0, 0.0)
CTX_MATRIX = cairo.Matrix(1.0, 0.0, 0.0, 1.0, 0.0, 0.0)
CTX.set_matrix(CTX_MATRIX)

PCCTX = pangocairo.CairoContext(CTX)
PANGO_LAYOUT = PCCTX.create_layout()

FAMILIES_LIST = []
FAMILIES_DICT = {}

ALIGN_TYPE = {
		0:pango.ALIGN_LEFT,
		1:pango.ALIGN_CENTER,
		2:pango.ALIGN_RIGHT
		}

def _get_fonts(families_list, families_dict):
	fm = pangocairo.cairo_font_map_get_default()
	context = fm.create_context()
	families = context.list_families()
	for item in families:
		fcs = {}
		scalable = True
		for face in item.list_faces():
			if not face.list_sizes() is None:
				scalable = False
			fcs[face.get_face_name()] = face
		if scalable:
			families_dict[item.get_name()] = fcs
			families_list.append(item.get_name())
	families_list.sort()

_get_fonts(FAMILIES_LIST, FAMILIES_DICT)

class PangoFontFace:

	familyname = None
	facename = None
	fontface = None
	fontdesc = None
	SURFACE = None
	CTX = None
	PCCTX = None
	PANGO_LAYOUT = None

	def __init__(self, familyname, facename='Regular'):
		if not familyname in FAMILIES_LIST:familyname = FAMILIES_LIST[0]
		self.familyname = familyname
		faces = FAMILIES_DICT[self.familyname]
		if not facename in faces.keys():facename = faces.keys()[0]
		self.facename = facename
		self.fontface = faces[self.facename]
		self.fontdesc = self.fontface.describe()

	def to_string(self): return self.fontdesc.to_string()

	def PostScriptName(self): return self.familyname

	def set_layout(self, text, properties):
		CTX.new_path()
		PANGO_LAYOUT.set_width(-1)
		self.fontdesc.set_size(int(properties.font_size * 1024))
		PANGO_LAYOUT.set_font_description(self.fontdesc)
		PANGO_LAYOUT.set_alignment(ALIGN_TYPE[properties.align])
		PANGO_LAYOUT.set_justify(False)
		PANGO_LAYOUT.set_text(text)

	def get_cpaths(self, text, properties):
		self.set_layout(text, properties)
		PCCTX.layout_path(PANGO_LAYOUT)
		cairo_path = CTX.copy_path()
		libcairo.apply_cmatrix(cairo_path, PANGO_MATRIX)
		return cairo_path

	def typeset_text(self, text, properties):
		self.set_layout('' + text, properties)
		typeset = []
		index = 0
		for char in text:
			utf_index = len(text[:index].encode('utf-8'))
			x, y, width, height = PANGO_LAYOUT.index_to_pos(utf_index)
			x = x / 1024.0
			y = y / 1024.0
			height = height / 1024.0
			typeset.append((x, -y - height))
			index += 1
		return typeset

	def text_caret_data(self, text, properties, caret):
		self.set_layout(text, properties)
		utf_caret = len(text[:caret].encode('utf-8'))
		x, y, width, height = PANGO_LAYOUT.index_to_pos(utf_caret)
		x = x / 1024.0
		y = y / 1024.0
		height = height / 1024.0
		return ((x, -y), (0, -height))

	def text_bbox(self, text, properties):
		cpath = self.get_cpaths(text, properties)
		return tuple(libcairo.get_cpath_bbox(cpath))

	def text_coordbox(self, text, properties):
		return self.text_bbox(text, properties)

	def get_paths(self, text, properties):
		cpath = self.get_cpaths(text, properties)
		paths = libcairo.get_path_from_cpath(cpath)
		return paths


def get_fontface(familyname, facename='Regular'):
	return PangoFontFace(familyname, facename)


