# -*- coding: utf-8 -*-

# Copyright (C) 2003-2006 by Igor E. Novikov
# Copyright (C) 1998, 1999, 2000, 2003 by Bernhard Herzog
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

import string
from colorsys import hsv_to_rgb, rgb_to_hsv

from PIL import Image
from Tkinter import TOP, BOTTOM, LEFT, RIGHT, X, BOTH, DoubleVar

from app.conf.const import CHANGED, ConstraintMask
from app import _, _sketch
from app import CreateRGBColor, StandardColors, Trafo, SketchError, Publisher
from app.Graphics import color

from sk1.x11const import GXxor, ZPixmap
from sk1sdk.libttk import TFrame, TButton, TLabel
from sk1.tkext import PyWidget
from sk1.ttk_ext import TSpinbox, TEntrybox
from sk1.dialogs.sketchdlg import SKModal

class MyDoubleVar(DoubleVar):

	def __init__(self, master=None, precision=3):
		self.precision = precision
		DoubleVar.__init__(self, master)

	def set(self, value):
		DoubleVar.set(self, round(value, self.precision))

	def set_precision(self, precision):
		self.precision = precision


class ColorSample(PyWidget):

	def __init__(self, master=None, color=None, **kw):
		apply(PyWidget.__init__, (self, master), kw)
		self.gc_initialized = 0
		if color is None:
			color = StandardColors.black
		self.color = color

	def MapMethod(self):
		if not self.gc_initialized:
			self.init_gc()
			self.gc_initialized = 1

	def init_gc(self):
		self.visual = color.skvisual
		self.set_color(self.color)

	def set_color(self, color):
		self.color = color
		self.tkwin.SetBackground(self.visual.get_pixel(self.color))
		self.UpdateWhenIdle()

	def SetColor(self, color):
		if self.color != color:
			self.set_color(color)

	def RedrawMethod(self, region=None):
		self.tkwin.ClearArea(0, 0, 0, 0, 0)

	def ResizedMethod(self, width, height):
		pass


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
		self.visual = color.skvisual
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

class ChooseComponent(ImageView, Publisher):

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
		Publisher.Destroy(self)

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

	def RGBColor(self):
		return apply(CreateRGBColor, apply(hsv_to_rgb, self.color)).RGB()

class ChooseRGBXY(ChooseComponent):

	def __init__(self, master, width, height, xcomp=0, ycomp=1,
					color=(0, 0, 0), **kw):
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
		self.issue(CHANGED, self.RGBColor())

	def draw_mark(self):
		color = self.color
		w, h = self.image.size
		x, y = self.color_to_win(color[self.xcomp], color[self.ycomp])
		x = int(x)
		y = int(y)
		self.invgc.DrawLine(x, 0, x, h)
		self.invgc.DrawLine(0, y, w, y)


class ChooseRGBZ(ChooseComponent):

	def __init__(self, master, width, height, comp=1, color=(0, 0, 0),
					**kw):
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
		self.issue(CHANGED, self.RGBColor())

	def draw_mark(self):
		w, h = self.image.size
		x, y = self.color_to_win(0, self.color[self.comp])
		x = int(x)
		y = int(y)
		self.invgc.DrawLine(0, y, w, y)


xyramp_size = (170, 170)
zramp_size = (15, 170)

class ChooseColorDlg(SKModal):

	title = _("Select RGB Color")
	class_name = 'ColorDialog'

	def __init__(self, master, color, **kw):
		self.color = color.RGB()
		self.orig_color = color.RGB()
		apply(SKModal.__init__, (self, master), kw)

	def build_dlg(self):
		super = self.top
		top = TFrame(super, borderwidth=10, style='FlatFrame')
		top.pack(side=TOP, fill=BOTH, expand=1)

		frame = TFrame(top, style='FlatFrame')
		frame.pack(side=BOTTOM, fill=BOTH, expand=0)

		label = TLabel(top, style="HLine")
		label.pack(side=BOTTOM, fill=BOTH, expand=0)

		button = TButton(frame, text=_("Cancel"), command=self.cancel)
		button.pack(side=RIGHT, expand=0)
		label = TLabel(frame, image="space_6", style="FlatLabel")
		label.pack(side=RIGHT)
		button = TButton(frame, text=_("OK"), command=self.ok)
		button.pack(side=RIGHT, expand=0)
		button = TButton(frame, image='colorpicker', state='disabled')
		button.pack(side=LEFT, expand=0)

