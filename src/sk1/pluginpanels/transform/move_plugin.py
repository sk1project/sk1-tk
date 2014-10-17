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

from app import _, config, Point
from app.conf import const
import app

ABSOLUTE = 'Absolute'
RELATIVE = 'Relative'

from sk1.pluginpanels.ppanel import PluginPanel

from sk1.widgets.lengthvar import LengthVar

class MovePanel(PluginPanel):
	name='Move'
	title = _("Move")


	def init(self, master):
		PluginPanel.init(self, master)

		root=self.mw.root
		self.var_width_number=DoubleVar(root)
		self.var_height_number=DoubleVar(root)
		
		self.var_width_base=DoubleVar(root)
		self.var_height_base=DoubleVar(root)

		var_width_unit = StringVar(root)
		var_height_unit = StringVar(root)
		
		unit = config.preferences.default_unit
		self.var_width = LengthVar(10, unit, self.var_width_number, var_width_unit)
		self.var_height = LengthVar(10, unit,self.var_height_number,var_height_unit)
		
		jump=config.preferences.default_unit_jump
		self.var_width.set(0)
		self.var_height.set(0)
		
		self.var_width_base.set(0)
		self.var_height_base.set(0)
		
		self.var_position = StringVar(root)
		self.var_position.set(ABSOLUTE)
		
		self.var_basepoint = StringVar(root)
		self.var_basepoint.set('C')
		 
		#---------------------------------------------------------
		top = TFrame(self.panel, style='FlatFrame')
		top.pack(side = TOP, fill=BOTH)
		#---------------------------------------------------------
		# Horisontal size
		size_frameH = TFrame(top, style='FlatFrame', borderwidth=3)
		size_frameH.pack(side = TOP, fill = BOTH)
		
		label = TLabel(size_frameH, style='FlatLabel', image='move_h')
		label.pack(side = LEFT, padx=5)
		self.entry_width = TSpinbox(size_frameH,  var=0, vartype=1, textvariable = self.var_width_number, 
									min = -50000, max = 50000, step = jump, width = 10, command=self.apply_move)
		self.entry_width.pack(side = LEFT)

		self.labelwunit = TLabel(size_frameH, style='FlatLabel', text = self.var_width.unit)
		self.labelwunit.pack(side = LEFT, padx=5)
		#---------------------------------------------------------
		# Vertical 
		
		size_frameV = TFrame(top, style='FlatFrame', borderwidth=3)
		size_frameV.pack(side = TOP, fill = BOTH)
		label = TLabel(size_frameV, style='FlatLabel', image='move_v')
		label.pack(side = LEFT, padx=5)
		
		self.entry_height = TSpinbox(size_frameV, var=0, vartype=1, textvariable = self.var_height_number, 
									min = -50000, max = 50000, step = jump, width = 10, command=self.apply_move)
		self.entry_height.pack(side = LEFT)
		
		self.labelhunit = TLabel(size_frameV, style='FlatLabel', text = self.var_height.unit)
		self.labelhunit.pack(side = LEFT, padx=5)
		
		#---------------------------------------------------------
		# position chek
		
		self.position_check = TCheckbutton(top, text = _("Absolute Coordinates"), variable = self.var_position,
												onvalue=ABSOLUTE, offvalue=RELATIVE, command = self.position)
		self.position_check.pack(side = TOP, anchor=W, padx=5,pady=5)
		
		#---------------------------------------------------------
		# Basepoint check
		
		label = TLabel(top, style='FlatLabel', text = _("Basepoint:"))
		label.pack(side = TOP, fill = BOTH, padx=5)
		basepoint_frame=TLabelframe(top, labelwidget=label, style='Labelframe', borderwidth=4)
		basepoint_frame.pack(side = TOP, fill=X, padx=5, pady=2)
		
		self.Basepoint = BasePointSelector(basepoint_frame, anchor=self.var_basepoint, command = self.apply_basepoint)
		self.Basepoint.pack(side = LEFT, fill = BOTH, padx=5)
		
		label = TLabel(basepoint_frame, style='FlatLabel', image = 'coordinate_sys')
		label.pack(side = LEFT, fill = BOTH, padx=10)
			
		#---------------------------------------------------------
		# Button frame 
		
		button_frame = TFrame(top, style='FlatFrame', borderwidth=5)
		button_frame.pack(side = BOTTOM, fill = BOTH)
		
		self.update_buttons = []
		self.button = UpdatedButton(top, text = _("Apply"),
								command = self.apply_move)
		self.button.pack(in_ = button_frame, side = BOTTOM, expand = 1, fill = X, pady=3)
		
		self.button_copy = UpdatedButton(top, text = _("Apply to Copy"),
								command = self.apply_to_copy)
		self.button_copy.pack(in_ = button_frame, side = BOTTOM, expand = 1, fill = X)
		
		self.init_from_doc()
		self.subscribe_receivers()


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
			self.position_check['state']=NORMAL
			self.button['state']=NORMAL
			self.button_copy['state']=NORMAL
		else:
			self.entry_width.set_state(DISABLED)
			self.entry_height.set_state(DISABLED)
			self.position_check['state']=DISABLED
			self.button['state']=DISABLED
			self.button_copy['state']=DISABLED
			
		self.update_pref()

	def apply_basepoint(self):
		self.Update()

	def position(self):
		if self.var_position.get()==ABSOLUTE and self.var_basepoint.get()=='USER':
			self.var_basepoint.set('C')
		self.update_var()

	def apply_move(self, *arg):
		if self.button["state"]==DISABLED:
			return
		try:
				var_x=self.var_width.get()
				var_y=self.var_height.get()
		except:
				return
		
		x, y = self.coordinates(self.var_position.get())
		
		if self.var_position.get()==RELATIVE:
			if self.var_width_base != self.var_width.get() or self.var_height_base != self.var_height.get():
				self.var_basepoint.set('USER')
			x,y = var_x, var_y
		else:
			x,y = var_x-x, var_y-y
		
		if arg and arg[0] == 'Duplicate':
			self.document.MoveAndCopy(x, y, Point(0,0))
		else:
			self.document.MoveSelected(x, y)

	def apply_to_copy(self):
		self.apply_move('Duplicate')


	def coordinates(self, position):
		br=self.document.selection.coord_rect
		hor_sel=br.right - br.left
		ver_sel=br.top - br.bottom
		
		if position == RELATIVE:
			left, bottom = -hor_sel/2, -ver_sel/2
		else:
			left, bottom = br.left, br.bottom
		
		cnt_x,cnt_y=self.Basepoint.get_basepoint(hor_sel,ver_sel,left,bottom)
		
		if position == RELATIVE and cnt_x!=None:
			return cnt_x*2, cnt_y*2
		else:
			return cnt_x, cnt_y

	def update_pref(self, *arg):
		self.labelwunit['text']=config.preferences.default_unit
		self.labelhunit['text']=config.preferences.default_unit
		self.entry_width.step=config.preferences.default_unit_jump
		self.entry_height.step=config.preferences.default_unit_jump
		self.update_var()

	def update_var(self, *arg):
		if len(self.document.selection.GetInfo()):
			if self.var_basepoint.get() == 'USER':
				x=self.var_width.get()
				y=self.var_height.get()
				self.var_width.unit=config.preferences.default_unit
				self.var_height.unit=config.preferences.default_unit
				self.var_width.set(x)
				self.var_height.set(y)
				
			else:
				self.var_width.unit=config.preferences.default_unit
				self.var_height.unit=config.preferences.default_unit
				x, y = self.coordinates(self.var_position.get())
				self.var_width.set(x)
				self.var_height.set(y)
				self.var_width_base=self.var_width.get()
				self.var_height_base=self.var_height.get()

	def is_selection(self):
		return (len(self.document.selection) > 0)


instance=MovePanel()
app.transform_plugins.append(instance)
