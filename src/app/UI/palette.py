# -*- coding: utf-8 -*-

# Copyright (C) 2003-2006 by Igor E. Novikov
# Copyright (C) 1997, 1998, 2001 by Bernhard Herzog
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

import operator, os, app
from types import StringType, TupleType, IntType
from string import strip, split, atof, atoi

from app.X11 import X
from app.Graphics.color import RGB_Color, CMYK_Color

from app.conf.const import CHANGED, COLOR1, COLOR2, CHANGED, VIEW, \
		DROP_COLOR, CurDragColor
from app.events.warn import warn, INTERNAL, USER, pdebug, warn_tb
from app import Publisher, config, SketchError, _
from app import CreateRGBColor, StandardColors, GraphicsDevice, Identity, Point

from tkext import PyWidget

from xml.sax import handler
import xml.sax
from xml.sax.xmlreader import InputSource

class NameInUse(SketchError):
	pass

class RGBAlreadyStored(SketchError):
	pass

class RGBPalette(Publisher):

	ignore_issue = 1

	def __init__(self):
		self.entries = []
		self.name_to_entry = {}
		self.rgb_to_entry = {}

	def Subscribe(self, channel, func, *args):
		apply(Publisher.Subscribe, (self, channel, func) + args)
		self.ignore_issue = 0

	def update_dicts(self):
		self.name_to_entry = {}
		self.rgb_to_entry = {}
		for entry in self.entries:
			rgb, name = entry
			self.name_to_entry[name] = entry
			self.rgb_to_entry[rgb] = entry

	def AddEntry(self, rgb, name = None, rename = 0):
		if name:
			if self.name_to_entry.has_key(name):
				if self.name_to_entry[name] != (rgb, name):
					raise NameInUse
		if self.rgb_to_entry.has_key(rgb):
			if self.rgb_to_entry[rgb] != (rgb, name) and not rename:
				raise RGBAlreadyStored
		if not name:
			i = 0
			base = 'Color '
			name = base + `i`
			known = self.name_to_entry.has_key
			while known(name):
				i = i + 1
				name = base + `i`
		entry = (rgb, name)
		self.entries.append(entry)
		self.name_to_entry[name] = entry
		self.rgb_to_entry[rgb] = entry
		self.issue(CHANGED)

	def __getitem__(self, idx):
		if type(idx) == StringType:
			return self.name_to_entry[idx]
		if type(idx) == TupleType:
			return self.rgb_to_entry[idx]
		if type(idx) == IntType:
			return self.entries[idx]


	def GetRGB(self, idx):
		return self[idx][0]

	def Colors(self):
		return map(operator.getitem, self.entries, [0] * len(self.entries))

	def WriteFile(self, file):
		for entry in self.entries:
			(r, g, b), name = entry
			file.write('%g %g %g\t%s\n' % (r, g, b, name))

	def __len__(self):
		return len(self.entries)



#
#	Get the standard palette. User settable.
#

def read_standard_palette(filename):
	filename = os.path.join(config.std_res_dir, filename)
	return read_palette_file(filename)

#minimalistic fallback:
_mini_pal = [(0, 0, 0, 'Black'),
				(1, 1, 1, 'White')]

def GetStandardPalette():
	palette = LoadPalette(None)
	#if not palette:
		#warn(USER,
			#_("Could not load palette mini.spl; reverting to black&white"))
		#palette = RGBPalette()
		#for r, g, b, name in _mini_pal:
			#palette.AddEntry((r, g, b), name)
	return palette


def LoadPalette(filename):
	try:
		return UniversalPalette(filename)
	except:
		return None

file_types = ((_("Sketch Palette"), '.spl'),
				(_("All Files"),	 '*'))


magic_rgb_palette = '##Sketch RGBPalette 0'
magic_gimp_palette = 'GIMP Palette'

def read_palette_file(filename):
	"""Read the palette file filename"""
	file = open(filename)
	line = file.readline()
	line = strip(line)
	palette = None
	try:
		if line == magic_rgb_palette:
			palette = ReadRGBPaletteFile(filename)
		elif line == magic_gimp_palette:
			palette = Read_X_RGB_TXT(filename)
	except:
		warn_tb(USER)
	return palette


