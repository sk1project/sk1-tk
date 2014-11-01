# -*- coding: utf-8 -*-

# Copyright (C) 2008-2009 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from sk1sdk.libttk import TFrame, TLabel, TCombobox
from Tkinter import RIGHT, BOTTOM, X, Y, BOTH, LEFT, CENTER, TOP, W, E, DISABLED, NORMAL
from Tkinter import StringVar, DoubleVar, IntVar, Canvas
from PIL import Image


from colorsys import hsv_to_rgb, rgb_to_hsv

from app.conf.const import CHANGED, ConstraintMask

from app import _sketch
from app import  _, StandardColors, Trafo, SketchError, Publisher
from app.Graphics.color import skvisual, CreateRGBColor, CreateCMYKColor, CreateRGBAColor, CreateCMYKAColor

from sk1.x11const import GXxor, ZPixmap
from sk1.tkext import PyWidget

import string


xyramp_size = (140, 140)
zramp_size = (15, 140)



class ColorChooserWidget(TFrame):

	current_chooser = None

	def __init__(self, parent, callback, color=None, **kw):
		self.color = color
		self.callback = callback
		self.parent = parent
		TFrame.__init__(self, parent, style='FlatFrame', **kw)
		self.rgb_chooser = RGBChooser(self, self.reset_color)
		self.spot_chooser = SPOTChooser(self)
		self.empty_chooser = EmptyPatternChooser(self)
		self.current_chooser = self.empty_chooser
		self.current_chooser.pack(side=TOP)


	def set_color(self, color):
		self.color = color
		if color is None:
			if not self.current_chooser.__class__ == EmptyPatternChooser:
				self.set_chooser(self.empty_chooser)
		elif color.model == 'RGB':
			if not self.current_chooser.__class__ == RGBChooser:
				self.set_chooser(self.rgb_chooser)
		elif color.model == 'CMYK':
			if not self.current_chooser.__class__ == RGBChooser:
				self.set_chooser(self.rgb_chooser)
		elif color.model == 'SPOT':
			if not self.current_chooser.__class__ == SPOTChooser:
				self.set_chooser(self.spot_chooser)
		self.current_chooser.set_color(color)

	def set_chooser(self, widget):
		self.current_chooser.forget()
		self.current_chooser = widget
		self.current_chooser.pack(side=TOP)

	def reset_color(self, color):
		r, g, b = color
		if self.color.model == 'RGB':
			self.callback(CreateRGBAColor(r, g, b, self.color.alpha))
		elif self.color.model == 'CMYK':
			rgb = CreateRGBColor(r, g, b)
			c, m, y, k = rgb.getCMYK()
			self.callback(CreateCMYKAColor(c, m, y, k, self.color.alpha))
		else:
			pass

class EmptyPatternChooser(TFrame):

	def __init__(self, parent, color=None, **kw):
		TFrame.__init__(self, parent, style='FlatFrame', **kw)
		label = TLabel(self, image='empty_pattern_chooser', justify=CENTER)
		label.pack(side=TOP, pady=3)
		label2 = TLabel(self, text=_('Empty pattern selected,\ni.e. object will not be filled'), justify=CENTER)
		label2.pack(side=TOP, pady=10)

	def set_color(self, color):
		pass

class SPOTChooser(TFrame):

	def __init__(self, parent, color=None, **kw):
		TFrame.__init__(self, parent, style='FlatFrame', **kw)

		frame = TFrame(self, style="RoundedFrame", borderwidth=5)
		frame.pack(side=LEFT)

		self.color_monitor = Canvas(frame, width=100, height=50, relief='flat')
		self.color_monitor.pack(side=TOP)

	def set_color(self, color):
		r, g, b = color.getRGB()
		int_color = (round(r * 255), round(g * 255), round(b * 255))
		text = '#%02X%02X%02X' % int_color
		self.color_monitor['bg'] = text

