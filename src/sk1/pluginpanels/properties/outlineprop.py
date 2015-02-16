# -*- coding: utf-8 -*-

# Copyright (C) 2009 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from sk1sdk.libttk import TFrame, TLabel, TCheckbutton, TButton, TLabelframe
from Tkinter import IntVar, DoubleVar, StringVar
from Tkinter import RIGHT, BOTTOM, X, Y, BOTH, LEFT, TOP, W, E, DISABLED, NORMAL
from sk1.ttk_ext import TSpinbox
from sk1.widgets.colorbutton import TColorButton

from app.conf.const import SELECTION, DOCUMENT, EDITED, CHANGED

from app import _, config, Rect, mw, StandardDashes, SolidPattern, EmptyPattern
from app.conf import const
import app
from sk1.tkext import UpdatedButton, UpdatedRadiobutton, TOptionMenu

from sk1.pluginpanels.ppanel import PluginPanel
from sk1.widgets.lengthvar import LengthVar
from sk1.dialogs import styledlg

from sk1sdk.libttk import tooltips

from PIL import Image, ImageDraw


DEFAULT_WIDTH = 0.283286
DEFAULT_CORNER = const.JoinMiter
DEFAULT_CAPS = const.CapButt
DEFAULT_STYLE = 0
DASH_SIZE = (96, 16)
DASH_WIDTH = 3


