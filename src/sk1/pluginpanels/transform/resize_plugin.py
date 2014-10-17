# -*- coding: utf-8 -*-

# Copyright (C) 2003-2006 by Igor E. Novikov
# Copyright (C) 2009 by Maxim S. Barabash
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from sk1sdk.libttk import TFrame, TLabel, TCheckbutton, TRadiobutton, TLabelframe
from Tkinter import Spinbox, DoubleVar, StringVar, BooleanVar, IntVar
from Tkinter import RIGHT, BOTTOM, X, Y, W, E, BOTH, LEFT, TOP, GROOVE, E, DISABLED, NORMAL
from sk1.tkext import UpdatedButton
from sk1.ttk_ext import TSpinbox
from sk1.widgets.basepoint import BasePointSelector

from app.conf.const import SELECTION, CHANGED, EDITED

from app import _, config, Rect, Trafo
from app.conf import const
import app

from sk1.pluginpanels.ppanel import PluginPanel

from sk1.widgets.lengthvar import LengthVar

class ResizePanel(PluginPanel):
	name='Resize'
	title = _("Resize")


	def init(self, master):
		PluginPanel.init(self, master)

		self.width_priority=1
		
		root=self.mw.root
		self.var_width_number=DoubleVar(root)
		self.var_height_number=DoubleVar(root)

		var_width_unit = StringVar(root)
		var_height_unit = StringVar(root)
		
		unit = config.preferences.default_unit
		self.var_width = LengthVar(10, unit, self.var_width_number, var_width_unit)
		self.var_height = LengthVar(10, unit,self.var_height_number,var_height_unit)
		
		jump=config.preferences.default_unit_jump
		self.var_width.set(0)
		self.var_height.set(0)
		
		self.var_proportional = IntVar(root)
		self.var_proportional.set(0)
		
		self.var_basepoint = StringVar(root)
		self.var_basepoint.set('C')
		
		#---------------------------------------------------------
		top = TFrame(self.panel, style='FlatFrame')
		top.pack(side = TOP, fill=BOTH)
		#---------------------------------------------------------
		# Horisontal size
		size_frameH = TFrame(top, style='FlatFrame', borderwidth=3)
		size_frameH.pack(side = TOP, fill = BOTH)
		
		label = TLabel(size_frameH, style='FlatLabel', image='size_h')
		label.pack(side = LEFT, padx=5)
		self.entry_width = TSpinbox(size_frameH,  var=0, vartype=1, textvariable = self.var_width_number, 
									min = 0, max = 50000, step = jump, width = 10, command=self.apply_resize)
		self.entry_width.pack(side = LEFT)

		self.entry_width.down_button.bind('<ButtonRelease>', self.entry_width_chang)
		self.entry_width.down_button.bind('<KeyRelease>', self.entry_width_chang)
		self.entry_width.up_button.bind('<ButtonRelease>', self.entry_width_chang)
		self.entry_width.up_button.bind('<KeyRelease>', self.entry_width_chang)
		self.entry_width.entry.bind('<ButtonRelease>', self.entry_width_chang)
		self.entry_width.entry.bind('<KeyRelease>', self.entry_width_chang)
		self.entry_width.entry.bind('<FocusOut>', self.entry_width_chang)
		self.entry_width.entry.bind('<FocusIn>', self.entry_width_FocusIn)
		
		self.labelwunit = TLabel(size_frameH, style='FlatLabel', text = self.var_width.unit)
		self.labelwunit.pack(side = LEFT, padx=5)
		#---------------------------------------------------------
		# Vertical 
		
		size_frameV = TFrame(top, style='FlatFrame', borderwidth=3)
		size_frameV.pack(side = TOP, fill = BOTH)
		label = TLabel(size_frameV, style='FlatLabel', image='size_v')
		label.pack(side = LEFT, padx=5)
		
		self.entry_height = TSpinbox(size_frameV, var=0, vartype=1, textvariable = self.var_height_number, 
									min = 0, max = 50000, step = jump, width = 10, command=self.apply_resize)
		self.entry_height.pack(side = LEFT)
		
		self.entry_height.down_button.bind('<ButtonRelease>', self.entry_height_chang)
		self.entry_height.down_button.bind('<KeyRelease>', self.entry_height_chang)
		self.entry_height.up_button.bind('<ButtonRelease>', self.entry_height_chang)
		self.entry_height.up_button.bind('<KeyRelease>', self.entry_height_chang)
		self.entry_height.entry.bind('<ButtonRelease>', self.entry_height_chang)
		self.entry_height.entry.bind('<KeyRelease>', self.entry_height_chang)
		self.entry_height.entry.bind('<FocusOut>', self.entry_height_chang)
		self.entry_height.entry.bind('<FocusIn>', self.entry_height_FocusIn)
		
		self.labelhunit = TLabel(size_frameV, style='FlatLabel', text = self.var_height.unit)
		self.labelhunit.pack(side = LEFT, padx=5)
		
		#---------------------------------------------------------
		# Proportional chek
		
		self.proportional_check = TCheckbutton(top, text = _("Proportional"), variable = self.var_proportional, command = self.proportional)
		self.proportional_check.pack(side = TOP, anchor=W, padx=5,pady=5)
		
		#---------------------------------------------------------
		# Basepoint check
		label = TLabel(top, style='FlatLabel', text = _("Basepoint:"))
		label.pack(side = TOP, fill = BOTH, padx=5)
		basepoint_frame=TLabelframe(top, labelwidget=label, style='Labelframe', borderwidth=4)
		basepoint_frame.pack(side = TOP, fill=X, padx=5, pady=2)
		
		self.Basepoint = BasePointSelector(basepoint_frame, anchor=self.var_basepoint)
		self.Basepoint.pack(side = LEFT, fill = BOTH, padx=5)
		
		label = TLabel(basepoint_frame, style='FlatLabel', image = 'coordinate_sys')
		label.pack(side = LEFT, fill = BOTH, padx=10)
			
		#---------------------------------------------------------
		# Button frame 
		
		button_frame = TFrame(top, style='FlatFrame', borderwidth=5)
		button_frame.pack(side = BOTTOM, fill = BOTH)

		self.update_buttons = []
		self.button = UpdatedButton(top, text = _("Apply"),
								command = self.apply_resize)
		self.button.pack(in_ = button_frame, side = BOTTOM, expand = 1, fill = X, pady=3)

		self.button_copy = UpdatedButton(top, text = _("Apply to Copy"),
								command = self.apply_to_copy)
		self.button_copy.pack(in_ = button_frame, side = BOTTOM, expand = 1, fill = X)
		
		self.subscribe_receivers()
		self.Update()