class RGBChooser(TFrame):

	def __init__(self, parent, callback, color=None, **kw):
		TFrame.__init__(self, parent, style='FlatFrame', **kw)

		frame = TFrame(self, style="RoundedFrame", borderwidth=5)
		frame.pack(side=LEFT)
		self.viewxy = ChooseRGBXY(frame, callback, xyramp_size[0], xyramp_size[1], 0, 1)
		self.viewxy.pack(side=LEFT)

		frame = TFrame(self, style="RoundedFrame", borderwidth=5)
		frame.pack(side=LEFT)
		self.viewz = ChooseRGBZ(frame, callback, zramp_size[0], zramp_size[1], 2)
		self.viewz.pack(side=LEFT)

	def set_color(self, color):
		r, g, b = color.getRGB()
		self.viewxy.SetColor((r, g, b))
		self.viewz.SetColor((r, g, b))


class ImageView(PyWidget):

	# display a PIL Image

	def __init__(self, master, image, **kw):
		width, height = image.size
		if not kw.has_key('width'):
			kw["width"] = width
		if not kw.has_key('height'):
			kw["height"] = height
		apply(PyWidget.__init__, (self, master), kw)
		self.gc_initialized = 0
		self.image = image
		self.ximage = None

	def MapMethod(self):
		if not self.gc_initialized:
			self.init_gc()
			self.gc_initialized = 1

	def init_gc(self):
		self.gc = self.tkwin.GetGC()
		self.visual = skvisual
		w = self.tkwin
		width, height = self.image.size
		depth = self.visual.depth
		if depth > 16:
			bpl = 4 * width
		elif depth > 8:
			bpl = ((2 * width + 3) / 4) * 4
		elif depth == 8:
			bpl = ((width + 3) / 4) * 4
		else:
			raise SketchError('unsupported depth for images')
		self.ximage = w.CreateImage(depth, ZPixmap, 0, None, width, height,
									32, bpl)
		self.set_image(self.image)

	def set_image(self, image):
		self.image = image
		if self.ximage:
			ximage = self.ximage
			_sketch.copy_image_to_ximage(self.visual, image.im, ximage,
											0, 0, ximage.width, ximage.height)
			self.UpdateWhenIdle()

	def RedrawMethod(self, region=None):
		self.gc.PutImage(self.ximage, 0, 0, 0, 0,
							self.ximage.width, self.ximage.height)

	def ResizedMethod(self, width, height):
		pass

class ChooseComponent(ImageView):

	def __init__(self, master, width, height, color=(0, 0, 0), **kw):
		image = Image.new('RGB', (width, height))
		apply(ImageView.__init__, (self, master, image), kw)
		self.set_color(color)
		self.drawn = 0
		self.dragging = 0
		self.drag_start = (0, 0, 0)
		self.update_pending = 1
		self.invgc = None
		self.bind('<ButtonPress>', self.ButtonPressEvent)
		self.bind('<Motion>', self.PointerMotionEvent)
		self.bind('<ButtonRelease>', self.ButtonReleaseEvent)

	def destroy(self):
		ImageView.destroy(self)
#		Publisher.Destroy(self)

	def set_color(self, color):
		self.color = tuple(color)

	def init_gc(self):
		ImageView.init_gc(self)
		self.invgc = self.tkwin.GetGC(foreground=~0,
										function=GXxor)
		self.tk.call(self._w, 'motionhints')
		self.show_mark()

	def ButtonPressEvent(self, event):
		if not self.dragging:
			self.drag_start = self.color
		self.dragging = self.dragging + 1
		self.move_to(self.win_to_color(event.x, event.y), event.state)

	def ButtonReleaseEvent(self, event):
		self.dragging = self.dragging - 1
		self.move_to(self.win_to_color(event.x, event.y), event.state)

	def PointerMotionEvent(self, event):
		if self.dragging:
			x, y = self.tkwin.QueryPointer()[4:6]
			self.move_to(self.win_to_color(x, y), event.state)

	#def moveto(self, x, y): #to be supplied by derived classes

	def hide_mark(self):
		if self.drawn:
			self.draw_mark()
			self.drawn = 0

	def show_mark(self):
		if not self.drawn and self.invgc:
			self.draw_mark()
			self.drawn = 1

	#def draw_mark(self):       # to be supplied by derived classes

	def UpdateWhenIdle(self):
		if not self.update_pending:
			self.update_pending = 1
			ImageView.UpdateWhenIdle(self)

	def RedrawMethod(self, region=None):
		if self.update_pending:
			self.update_ramp()
			self.update_pending = 0
		ImageView.RedrawMethod(self, region)
		if self.drawn:
			self.draw_mark()
	def getRGB(self):
		return (apply(hsv_to_rgb, self.color))

	def RGBColor(self):
		return apply(CreateRGBColor, apply(hsv_to_rgb, self.color)).RGB()

