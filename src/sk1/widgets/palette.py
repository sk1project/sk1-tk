# -*- coding: utf-8 -*-

# Copyright (C) 2003-2006 by Igor E. Novikov
# Copyright (C) 1997, 1998, 2001 by Bernhard Herzog
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

import os, app

from app.Graphics.color import RGB_Color, CMYK_Color, SPOT_Color, tk_to_rgb
from app.conf.const import COLOR1, COLOR2
from app import Publisher, config, SketchIOError
from app import CreateRGBColor, StandardColors, GraphicsDevice, Identity, Point

from sk1.tkext import PyWidget


class SK1Palette:

	name = ''
	source = ''
	columns = 1
	comments = ''
	colors = []
	pal_sign = '##sK1 palette'

	def __init__(self, filepath=''):
		self.colors = []
		if filepath and os.path.isfile(filepath):
			self.load_palette(filepath)

	def load_palette(self, filepath):
		if not filepath or not os.path.isfile(filepath):
			strerror = 'Cannot read palette'
			raise SketchIOError(0, strerror, filepath)

		fileptr = open(filepath, 'rb')
		if not fileptr.readline().strip() == self.pal_sign:
			strerror = 'Unsupported palette format'
			raise SketchIOError(0, strerror, filepath)

		while True:
			line = fileptr.readline()
			if not line: break
			line = line.strip()
			if not line: continue
			if line[0] == '#': continue
			try:
				line = 'self.' + line
				code = compile(line, '<string>', 'exec')
				exec code
			except:pass
		fileptr.close()

	def palette(self, name=''):
		if name: self.name = name.decode('utf-8')

	def add_comments(self, comment_line=''):
		if comment_line:
			if self.comments: self.comments += '\n'
			self.comments += comment_line.decode('utf-8')

	def set_name(self, name): self.name = name.decode('utf-8')
	def set_source(self, source):self.source = source.decode('utf-8')
	def set_columns(self, val): self.columns = val
	def color(self, color):
		clrtype = 'RGB'
		clrvals = ()
		alpha = 1.0
		name = ''
		palname = ''
		if not color[0] == 'SPOT':
			clrtype, clrvals, alpha, name = color
		else:
			clrtype, clrvals, alpha, name, palname = color
			palname = palname.decode('utf-8')
		name = name.decode('utf-8')

		if clrtype == 'RGB':
			r, g, b = clrvals
			self.colors.append(RGB_Color(r, g, b, alpha, name))
		elif clrtype == 'CMYK':
			c, m, y, k = clrvals
			self.colors.append(CMYK_Color(c, m, y, k, alpha, name))
		elif clrtype == 'SPOT':
			r, g, b = clrvals[0]
			c, m, y, k = clrvals[1]
			clr = SPOT_Color(r, g, b, c, m, y, k, name, palname)
			self.colors.append(clr)

	def palette_end(self, *args):pass

def load_palette(filepath):
	if os.path.isfile(filepath):
		try: return SK1Palette(filepath)
		except: pass
	return None

def get_builtin_palette():
	filepath = os.path.join(config.sk_palettes,
						config.preferences.builtin_palette)
	return load_palette(filepath)

def get_default_palette():
	pal = None
	if config.preferences.palette:
		pal = load_palette(config.preferences.palette)
	if pal: return pal
	return get_builtin_palette()


##########################

