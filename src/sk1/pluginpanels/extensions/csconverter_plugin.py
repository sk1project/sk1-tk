# -*- coding: utf-8 -*-

# Copyright (C) 2009 by Maxim S. Barabash, Igor E.Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from sk1sdk.libttk import TFrame, TLabel, TButton, TCombobox
from Tkinter import IntVar, StringVar
from Tkinter import RIGHT, BOTTOM, X, Y, BOTH, LEFT, TOP, W, E, DISABLED, NORMAL
from sk1sdk.libttk import tooltips

from app.conf.const import SELECTION, DOCUMENT, EDITED

from app import _, config, Rect, mw, EmptyPattern, SolidPattern, NullUndo
from app.Graphics.color import CreateRGBAColor, CreateCMYKAColor
from app.conf import const
import app
from sk1.tkext import UpdatedButton

from sk1.pluginpanels.ppanel import PluginPanel


RGB=_('RGB color')
CMYK=_('CMYK color')


class ColorSpaceConverter(PluginPanel):
	name='ColorSpaceConverter'
	title = _("Color Space Converter")


	def init(self, master):
		PluginPanel.init(self, master)
		top = TFrame(self.panel, style='FlatFrame', borderwidth=7)
		top.pack(side = TOP, fill=BOTH)
		
		sign = TFrame(top, style='RoundedFrame', borderwidth=5)
		sign.pack(side=TOP)

		self.sign = TLabel(sign, image='color_converter')
		self.sign.pack(side=TOP)
		
		self.cs_name = StringVar(top)
		self.cs_name.set(RGB)
		
		label = TLabel(top, text=_("Colorspace:")+" ")
		label.pack(side = TOP, anchor=W)
		
		self.colorspaces = TCombobox(top, state='readonly', postcommand = self.set_cs, 
									 values=self.make_cs_list(), width=14, style='ComboNormal',
									 textvariable=self.cs_name)
		self.colorspaces.pack(side = TOP, fill=X, pady=3)
		
		button = UpdatedButton(top, text = _("Apply"),
								command = self.apply_colorspace,
								sensitivecb = self.is_selection)
		button.pack(side = BOTTOM, expand = 1, fill = X, pady=3)
		self.Subscribe(SELECTION, button.Update)
		


		self.init_from_doc()
		self.subscribe_receivers()

###############################################################################
	def is_selection(self):
		return (len(self.document.selection) > 0)
	
	def subscribe_receivers(self):
		self.document.Subscribe(SELECTION, self.init_from_doc)

	def unsubscribe_receivers(self):
		self.document.Unsubscribe(SELECTION, self.init_from_doc)

	def init_from_doc(self, *arg):
		self.issue(SELECTION)

	def Update(self):
		pass

	def make_cs_list(self):
		cs=()
		cs+=(RGB,CMYK)
		return cs

	def set_cs(self):
		pass

	def apply_colorspace(self):
		objects = self.document.selection.GetObjects()
		name = self.cs_name.get()
		if name==RGB:
			cs_name= 'RGB'
		elif name==CMYK:
			cs_name= 'CMYK'
		
		self.document.begin_transaction(name)
		try:
			try:
				add_undo = self.document.add_undo
				self.apply_cs(objects, cs_name)
				add_undo(self.document.queue_edited())
			except:
				self.document.abort_transaction()
		finally:
			self.document.end_transaction()
		app.mw.canvas.ForceRedraw()

	def apply_cs(self, objects, cs_name):
		for object in objects:
			if object.is_Compound:
				self.apply_cs(object.GetObjects(),cs_name)
			
			elif object.is_Text or object.is_Bezier or object.is_Rectangle or object.is_Ellipse:
				self.document.add_undo(self.FillStyle(object,cs_name))
				self.document.add_undo(self.OutlineStyle(object,cs_name))
			
			elif object.is_Image:
				if not cs_name==object.data.image_mode:
					self.document.add_undo(object.Convert(cs_name))


	def FillStyle(self, object, cs_name):
		undo_info = None
		try:
			fill_pattern = object.properties.fill_pattern
			
			if fill_pattern is EmptyPattern:
				pass
			
			elif fill_pattern.is_Solid:
				color=fill_pattern.Color()
				undo_info = self.setSolidPatternFill(object, color, cs_name)
			
			elif fill_pattern.is_Hatching:
				pass
			
			elif fill_pattern.is_Tiled:
				pass
			
			elif fill_pattern.is_Gradient:
				pass
			
			elif fill_pattern.is_Image:
				pass
		finally:
			if undo_info is not None:
				return undo_info
			return NullUndo

	def setSolidPatternFill(self, object, color, cs_name):
		if color.model == cs_name:
			return
		color=self.convert_color(color, cs_name)
		undo=(object.SetProperties(fill_pattern=SolidPattern(color)))
		return undo



	def OutlineStyle(self, object, cs_name):
		undo_info = None
		try:
			line_pattern=object.properties.line_pattern
			if line_pattern is EmptyPattern:
					pass
			elif line_pattern.is_Solid:
					color=line_pattern.Color()
					undo_info = self.setSolidPatternOutline(object, color, cs_name)
		finally:
			if undo_info is not None:
				return undo_info
			return NullUndo

	def setSolidPatternOutline(self, object, color, cs_name):
		if color.model == cs_name:
			return
		color=self.convert_color(color, cs_name)
		undo=(object.SetProperties(line_pattern=SolidPattern(color)))
		return undo




	def convert_color(self, color, cs_name):
		if cs_name is None:
			return color
		
		elif cs_name == 'CMYK':
			c, m, y, k = color.getCMYK()
			return CreateCMYKAColor(c, m, y, k, color.alpha)
		
		elif cs_name == 'RGB':
			r, g, b = color.getRGB()
			return CreateRGBAColor(r, g, b, color.alpha)

instance=ColorSpaceConverter()
app.extentions_plugins.append(instance)