class ChooseRGBXY(ChooseComponent):

	def __init__(self, master, callback, width, height, xcomp=0, ycomp=1,
					color=(0, 0, 0), **kw):
		self.callback = callback
		self.xcomp = xcomp
		self.ycomp = ycomp
		self.win_to_color = Trafo(1 / float(width - 1), 0,
									0, -1 / float(height - 1),
									0, 1)
		self.color_to_win = self.win_to_color.inverse()
		apply(ChooseComponent.__init__, (self, master, width, height, color),
				kw)

	def SetColor(self, color):
		color = apply(rgb_to_hsv, tuple(color))
		otheridx = 3 - self.xcomp - self.ycomp
		if color[otheridx] != self.color[otheridx]:
			self.UpdateWhenIdle()
		self.hide_mark()
		self.color = color
		self.show_mark()

	def update_ramp(self):
		_sketch.fill_hsv_xy(self.image.im, self.xcomp, self.ycomp, self.color)
		self.set_image(self.image)

	def move_to(self, p, state):
		x, y = p
		if state & ConstraintMask:
			sx = self.drag_start[self.xcomp]
			sy = self.drag_start[self.ycomp]
			if abs(sx - x) < abs(sy - y):
				x = sx
			else:
				y = sy
		if x < 0:       x = 0
		elif x >= 1.0:  x = 1.0
		if y < 0:       y = 0
		elif y >= 1.0:  y = 1.0

		color = list(self.color)
		color[self.xcomp] = x
		color[self.ycomp] = y
		self.hide_mark()
		self.color = tuple(color)
		self.show_mark()
		self.callback(self.getRGB())
#		self.issue(CHANGED, self.RGBColor())

	def draw_mark(self):
		color = self.color
		w, h = self.image.size
		x, y = self.color_to_win(color[self.xcomp], color[self.ycomp])
		x = int(x)
		y = int(y)
		self.invgc.DrawLine(x, 0, x, h)
		self.invgc.DrawLine(0, y, w, y)


class ChooseRGBZ(ChooseComponent):

	def __init__(self, master, callback, width, height, comp=1, color=(0, 0, 0),
					**kw):
		self.callback = callback
		self.comp = comp
		self.win_to_color = Trafo(1, 0, 0, -1 / float(height - 1), 0, 1)
		self.color_to_win = self.win_to_color.inverse()
		apply(ChooseComponent.__init__, (self, master, width, height, color),
				kw)

	def SetColor(self, color):
		c = self.color;
		color = apply(rgb_to_hsv, tuple(color))
		if ((self.comp == 0 and (color[1] != c[1] or color[2] != c[2]))
			or (self.comp == 1 and (color[0] != c[0] or color[2] != c[2]))
			or (self.comp == 2 and (color[0] != c[0] or color[1] != c[1]))):
			self.hide_mark()
			self.color = color
			self.show_mark()
			self.UpdateWhenIdle()

	def update_ramp(self):
		_sketch.fill_hsv_z(self.image.im, self.comp, self.color)
		self.set_image(self.image)

	def move_to(self, p, state):
		y = p.y
		if y < 0:       y = 0
		elif y >= 1.0:  y = 1.0

		color = list(self.color)
		color[self.comp] = y
		self.hide_mark()
		self.color = tuple(color)
		self.show_mark()
		self.callback(self.getRGB())
#		self.issue(CHANGED, self.RGBColor())

	def draw_mark(self):
		w, h = self.image.size
		x, y = self.color_to_win(0, self.color[self.comp])
		x = int(x)
		y = int(y)
		self.invgc.DrawLine(0, y, w, y)