class PaletteWidget(PyWidget, Publisher):

	def __init__(self, master=None, palette=None, cell_size=20, **kw):
		if not kw.has_key('width'):
			kw['width'] = cell_size
		apply(PyWidget.__init__, (self, master), kw)

		self.cell_size = cell_size
		self.num_cells = 0
		self.gc_initialized = 0
		self.gc = GraphicsDevice()
		self.gc.SetViewportTransform(1.0, Identity, Identity)
		self.start_idx = 0
		self.dragging = 0
		self.bind('<ButtonPress-1>', self.release_1)
		self.bind('<ButtonPress-3>', self.apply_color_2)

	def DestroyMethod(self):
		Publisher.Destroy(self)

	def compute_num_cells(self):
		self.num_cells = self.tkwin.height / self.cell_size + 1

	def MapMethod(self):
		self.compute_num_cells()
		if not self.gc_initialized:
			self.init_gc()
			self.gc_initialized = 1

	def init_gc(self):
		self.gc.init_gc(self.tkwin)

	def get_color(self, x, y):
		if 0 <= x < self.tkwin.width and 0 <= y < self.tkwin.height:
			i = self.start_idx + y / self.cell_size
			if i < len(self.unipalette.colors):
				return self.unipalette.colors[i]

	def release_1(self, event):
		try:
			self.apply_color_1(event)
		finally:
			self.dragging = 0

	def apply_color_1(self, event):
		c = self.get_color(event.x, event.y)
		if c:
			self.issue(COLOR1, c)

	def apply_color_2(self, event):
		c = self.get_color(event.x, event.y)
		if c:
			self.issue(COLOR2, c)

	drag_start = (0, 0, 0)
	def press_1(self, event):
		self.drag_start = self.get_color(event.x, event.y)

	def move_1(self, event):pass

	def Palette(self):
		return self.unipalette

	def SetPalette(self, palette):
		self.unipalette = palette
		self.palette_changed()

	def palette_changed(self):
		self.compute_num_cells()
		self.normalize_start()
		self.tk.call(self._w, 'update')

	def RedrawMethod(self, region=None):
		win = self.tkwin
		width = win.width
		height = win.height
		self.gc.StartDblBuffer()
		self.gc.SetFillColor(StandardColors.black)
		self.gc.FillRectangle(0, 0, height, width)

		x = 0
		FillRectangle = self.gc.FillRectangle
		DrawRectangle = self.gc.DrawRectangle
		DrawLine = self.gc.DrawLine
		SetFillColor = self.gc.SetFillColor
		create_color = CreateRGBColor
		rgbs = self.unipalette.colors
		rgbs = rgbs[self.start_idx:self.start_idx + self.num_cells]
		###widget refresh###
		r, g, b = tk_to_rgb(app.uimanager.currentColorTheme.bg)
		SetFillColor(apply(create_color, (r, g, b)))
		FillRectangle(0, 0, width, height)
		####################
		for rgb in rgbs:
			SetFillColor(apply(create_color, (1.0, 1.0, 1.0)))
			FillRectangle(0, x, width, x + width)
			SetFillColor(apply(create_color, (0.5, 0.5, 0.5)))
			FillRectangle(1, x, width, x + width - 1)
			SetFillColor(rgb.RGB())
			FillRectangle(2, x + 1, width - 1, x + width - 2)
			if rgb.name == 'Registration Color':
				cw = 5
				lx = 0 + cw + 1
				ly = x + cw + 2
				rx = width - cw - 1
				ry = x + width - cw - 2
				SetFillColor(apply(create_color, (1.0, 1.0, 1.0)))
				DrawRectangle(Point(lx, ly - 2), Point(rx, ry))
				DrawLine(Point(lx + 4, ly - 4), Point(lx + 4, ry + 2))
				DrawLine(Point(lx - 2, ly + 2), Point(rx + 2, ly + 2))
			x = x + width
		self.gc.EndDblBuffer()

	def ResizedMethod(self, width, height):
		self.compute_num_cells()
		self.gc.WindowResized(width, height)
		self.normalize_start()
		self.UpdateWhenIdle()

	def normalize_start(self):
		length = len(self.unipalette.colors)
		if self.start_idx < 0:
			self.start_idx = 0
		if length < self.num_cells:
			self.start_idx = 0
		elif length - self.start_idx < self.num_cells:
			self.start_idx = length - self.num_cells

	def CanScrollLeft(self):
		return self.start_idx > 0

	def CanScrollRight(self):
		return len(self.unipalette.colors) - self.start_idx > self.num_cells

	def ScrollXPages(self, count):
		length = self.tkwin.height / self.cell_size
		start = self.start_idx
		self.start_idx = self.start_idx + count * length
		self.normalize_start()
		if start != self.start_idx:
			self.UpdateWhenIdle()

	def ScrollXUnits(self, count):
		start = self.start_idx
		self.start_idx = self.start_idx + count
		self.normalize_start()
		if start != self.start_idx:
			self.UpdateWhenIdle()