def ReadRGBPaletteFile(filename):
	file = open(filename)

	line = file.readline()
	if line != magic_rgb_palette + '\n':
		file.close()
		raise ValueError, 'Invalid file type'

	palette = RGBPalette()

	linenr = 1
	for line in file.readlines():
		line = strip(line)
		linenr = linenr + 1
		if not line or line[0] == '#':
			continue

		line = split(line, None, 3)
				
		if len(line) != 4:
			warn(INTERNAL, '%s:%d: wrong number of fields', filename, linenr)
			continue
		try:
			rgb = tuple(map(atof, line[:3]))
		except:
			warn(INTERNAL, '%s:%d: cannot parse rgb values', filename, linenr)
			continue

		for value in rgb:
			if value < 0 or value > 1.0:
				warn(INTERNAL, '%s:%d: value out of range', filename, linenr)
				continue

		name = strip(line[-1])

		try:
			palette.AddEntry(rgb, name)
		except NameInUse:
			warn(INTERNAL, '%s:%d: color name already used', filename, linenr)
			continue
		except RGBAlreadyStored:
			warn(INTERNAL, '%s:%d: color already stored', filename, linenr)
			continue

	file.close()

	return palette



def Read_X_RGB_TXT(filename):
	file = open(filename)

	palette = RGBPalette()

	linenr = 0
	color_num = 0
	for line in file.readlines():
		line = strip(line)
		linenr = linenr + 1
		if not line or line[0] in ('#', '!'):
			# an empty line or an X-style comment (!) or a GIMP comment (#)
			# GIMP's palette files have practically the same format as rgb.txt
			continue

		line = split(line, None, 3)
		if len(line) == 3:
			# the name is missing
			while 1:
				name = 'color ' + str(color_num)
				try:
					palette[name]
					used = 1
				except KeyError:
					used = 0
				if not used:
					line.append(name)
					break
				color_num = color_num + 1
		if len(line) != 4:
			warn(INTERNAL, '%s:%d: wrong number of fields', filename, linenr)
			continue
		try:
			values = map(atoi, line[:3])
		except:
			warn(INTERNAL, '%s:%d: cannot parse rgb values', filename, linenr)
			continue

		rgb = []
		for value in values:
			value = round(value / 255.0, 3)
			if value < 0:
				value = 0.0
			elif value > 1.0:
				value = 1.0
			rgb.append(value)
		rgb = tuple(rgb)

		name = strip(line[-1])

		try:
			palette.AddEntry(rgb, name)
		except NameInUse:
			warn(INTERNAL, '%s:%d: color name already used', filename, linenr)
			continue
		except RGBAlreadyStored:
			warn(INTERNAL, '%s:%d: color already stored', filename, linenr)
			continue

	file.close()

	return palette

class UniversalPalette:
	
	def __init__(self, file=None):
		self.name=''
		self.type=''
		self.colors=[]
		if file and os.path.isfile(file):
			self.file=file
		else:
			self.file=os.path.join(config.user_palettes, config.preferences.unipalette)
		self.loadPalette(self.file)
		
	def loadPalette(self, file=None):
		self.load(file)
		
	def load(self, filename=None):
		content_handler = XMLPaletteReader(palette=self)
		error_handler = ErrorHandler()
		entity_resolver = EntityResolver()
		dtd_handler = DTDHandler()
		try:
			input = open(filename, "r")
			input_source = InputSource()
			input_source.setByteStream(input)
			xml_reader = xml.sax.make_parser()
			xml_reader.setContentHandler(content_handler)
			xml_reader.setErrorHandler(error_handler)
			xml_reader.setEntityResolver(entity_resolver)
			xml_reader.setDTDHandler(dtd_handler)
			xml_reader.parse(input_source)
			input.close
		except:
			pass
	
class XMLPaletteReader(handler.ContentHandler):
	def __init__(self, palette=None):
		self.key = None
		self.value = None
		self.palette = palette
		self.attrs=None
		self.type=None

	def startElement(self, name, attrs):
		self.key = name
		self.attrs=attrs

	def endElement(self, name):		
		if name=='color':
			if self.type=='RGB':
				r=atof(self.attrs._attrs['r'])
				g=atof(self.attrs._attrs['g'])
				b=atof(self.attrs._attrs['b'])				
				color_name=self.attrs._attrs['name']
				self.palette.colors.append(RGB_Color(r,g,b, name=color_name))
				#c,m,y,k=app.colormanager.convertRGB(r,g,b)
				#print '<color c="%f"'%c,'m="%f"'%m,'y="%f"'%y,'k="%f"'%k,'name="%s"'%color_name,'/>'
			if self.type=='CMYK':
				c=atof(self.attrs._attrs['c'])
				m=atof(self.attrs._attrs['m'])
				y=atof(self.attrs._attrs['y'])
				k=atof(self.attrs._attrs['k'])
				color_name=self.attrs._attrs['name']
				self.palette.colors.append(CMYK_Color(c,m,y,k, name=color_name))
		if name=='description':			
			self.type=self.attrs._attrs['type']
			self.palette.name=self.attrs._attrs['name']
			self.palette.type=self.attrs._attrs['type']

	def characters(self, data):
		self.value = data