###############################################################################

	def subscribe_receivers(self):
		self.document.Subscribe(SELECTION, self.Update)	
		self.document.Subscribe(EDITED, self.update_var)
		config.preferences.Subscribe(CHANGED, self.update_pref)

	def unsubscribe_receivers(self):
		self.document.Unsubscribe(SELECTION, self.Update)	
		self.document.Unsubscribe(EDITED, self.update_var)
		config.preferences.Unsubscribe(CHANGED, self.update_pref)

	def init_from_doc(self, *arg):
			self.Update()

	def Update(self, *arg):
		if self.is_selection():
			self.entry_width.set_state(NORMAL)
			self.entry_height.set_state(NORMAL)
			self.proportional_check['state']=NORMAL
			self.button['state']=NORMAL
			self.button_copy['state']=NORMAL
		else:
			self.entry_width.set_state(DISABLED)
			self.entry_height.set_state(DISABLED)
			self.proportional_check['state']=DISABLED
			self.button['state']=DISABLED
			self.button_copy['state']=DISABLED
			self.var_width.set(0)
			self.var_height.set(0)
			
		self.update_pref()

	def entry_width_FocusIn(self, *arg):
		self.width_priority=1

	def entry_height_FocusIn(self, *arg):
		self.width_priority=0

	def ResizeSelected(self, h, v, cnt_x=None, cnt_y=None):
		text = _("Resize")
		if self.document.selection:
			self.document.begin_transaction(text)
			try:
				try:
					br=self.document.selection.coord_rect
					hor_sel=br.right - br.left
					ver_sel=br.top - br.bottom
					if cnt_x is None:
						cnt_x=hor_sel/2+br.left
					if cnt_y is None:
						cnt_y=ver_sel/2+br.bottom
					trafo = Trafo(h, 0, 0, v, cnt_x-cnt_x*h, cnt_y-cnt_y*v)
					self.document.TransformSelected(trafo, text)
				except:
					self.document.abort_transaction()
			finally:
				self.document.end_transaction()

	def ResizeAndCopy(self, h, v, cnt_x=None, cnt_y=None):
		text = _("Resize&Copy")
		if self.document.selection:
			self.document.begin_transaction(text)
			try:
				try:
					br=self.document.selection.coord_rect
					hor_sel=br.right - br.left
					ver_sel=br.top - br.bottom
					if cnt_x is None:
						cnt_x=hor_sel/2+br.left
					if cnt_y is None:
						cnt_y=ver_sel/2+br.bottom
					trafo = Trafo(h, 0, 0, v, cnt_x-cnt_x*h, cnt_y-cnt_y*v)
					self.document.ApplyToDuplicate()
					self.document.TransformSelected(trafo, text)
				except:
					self.document.abort_transaction()
			finally:
				self.document.end_transaction()

	def entry_height_chang(self, *arg):
		if self.var_proportional.get():
			try:
				height=self.var_height.get()
				br=self.document.selection.coord_rect
				hor_sel=br.right - br.left
				ver_sel=br.top - br.bottom
				self.var_width.set(hor_sel * height/ver_sel)
			except ZeroDivisionError:
				return

	def entry_width_chang(self, *arg):
		if self.var_proportional.get():
			try:
				width=self.var_width.get()
				br=self.document.selection.coord_rect
				hor_sel=br.right - br.left
				ver_sel=br.top - br.bottom
				self.var_height.set(ver_sel * width/hor_sel)
			except ZeroDivisionError:
				return

	def proportional(self):
		if self.width_priority:
			self.entry_width_chang()
		else:
			self.entry_height_chang()

	def apply_resize(self, *arg):
		if self.button["state"]==DISABLED:
			return
		self.proportional()
		width=self.var_width.get()
		height=self.var_height.get()
		br=self.document.selection.coord_rect
		hor_sel=br.right - br.left
		ver_sel=br.top - br.bottom
		cnt_x,cnt_y=self.Basepoint.get_basepoint(hor_sel,ver_sel,br.left,br.bottom)
		
		try:
			h=width/hor_sel
		except ZeroDivisionError:
			h=0
		
		try:
			v=height/ver_sel
		except ZeroDivisionError:
			v=0
		
		if arg and arg[0] == 'Duplicate':
			self.ResizeAndCopy(h, v, cnt_x, cnt_y)
		else:
			self.ResizeSelected(h, v, cnt_x, cnt_y)
		
		self.update_var()

	def apply_to_copy(self):
		self.apply_resize('Duplicate')

	def update_pref(self, *arg):
		self.labelwunit['text']=config.preferences.default_unit
		self.labelhunit['text']=config.preferences.default_unit
		self.var_width.unit=config.preferences.default_unit
		self.var_height.unit=config.preferences.default_unit
		self.entry_width.step=config.preferences.default_unit_jump
		self.entry_height.step=config.preferences.default_unit_jump
		self.update_var()
		
	def update_var(self, *arg):
		if len(self.document.selection.GetInfo()):
			br=self.document.selection.coord_rect
			width=br.right - br.left
			height=br.top - br.bottom
			self.var_width.set(width)
			self.var_height.set(height)

	def is_selection(self):
		return (len(self.document.selection) > 0)


instance=ResizePanel()
app.transform_plugins.append(instance)
