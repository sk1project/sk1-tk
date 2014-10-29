# -*- coding: utf-8 -*-

# Copyright (C) 2009 by Barabash Maxim
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

###Sketch Config
#type = Export
#tk_file_type = ("Portable Network Graphics files", '.png')
#extensions = '.png'
format_name = 'PNG'
#unload = 1
###End

__version__ = '0.1'

import cairo
from app.Graphics.renderer import ObjRenderer


class PNGSaver(ObjRenderer):

	def __init__(self, fileptr, pathname, options=None):
		self.file = fileptr
		self.pathname = pathname

	def close(self):
		self.file.close()

	def SaveDocument(self, doc):
		self.doc = doc
		w, h = self.doc.PageSize()
		self.trafo = (1.0, 0, 0, -1.0, 0, h)
		self.canvas_matrix = cairo.Matrix(*self.trafo)
		self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(w), int(h))
		self.ctx = cairo.Context(self.surface)
		self.ctx.set_matrix(self.canvas_matrix)

		layers = []
		for layer in doc.Layers():
			if not layer.is_SpecialLayer and layer.visible:
				layers.append(layer)
		self.draw_layers(layers)

		self.surface.write_to_png(self.file)

def save(document, fileptr, filename, options={}):
	saver = PNGSaver(fileptr, filename, options)
	saver.SaveDocument(document)
	saver.close()