class ErrorHandler(handler.ErrorHandler): pass
class EntityResolver(handler.EntityResolver): pass
class DTDHandler(handler.DTDHandler): pass	

class PaletteWidget(PyWidget, Publisher):

	def __init__(self, master=None, palette = None, cell_size = 20, **kw):
		if not kw.has_key('width'):
			kw['width'] = cell_size
		apply(PyWidget.__init__, (self, master), kw)

		self.cell_size = cell_size
		self.num_cells = 0
		self.gc_initialized = 0
		self.gc = GraphicsDevice()
		self.gc.SetViewportTransform(1.0, Identity, Identity)
		self.start_idx = 0
		self.unipalette= UniversalPalette()
		self.SetPalette(self.unipalette)
		self.dragging = 0
		self.bind('<ButtonPress-1>', self.release_1)
		self.bind('<ButtonPress-3>', self.apply_color_2)

	def DestroyMethod(self):
		Publisher.Destroy(self)

	def compute_num_cells(self):
		self.num_cells = self.tkwin.height / self.cell_size+1

	def MapMethod(self):
		self.compute_num_cells()
		self.issue(VIEW)
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
			if self.dragging:
				self.drop_color(event)
			else:
				self.apply_color_1(event)
		finally:
			self.dragging = 0

	def drop_color(self, event):
		self['cursor'] = self.drag_old_cursor
		w = self.winfo_containing(event.x_root, event.y_root)
		while w and w != self:
			if __debug__:
				pdebug('DND', 'trying to drop on', w)
			try:
				accepts = w.accept_drop
			except AttributeError:
				accepts = ()
			if DROP_COLOR in accepts:
				x = event.x_root - w.winfo_rootx()
				y = event.y_root - w.winfo_rooty()
				w.DropAt(x, y, DROP_COLOR, self.drag_start)
				break
			if w != w.winfo_toplevel():
				parent = self.tk.call('winfo', 'parent', w._w)
				w = self.nametowidget(parent)
			else:
				break


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

	def move_1(self, event):
		if event.state & X.Button1Mask:
			if not self.dragging:
				self.dragging = 1
				self.drag_old_cursor = self['cursor']
				self['cursor'] = CurDragColor
			w = self.winfo_containing(event.x_root, event.y_root)

	def Palette(self):
		return self.unipalette

	def SetPalette(self, palette):
		self.unipalette = palette
		self.palette_changed()

	def palette_changed(self):
		self.compute_num_cells()
		self.normalize_start()
		self.issue(VIEW)
		self.UpdateWhenIdle()

	def RedrawMethod(self, region = None):
		win = self.tkwin
		width = win.width
		height =win.height
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
		for rgb in rgbs:
			SetFillColor(apply(create_color, (1.0, 1.0, 1.0)))
			FillRectangle(0, x,  width, x + width)
			SetFillColor(apply(create_color, (0.5, 0.5, 0.5)))
			FillRectangle(1, x,  width, x + width-1)
			SetFillColor(rgb.RGB())
			FillRectangle(2, x+1,  width-1, x + width-2)
			if rgb.name=='Registration Color':
				cw=5
				lx=0+cw+1
				ly=x+cw+2
				rx=width-cw-1
				ry=x+width-cw-2
				SetFillColor(apply(create_color, (1.0, 1.0, 1.0)))
				DrawRectangle(Point(lx, ly-2), Point(rx, ry))	
				DrawLine(Point(lx+4, ly-4), Point(lx+4, ry+2))	
				DrawLine(Point(lx-2, ly+2), Point(rx+2, ly+2))
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
			self.issue(VIEW)

	def ScrollXUnits(self, count):
		start = self.start_idx
		self.start_idx = self.start_idx + count
		self.normalize_start()
		if start != self.start_idx:
			self.UpdateWhenIdle()
			self.issue(VIEW)