#       RGBlabel_frame = TFrame(top, borderwidth = 1, style='FlatFrame')
#       RGBlabel_frame.pack(side = BOTTOM, fill = BOTH)
#
#       self.label = TLabel(RGBlabel_frame, style="FlatLabel")
#       self.label.pack(side = LEFT)


		frame = TFrame(top, style="RoundedFrame", borderwidth=5)
		frame.pack(side=LEFT)
		viewxy = ChooseRGBXY(frame, xyramp_size[0], xyramp_size[1], 0, 1)
		viewxy.pack(side=LEFT)

		frame = TFrame(top, style="RoundedFrame", borderwidth=5)
		frame.pack(side=LEFT)
		viewz = ChooseRGBZ(frame, zramp_size[0], zramp_size[1], 2)
		viewz.pack(side=LEFT)

		frame1 = TFrame(top, borderwidth=3, style='FlatFrame')
		frame1.pack(side=RIGHT)

		CS_frame = TFrame(frame1, borderwidth=1, style='FlatFrame')
		CS_frame.pack(side=TOP)

		label = TLabel(CS_frame, text="Old color:   \nNew color:   ", justify='right')
		label.pack(side=LEFT)

		frame = TFrame(CS_frame, style="RoundedFrame", borderwidth=5)
		frame.pack(side=LEFT)

		self.sample = ColorSample(frame, self.color, width=60, height=20)
		self.sample.pack(side=BOTTOM)
		sample = ColorSample(frame, self.color, width=60, height=20)
		sample.pack(side=TOP)

		label = TLabel(frame1, style="HLine")
		label.pack(side=TOP, fill=BOTH, expand=0)

		spin_frame = TFrame(frame1, borderwidth=1, style='FlatFrame')
		spin_frame.pack(side=TOP)

		hsv_frame = TFrame(spin_frame, borderwidth=2, style='FlatFrame')
		hsv_frame.pack(side=LEFT)

		frame = TFrame(hsv_frame, borderwidth=2, style='FlatFrame')
		frame.pack(side=TOP)
		label = TLabel(frame, text="H: ")
		label.pack(side=LEFT)
		self.var1 = TSpinbox(frame, min=0, max=1.0, step=0.01, vartype=1, command=self.component_changed)
		self.var1.pack(side=RIGHT)

		frame = TFrame(hsv_frame, borderwidth=2, style='FlatFrame')
		frame.pack(side=TOP)
		label = TLabel(frame, text="S: ")
		label.pack(side=LEFT)
		self.var2 = TSpinbox(frame, min=0, max=1.0, step=0.01, vartype=1, command=self.component_changed)
		self.var2.pack(side=RIGHT)

		frame = TFrame(hsv_frame, borderwidth=2, style='FlatFrame')
		frame.pack(side=TOP)
		label = TLabel(frame, text="V: ")
		label.pack(side=LEFT)
		self.var3 = TSpinbox(frame, min=0, max=1.0, step=0.01, vartype=1, command=self.component_changed)
		self.var3.pack(side=RIGHT)


		rgb_frame = TFrame(spin_frame, borderwidth=2, style='FlatFrame')
		rgb_frame.pack(side=LEFT)

		frame = TFrame(rgb_frame, borderwidth=2, style='FlatFrame')
		frame.pack(side=TOP)
		label = TLabel(frame, text="R: ")
		label.pack(side=LEFT)
		self.var4 = TSpinbox(frame, min=0, max=255, step=1, vartype=0, command=self.rgb_component_changed)
		self.var4.pack(side=RIGHT)

		frame = TFrame(rgb_frame, borderwidth=2, style='FlatFrame')
		frame.pack(side=TOP)
		label = TLabel(frame, text="G: ")
		label.pack(side=LEFT)
		self.var5 = TSpinbox(frame, min=0, max=255, step=1, vartype=0, command=self.rgb_component_changed)
		self.var5.pack(side=RIGHT)

		frame = TFrame(rgb_frame, borderwidth=2, style='FlatFrame')
		frame.pack(side=TOP)
		label = TLabel(frame, text="B: ")
		label.pack(side=LEFT)
		self.var6 = TSpinbox(frame, min=0, max=255, step=1, vartype=0, command=self.rgb_component_changed)
		self.var6.pack(side=RIGHT)

		HTML_frame = TFrame(frame1, borderwidth=3, style='FlatFrame')
		HTML_frame.pack(side=TOP)

		label = TLabel(HTML_frame, text="HTML: ")
		label.pack(side=LEFT)
		self.html = TEntrybox(HTML_frame, text='#000000', width=10, command=self.html_component_changed)
		self.html.pack(side=LEFT)



		viewxy.Subscribe(CHANGED, self.color_changed)
		viewz.Subscribe(CHANGED, self.color_changed)
		self.viewxy = viewxy
		self.viewz = viewz

		super.resizable(width=0, height=0)

		self.color_changed(self.color)

	def color_changed(self, color):
#       self.label.configure(text = 'RGB:( %.3f %.3f %.3f )' % tuple(color))
		self.viewxy.SetColor(color)
		self.viewz.SetColor(color)
		self.sample.SetColor(color)
		v1, v2, v3 = apply(rgb_to_hsv, tuple(color))
		self.var1.set_value(v1)
		self.var2.set_value(v2)
		self.var3.set_value(v3)
		self.var4.set_value(round(color[0] * 255))
		self.var5.set_value(round(color[1] * 255))
		self.var6.set_value(round(color[2] * 255))
		int_color = (round(color[0] * 255), round(color[1] * 255), round(color[2] * 255))
		self.html.set_text('#%02X%02X%02X' % int_color)
		self.color = color


	def component_changed(self, *rest):
		color = (self.var1.get_value(), self.var2.get_value(), self.var3.get_value())
		color = apply(CreateRGBColor, apply(hsv_to_rgb, color)).RGB()
		self.color_changed(color)

	def rgb_component_changed(self, *rest):
		RGBColor = CreateRGBColor(self.var4.get_value() / 255.0,
												self.var5.get_value() / 255.0,
												self.var6.get_value() / 255.0).RGB()
		self.color_changed(RGBColor)

	def html_component_changed(self, *rest):
		html = self.html.get_text()
		try:
				RGBColor = CreateRGBColor(int(string.atoi(html[1:3], 0x10)) / 255.0,
														int(string.atoi(html[3:5], 0x10)) / 255.0,
														int(string.atoi(html[5:], 0x10)) / 255.0).RGB()
		except:
				RGBColor = self.color
		self.color_changed(RGBColor)



	def ok(self, *args):
		r, g, b = tuple(self.color)
		ColorObject = CreateRGBColor(r, g, b)
		self.close_dlg(ColorObject)

def GetColor(master, color):
	dlg = ChooseColorDlg(master, color)
	return dlg.RunDialog()
