# -*- coding: utf-8 -*-

# Copyright (C) 2003-2008 by Igor E. Novikov
# Copyright (C) 1997, 1998, 1999, 2001, 2003 by Bernhard Herzog
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from math import floor, ceil, hypot
from string import atoi
from types import TupleType
import operator, app

from Tkinter import Canvas, Label

from app import config, GuideLine, Point
from app.conf import const
from app.conf.const import CHANGED
from app.Lib import units

from tkgraphics import NumWriter

HORIZONTAL = 0
VERTICAL = 1

tick_lengths = (8, 5, 3, 3)

# (base_unit_factor, (subdiv1, subdiv2,...))
tick_config = {'in': (1.0, (2, 2, 2, 2)),
				'cm': (1.0, (2, 5)),
				'mm': (10.0, (2, 5)),
				'pt': (100.0, (2, 5, 2, 5)),
				'px': (100.0, (2, 5, 2, 5)),
				#'pt': (72.0, (2, 3, 12)),
				}

class Ruler(Canvas):

	writer = None

	def __init__(self, master=None, orient=HORIZONTAL, canvas=None, **kw):
		self.writer = NumWriter(self)
		self.mw = None
		self.document = None

		apply(Canvas.__init__, (self, master), kw)
		self.root = master
		self.orient = orient
		self.canvas = canvas
		self.positions = None
		self.SetRange(0.0, 1.0, force=1)

		self.text_type = 'horizontal'
		self.border_width = 0
		self.relief = 'FLAT'
		height = 20

		if orient == HORIZONTAL:
			self['height'] = height
		else:
			self['width'] = height

		self.bind('<ButtonPress>', self.ButtonPressEvent)
		self.bind('<Double-Button-1>', self.draw_test)
		self.bind('<ButtonRelease>', self.ButtonReleaseEvent)
		self.bind('<Motion>', self.PointerMotionEvent)
		self.bind('<Map>', self.RedrawMethod)
		self.bind('<Configure>', self.RedrawMethod)
		self.button_down = 0
		self.forward_motion = 0

		config.preferences.Subscribe(CHANGED, self.preference_changed)


	def destroy(self):
			Canvas.destroy(self)
			self.canvas = None

	def ResizedMethod(self, width, height):
			self.SetRange(self.start, self.pixel_per_pt, force=1)

	def SetRange(self, start, pixel_per_pt, force=0):
			if not force and start == self.start and pixel_per_pt == self.pixel_per_pt:
				return
			self.start = start
			self.pixel_per_pt = pixel_per_pt
			self.positions = None
			self.RedrawMethod()

	def preference_changed(self, pref, value):
		if pref == 'default_unit' or pref == 'coord_system':
			self.positions = None
			self.RedrawMethod()

	def get_positions(self):