class OutlinePropertiesPanel(PluginPanel):
	name = 'OutlineProperties'
	title = _("Outline Properties")
	dashlist = []
	dash = ()
	ref_style = None
	color = None

	def init(self, master):
		PluginPanel.init(self, master)

		root = self.mw.root

		top = TFrame(self.panel, style='FlatFrame', borderwidth=5)
		top.pack(side=TOP, fill=BOTH)

		########### APPLY BUTTON ################################################
		button = UpdatedButton(top, text=_("Apply"),
								command=self.apply_properties,
								sensitivecb=self.is_correct_selection)
		button.pack(side=BOTTOM, expand=1, fill=X)
		self.Subscribe(SELECTION, button.Update)

		########### COLOR BUTTON ################################################

		color_frame = TFrame(top, style='FlatFrame', borderwidth=3)
		color_frame.pack(side=TOP)

		label = TLabel(color_frame, style='FlatLabel', text=_('Color:'))
		label.pack(side=LEFT, padx=5)

		self.color_button = TColorButton(color_frame, command=self.show_outline_color)
		self.color_button.pack(side=LEFT, padx=5)
		self.color_button.set_color((255, 0, 0))

		########### LINE WIDTH ##################################################

		self.var_width_number = DoubleVar(root)

		self.var_width_base = DoubleVar(root)

		var_width_unit = StringVar(root)

		unit = config.preferences.default_unit

		self.var_width = LengthVar(10, unit, self.var_width_number, var_width_unit)

		line_width_frame = TFrame(top, style='FlatFrame', borderwidth=3)
		line_width_frame.pack(side=TOP, fill=BOTH)

		self.labelwunit = TLabel(line_width_frame, style='FlatLabel', text=self.var_width.unit)
		self.labelwunit.pack(side=RIGHT, padx=5)

		self.entry_width = TSpinbox(line_width_frame, var=0, vartype=1, textvariable=self.var_width_number,
									min=0, max=50000, step=.1, width=8, command=self.update_pattern)
		self.entry_width.pack(side=RIGHT)

		label = TLabel(line_width_frame, style='FlatLabel', text=_('Line width:'))
		label.pack(side=RIGHT, padx=5)
		########### LINE STYLE #################################################
		style_frame = TFrame(top, style='FlatFrame', borderwidth=5)
		style_frame.pack(side=TOP, fill=X)

		for item in range(1, 12):
			self.dashlist.append("dash%d" % (item))

		self.style_button = TOptionMenu(style_frame, self.dashlist, command=self.set_dash,
									entry_type='image', style='TComboSmall')
		self.style_button.pack(side=RIGHT, fill=X)

		label = TLabel(style_frame, style='FlatLabel', text=_('Style:'))
		label.pack(side=RIGHT, padx=5)

		########################################################################
		selection_frame = TFrame(top, style='FlatFrame', borderwidth=1)
		selection_frame.pack(side=TOP)

		########### CORNERS #####################################################

		label = TLabel(selection_frame, text=" " + _("Corners:") + " ", style="FlatLabel")
		label.pack()

		corners_frame = TLabelframe(selection_frame, labelwidget=label, style='Labelframe', borderwidth=8)

		corners_frame.pack(side=LEFT, fill=Y, pady=1, padx=1)

		self.var_corner = IntVar(root)
		radio = UpdatedRadiobutton(corners_frame, image="join_miter",
									variable=self.var_corner,
									value=const.JoinMiter,
									command=self.update_pattern)
		radio.pack(side=TOP, anchor=W, pady=2)

		radio = UpdatedRadiobutton(corners_frame, image="join_round",
									variable=self.var_corner,
									value=const.JoinRound,
									command=self.update_pattern)
		radio.pack(side=TOP, anchor=W, pady=2)

		radio = UpdatedRadiobutton(corners_frame, image="join_bevel",
									variable=self.var_corner,
									value=const.JoinBevel,
									command=self.update_pattern)
		radio.pack(side=TOP, anchor=W, pady=2)


		########### LINE CAPS ###################################################

		label = TLabel(selection_frame, text=" " + _("Line caps:") + " ", style="FlatLabel")
		label.pack()

		caps_frame = TLabelframe(selection_frame, labelwidget=label, style='Labelframe', borderwidth=8)

		caps_frame.pack(side=RIGHT, fill=Y, pady=1, padx=1)

		self.var_caps = IntVar(root)
		radio = UpdatedRadiobutton(caps_frame, image="cap_butt",
									variable=self.var_caps,
									value=const.CapButt,
									command=self.update_pattern)
		radio.pack(side=TOP, anchor=W, pady=2)

		radio = UpdatedRadiobutton(caps_frame, image="cap_round",
									variable=self.var_caps,
									value=const.CapRound,
									command=self.update_pattern)
		radio.pack(side=TOP, anchor=W, pady=2)

		radio = UpdatedRadiobutton(caps_frame, image="cap_projecting",
									variable=self.var_caps,
									value=const.CapProjecting,
									command=self.update_pattern)
		radio.pack(side=TOP, anchor=W, pady=2)
		self.var_caps.set(0)

		############ BOTTOM BUTTONS #############################################

		button_frame = TFrame(top, style='FlatFrame', borderwidth=1)
		button_frame.pack(side=BOTTOM, fill=X, pady=5)

		button = TButton(button_frame, style='TSmallbutton', text=' ', image='small_colorpicker', command=self.copy_from)
		button.pack(side=LEFT)
		tooltips.AddDescription(button, _("Copy From..."))

		button = TButton(button_frame, style='TSmallbutton', text=' ', image='restore_color', command=self.restore_properties)
		button.pack(side=LEFT, padx=5)
		tooltips.AddDescription(button, _("Restore properties"))

		self.var_autoupdate = IntVar(top)
		self.var_autoupdate.set(1)

		self.autoupdate_check = TCheckbutton(button_frame, text=_("Auto Update"), variable=self.var_autoupdate,
											command=self.init_from_doc)
		self.autoupdate_check.pack(side=RIGHT, anchor=W, padx=10)
		#######################################################################


		self.set_default_style()

		self.init_from_doc()
		self.subscribe_receivers()

