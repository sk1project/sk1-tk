# -*- coding: utf-8 -*-

# Copyright (C) 2014 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

import cairo, cids, math
from sk1sdk import tkcairo

from app import config

CAIRO_BLACK = (0.0, 0.0, 0.0)
CAIRO_DGRAY = (0.25, 0.25, 0.25)
CAIRO_GRAY = (0.5, 0.5, 0.5)
CAIRO_LGRAY = (0.75, 0.75, 0.75)
CAIRO_WHITE = (1.0, 1.0, 1.0)

class DocRenderer:

	canvas = None
	surface = None
	ctx = None
	trafo = ()
	doc = None
	direct_matrix = cairo.Matrix(1.0, 0.0, 0.0, 1.0, 0.0, 0.0)
	canvas_matrix = None
	zoom = 1.0
	width = 0
	height = 0
	rect = None


	def __init__(self, canvas):
		self.canvas = canvas
		self.init_fields()

	def init_fields(self):
		self.ctx = None
		self.surface = None
		self.trafo = ()
		self.doc = None
		self.rect = None
		self.canvas_matrix = None
		self.zoom = 1.0

	def draw(self, doc, rect):
		self.doc = doc
		self.rect = rect
		self.width = self.canvas.winfo_width()
		self.height = self.canvas.winfo_height()
		self.trafo = self.canvas.get_matrix()
		self.zoom = abs(self.trafo[0])
		self.canvas_matrix = cairo.Matrix(*self.trafo)

		self.surface = cairo.ImageSurface(cairo.FORMAT_RGB24,
										self.width, self.height)
		self.ctx = cairo.Context(self.surface)
		self.ctx.set_source_rgb(*CAIRO_WHITE)
		self.ctx.paint()
		self.ctx.set_matrix(self.canvas_matrix)

		#---Drawing Start
		self.draw_page()

		layers = self.doc.getRegularLayers()
		for layer in layers:
			self.draw_layer(layer)

		layers = self.doc.getMasterLayers()
		for layer in layers:
			self.draw_layer(layer)

		self.draw_guidelayer(self.doc.guide_layer)
		self.draw_gridlayer(self.doc.snap_grid)
		#---Drawing End

		winctx = tkcairo.create_context(self.canvas)
		winctx.set_source_surface(self.surface)
		winctx.paint()
		self.init_fields()

	def doc_to_win(self, x, y):
		m11 = self.trafo[0]
		m22, dx, dy = self.trafo[3:]
		x_new = m11 * x + dx
		y_new = m22 * y + dy
		return (x_new, y_new)

	def draw_page(self):
		if self.canvas.show_page_outline:
			w, h = self.doc.PageSize()
			self.ctx.set_line_width(1.0 / self.zoom)
			offset = 5.0 / self.zoom
			self.ctx.rectangle(offset, -offset, w, h)
			self.ctx.set_source_rgb(*CAIRO_LGRAY)
			self.ctx.fill()
			self.ctx.set_antialias(cairo.ANTIALIAS_NONE)
			self.ctx.rectangle(0.0, 0.0, w, h)
			self.ctx.set_source_rgb(*CAIRO_WHITE)
			self.ctx.fill()
			self.ctx.rectangle(0.0, 0.0, w, h)
			self.ctx.set_source_rgb(*CAIRO_BLACK)
			self.ctx.stroke()

	def draw_layer(self, layer):pass

	def draw_guidelayer(self, guidelayer):
		if not guidelayer.visible: return
		guides = []
		for obj in guidelayer.objects:
			if obj.cid == cids.GUIDE:
				guides.append(obj)
		if guides:
			self.ctx.set_matrix(self.direct_matrix)
			self.ctx.set_antialias(cairo.ANTIALIAS_NONE)
			self.ctx.set_line_width(1.0)
			self.ctx.set_dash(config.preferences.horizontal_guide_shape)
			self.ctx.set_source_rgba(*config.preferences.guideline_color)
			for item in guides:
				if item.horizontal:
					y_win = self.doc_to_win(0, item.point.y)[1]
					self.ctx.move_to(0, y_win)
					self.ctx.line_to(self.width, y_win)
					self.ctx.stroke()
				else:
					x_win = self.doc_to_win(item.point.x, 0)[0]
					self.ctx.move_to(x_win, 0)
					self.ctx.line_to(x_win, self.height)
					self.ctx.stroke()
			self.ctx.set_matrix(self.canvas_matrix)
			self.ctx.set_antialias(cairo.ANTIALIAS_DEFAULT)

	def draw_gridlayer(self, gridlayer):
		if not gridlayer.visible: return

		self.ctx.set_matrix(self.direct_matrix)
		self.ctx.set_antialias(cairo.ANTIALIAS_NONE)
		self.ctx.set_line_width(1.0)
		self.ctx.set_dash([])
		self.ctx.set_source_rgba(*config.preferences.gridlayer_color)

		x, y, dx, dy = gridlayer.geometry

		x0, y0 = self.doc_to_win(x, y)
		dx = dx * self.zoom
		dy = dy * self.zoom

		#config.snap_distance
		sdist = 10

		i = 0.0
		while dx < sdist + 3:
			i = i + 0.5
			dx = dx * 10.0 * i
		if dx / 2.0 > sdist + 3:
			dx = dx / 2.0

		i = 0.0
		while dy < sdist + 3:
			i = i + 0.5
			dy = dy * 10.0 * i
		if dy / 2.0 > sdist + 3:
			dy = dy / 2.0

		sx = (x0 / dx - math.floor(x0 / dx)) * dx
		sy = (y0 / dy - math.floor(y0 / dy)) * dy

		i = pos = 0
		while pos < self.width:
			pos = sx + i * dx
			i += 1
			self.ctx.move_to(pos, 0)
			self.ctx.line_to(pos, self.height)
			self.ctx.stroke()
		i = pos = 0
		while pos < self.height:
			pos = sy + i * dy
			i += 1
			self.ctx.move_to(0, pos)
			self.ctx.line_to(self.width, pos)
			self.ctx.stroke()

		self.ctx.set_matrix(self.canvas_matrix)
		self.ctx.set_antialias(cairo.ANTIALIAS_DEFAULT)