##    Fixed to avoid blank rules on start
##         if self.positions is not None:
##            return self.positions, self.texts
			self.mw = app.mw
			if self.mw:
				self.document = self.mw.document
				page_width, page_height = self.document.PageSize()
			else:
				page_width, page_height = (0, 0)

			min_text_step = config.preferences.ruler_min_text_step
			max_text_step = config.preferences.ruler_max_text_step
			min_tick_step = config.preferences.ruler_min_tick_step
			if self.orient == HORIZONTAL:
				length = int(self.winfo_width())
				origin = self.start
				if config.preferences.coord_system == 2:
					origin -= page_width / 2
			else:
				length = int(self.winfo_height())
				origin = self.start - length / self.pixel_per_pt
				if config.preferences.coord_system == 1:
					origin -= page_height
				if config.preferences.coord_system == 2:
					origin -= page_height / 2

			unit_name = config.preferences.default_unit
			pt_per_unit = units.unit_dict[unit_name]
			units_per_pixel = 1.0 / (pt_per_unit * self.pixel_per_pt)
			factor, subdivisions = tick_config[unit_name]
			subdivisions = (1,) + subdivisions

			factor = factor * pt_per_unit
			start_pos = floor(origin / factor) * factor
			main_tick_step = factor * self.pixel_per_pt
			num_ticks = floor(length / main_tick_step) + 2

			if main_tick_step < min_tick_step:
				tick_step = ceil(min_tick_step / main_tick_step) * main_tick_step
				subdivisions = (1,)
				ticks = 1
			else:
				tick_step = main_tick_step
				ticks = 1
				for depth in range(len(subdivisions)):
					tick_step = tick_step / subdivisions[depth]
					if tick_step < min_tick_step:
						tick_step = tick_step * subdivisions[depth]
						depth = depth - 1
						break
					ticks = ticks * subdivisions[depth]
				subdivisions = subdivisions[:depth + 1]

			positions = range(int(num_ticks * ticks))
			positions = map(operator.mul, [tick_step] * len(positions), positions)
			positions = map(operator.add, positions,
						[(start_pos - origin) * self.pixel_per_pt]
						* len(positions))

			stride = ticks
			marks = [None] * len(positions)
			for depth in range(len(subdivisions)):
				stride = stride / subdivisions[depth]
				if depth >= len(tick_lengths):
					height = tick_lengths[-1]
				else:
					height = tick_lengths[depth]
				for i in range(0, len(positions), stride):
					if marks[i] is None:
						marks[i] = (height, int(round(positions[i])))

			texts = []
			if main_tick_step < min_text_step:
				stride = int(ceil(min_text_step / main_tick_step))
				start_index = stride - (floor(origin / factor) % stride)
				start_index = int(start_index * ticks)
				stride = stride * ticks
			else:
				start_index = 0
				stride = ticks
				step = main_tick_step
				for div in subdivisions:
					step = step / div
					if step < min_text_step:
						break
					stride = stride / div
					if step < max_text_step:
						break

			for i in range(start_index, len(positions), stride):
				pos = positions[i] * units_per_pixel + origin / pt_per_unit
				pos = round(pos, 3)

				if config.preferences.coord_system == 1:
					if self.orient == VERTICAL:
						pos *= -1

				if pos == 0.0:# avoid '-0' strings
					pos = 0.0

				texts.append(("%g" % pos, marks[i][-1]))

			self.positions = marks
			self.texts = texts

			return self.positions, self.texts


	def RedrawMethod(self, region=None):
		tags = self.find_all()
		for tag in tags:
			self.delete(tag)
		if self.orient == HORIZONTAL:
			self.draw_ruler_horizontal()
		else:
			self.draw_ruler_vertical()

	def draw_test(self, event):
		self.draw_ruler_horizontal()

	def draw_ruler_horizontal(self):
		height = int(self.winfo_height())
		width = int(self.winfo_width())
		self.create_line(0, height - 1, width, height - 1, fill=config.preferences.ruler_tick_color)
		ticks, texts = self.get_positions()
		offset = 0
		if config.preferences.cairo_enabled:
			offset = 0

		for h, pos in ticks:
			pos = pos - offset
			self.create_line(pos, height - h, pos, height, fill=config.preferences.ruler_tick_color)
		y = int(height / 2) - 5
		for text, pos in texts:
			pos = pos - offset
			self.create_line(pos, height - 10, pos, height, fill=config.preferences.ruler_tick_color)
			self.writer.write(text, config.preferences.ruler_text_color, pos + 2, y)

	def draw_ruler_vertical(self):
		height = int(self.winfo_height())
		width = int(self.winfo_width())
		self.create_line(width - 1, 0, width - 1, height, fill=config.preferences.ruler_tick_color)
		ticks, texts = self.get_positions()

		for h, pos in ticks:
			pos = height - pos
			self.create_line(width - h, pos, width, pos, fill=config.preferences.ruler_tick_color)
		x = int(width / 2) - 5
		for text, pos in texts:
			pos = height - pos
			self.create_line(width - 10, pos, width, pos, fill=config.preferences.ruler_tick_color)
			self.writer.writeVertically(text, config.preferences.ruler_text_color, x, pos - 2)


	def ButtonPressEvent(self, event):
		if event.num == const.Button1:
			self.button_down = 1
			self.pressevent = event

	def ButtonReleaseEvent(self, event):
		if event.num == const.Button1:
			self.button_down = 0

	def PointerMotionEvent(self, event):
		if self.button_down:
			if self.canvas is not None:
				press = self.pressevent
				if hypot(press.x - event.x, press.y - event.y) > 3:
					guide = GuideLine(Point(0, 0), self.orient == HORIZONTAL)
					self.canvas.PlaceObject(guide)
					press.x = press.x_root - self.canvas.winfo_rootx()
					press.y = press.y_root - self.canvas.winfo_rooty()
					self.canvas.ButtonPressEvent(press)
					self.canvas.grab_set()
					self.button_down = 0

	def SetCanvas(self, canvas):
		self.canvas = canvas
		self.RedrawMethod()

class RulerCorner(Label):

		def __init__(self, master=None, **kw):
			apply(Label.__init__, (self, master), kw)
			self['image'] = 'rulers_corner'
			if config.preferences.coord_system == 2:
				self['image'] = 'rulers_corner2'
			if config.preferences.coord_system == 1:
				self['image'] = 'rulers_corner1'
			self.bind('<Button-1>', self.change_coord)

		def change_coord(self, *args):
			if config.preferences.coord_system == 2:
				self['image'] = 'rulers_corner'
				config.preferences.coord_system = 0
			elif config.preferences.coord_system == 1:
				self['image'] = 'rulers_corner2'
				config.preferences.coord_system = 2
			else:
				self['image'] = 'rulers_corner1'
				config.preferences.coord_system = 1