###############################################################################
	def is_correct_selection(self):
		return (len(self.document.selection) > 0)

	def subscribe_receivers(self):
		self.document.Subscribe(SELECTION, self.init_from_doc)
		self.document.Subscribe(EDITED, self.init_from_doc)
		config.preferences.Subscribe(CHANGED, self.update_pref)

	def unsubscribe_receivers(self):
		self.document.Unsubscribe(SELECTION, self.init_from_doc)
		self.document.Unsubscribe(EDITED, self.init_from_doc)
		config.preferences.Unsubscribe(CHANGED, self.update_pref)

	def init_from_doc(self, *arg):
		self.issue(SELECTION)
		if self.var_autoupdate.get():
			if self.is_correct_selection():
				if len(self.document.selection) > 1:
					info, obj = self.document.selection.GetInfo()[0]
					self.update_from_object(obj)
				else:
					self.init_from_style(self.document.CurrentProperties())
			else:
				self.ref_style = None
				self.set_default_style()

	def set_dash(self, value):
		if value in self.dashlist:
			dash_index = self.dashlist.index(value)
			self.dash = StandardDashes()[dash_index]

	def update_pattern(self, *args):
		pass

	def apply_properties(self):
		kw = {}
		if self.color is not None:
			kw["line_pattern"] = SolidPattern(self.color)
			kw["line_width"] = self.var_width.get()
			kw["line_join"] = self.var_corner.get()
			kw["line_cap"] = self.var_caps.get()
			kw["line_dashes"] = self.dash
		else:
			kw["line_pattern"] = EmptyPattern
		styledlg.set_properties(self.mw.root, self.document, _("Set Outline Properties"), 'line', kw)

	def copy_from(self):
		self.mw.canvas.PickObject(self.update_from_object)

	def show_outline_color(self):
		self.mw.LoadPlugin('OutlineColor')

	def update_from_object(self, obj):
		if obj is not None:
			self.init_from_style(obj.Properties())

	def restore_properties(self):
		self.init_from_style(self.ref_style)

	def init_from_style(self, initial_style):
		if initial_style is None:
			self.set_default_style()
			return
		import copy
		self.ref_style = copy.copy(initial_style)
		style = self.ref_style
		if style.HasLine():
			self.var_corner.set(style.line_join)
			self.var_caps.set(style.line_cap)
			self.color = copy.copy(style.line_pattern.Color())
			r, g, b = style.line_pattern.Color().getRGB()
			self.color_button.set_color((int(round(r * 255)),
										int(round(g * 255)),
										int(round(b * 255))))
			self.var_width.set(style.line_width)
			self.dash = style.line_dashes
			if style.line_dashes in StandardDashes():
				dash_index = StandardDashes().index(self.dash)
				self.style_button.SetValue(self.dashlist[dash_index])
			else:
				dash_image = self.generate_dash_image(style.line_dashes)
				self.style_button.SetValue(dash_image)
		else:
			self.set_default_style()

	def set_default_style(self):
		self.var_corner.set(DEFAULT_CORNER)
		self.var_caps.set(DEFAULT_CAPS)
		self.color_button.set_color(None)
		self.color = None
		self.var_width.set(DEFAULT_WIDTH)
		self.style_button.SetValue(self.dashlist[0])

	def generate_dash_image(self, dashes):
		self.generated_image = Image.new("RGBA", DASH_SIZE, (0, 0, 0, 0))
		draw = ImageDraw.Draw(self.generated_image)
		point = 0
		fill = 1
		y = int(DASH_SIZE[1] / 2)
		while point < DASH_SIZE[0]:
			for item in dashes:
				if fill:
					color = (0, 0, 0, 1)
					fill = 0
				else:
					color = (0, 0, 0, 0)
					fill = 1
				draw.line([(point, y), (point + item * DASH_WIDTH, y)], color, DASH_WIDTH)
				point += item * DASH_WIDTH
		from PIL import ImageTk
		self.generated_tk_image = ImageTk.PhotoImage(self.generated_image)
		return self.generated_tk_image

	def update_pref(self, *arg):
		self.labelwunit['text'] = config.preferences.default_unit
		self.var_width.UpdateUnit(config.preferences.default_unit)
		self.init_from_doc()


instance = OutlinePropertiesPanel()
app.objprop_plugins.append(instance)



