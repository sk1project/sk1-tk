# -*- coding: utf-8 -*-

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

from app import _, config, Point, Rotation
from app.conf import const
import app

from math import pi

degrees = pi / 180.0


from sk1.pluginpanels.ppanel import PluginPanel

from sk1.widgets.lengthvar import LengthVar

ABSOLUTE = 'Absolute'
RELATIVE = 'Relative'


class RotatePanel(PluginPanel):
	name='Rotate'
	title = _("Rotate")


	def init(self, master):
		PluginPanel.init(self, master)

		root=self.mw.root
		
		self.var_angle=DoubleVar(root)
		self.var_angle.set(0)
		
		self.var_width_number=DoubleVar(root)
		self.var_height_number=DoubleVar(root)
		
		self.var_width_base=DoubleVar(root)
		self.var_height_base=DoubleVar(root)
		
		self.cnt_x_absolute=None
		self.cnt_y_absolute=None
			
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
		
		angle_frame = TFrame(top, style='FlatFrame', borderwidth=3)
		angle_frame.pack(side = TOP, fill = BOTH)
		label = TLabel(angle_frame, style='FlatLabel', text = " "+_("Angle:")+" ")
		label.pack(side = LEFT, padx=5)
		
		self.entry_angle = TSpinbox(angle_frame, var=0, vartype=1, textvariable = self.var_angle, 
									min = -360, max = 360, step = 5, width = 6, command=self.apply_rotate)
		self.entry_angle.pack(side = LEFT, anchor = E)
		label = TLabel(angle_frame, style='FlatLabel', text = _("deg"))
		label.pack(side = LEFT, padx=5)
		#---------------------------------------------------------
		label = TLabel(top, style='FlatLabel', text = _("Center:"))
		label.pack(side = TOP, fill = BOTH, padx=5)
		
		#---------------------------------------------------------
		# Horisontal
		size_frameH = TFrame(top, style='FlatFrame', borderwidth=3)
		size_frameH.pack(side = TOP, fill = BOTH)
		
		label = TLabel(size_frameH, style='FlatLabel', image='center_h')
		label.pack(side = LEFT, padx=5)
		self.entry_width = TSpinbox(size_frameH,  var=0, vartype=1, textvariable = self.var_width_number, 
									min = -50000, max = 50000, step = jump, width = 10, command=self.apply_rotate)
		self.entry_width.pack(side = LEFT)

		self.labelwunit = TLabel(size_frameH, style='FlatLabel', text = self.var_width.unit)
		self.labelwunit.pack(side = LEFT, padx=5)
		#---------------------------------------------------------
		# Vertical 
		
		size_frameV = TFrame(top, style='FlatFrame', borderwidth=3)
		size_frameV.pack(side = TOP, fill = BOTH)
		label = TLabel(size_frameV, style='FlatLabel', image='center_v')
		label.pack(side = LEFT, padx=5)
		
		self.entry_height = TSpinbox(size_frameV, var=0, vartype=1, textvariable = self.var_height_number, 
									min = -50000, max = 50000, step = jump, width = 10, command=self.apply_rotate)
		self.entry_height.pack(side = LEFT)
		
		self.labelhunit = TLabel(size_frameV, style='FlatLabel', text = self.var_height.unit)
		self.labelhunit.pack(side = LEFT, padx=5)
		
		#---------------------------------------------------------
		# position chek
		
		self.position_check = TCheckbutton(top, text = _("Absolute Center"), variable = self.var_position,
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
		
		label = TLabel(basepoint_frame, style='FlatLabel', image = 'coordinate_deg')
		label.pack(side = LEFT, fill = BOTH, padx=10)
		
		self.position_check.pack(side = TOP, anchor=W, padx=5,pady=5)
		
		#---------------------------------------------------------
		# Button frame 
		
		button_frame = TFrame(top, style='FlatFrame', borderwidth=5)
		button_frame.pack(side = BOTTOM, fill = BOTH)
		
		self.update_buttons = []
		self.button = UpdatedButton(top, text = _("Apply"),
								command = self.apply_rotate)
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
			self.entry_angle.set_state(NORMAL)
			self.entry_width.set_state(NORMAL)
			self.entry_height.set_state(NORMAL)
			self.position_check['state']=NORMAL
			self.button['state']=NORMAL
			self.button_copy['state']=NORMAL
			self.TestBasepoint()
		else:
			self.entry_angle.set_state(DISABLED)
			self.entry_width.set_state(DISABLED)
			self.entry_height.set_state(DISABLED)
			self.position_check['state']=DISABLED
			self.button['state']=DISABLED
			self.button_copy['state']=DISABLED
			
		self.update_pref()

	def apply_basepoint(self):
		self.update_var()

	def position(self):
		self.update_var()

	def RotateSelected(self, angle, cnt=None):
		text = _("Rotation")
		if self.document.selection:
			self.document.begin_transaction(text)
			try:
				try:
					if cnt is None:
						cnt = self.document.selection.coord_rect.center()
					angle=angle*degrees
					trafo = Rotation(angle, cnt)
					self.document.TransformSelected(trafo, text)
				except:
					self.document.abort_transaction()
			finally:
				self.document.end_transaction()

	def RotateAndCopy(self, angle, cnt=None):
		text = _("Rotation&Copy")
		if self.document.selection:
			self.document.begin_transaction(text)
			try:
				try:
					if cnt is None:
						cnt = self.document.selection.coord_rect.center()
					angle=angle*degrees
					trafo = Rotation(angle, cnt)
					self.document.ApplyToDuplicate()
					self.document.TransformSelected(trafo, text)
				except:
					self.document.abort_transaction()
			finally:
				self.document.end_transaction()






	def apply_rotate(self, *arg):
		if self.button["state"]==DISABLED:
			return
		
		try:
				var_x=self.var_width.get()
				var_y=self.var_height.get()
				var_a=self.var_angle.get()
		except:
				return
		
		if var_a<0:
			if var_a<-360:
				var_a+=int(var_a/360)*360
			var_a+=360
		
		if 	self.var_basepoint.get() != 'USER':
			self.cnt_x_absolute, self.cnt_y_absolute=self.coordinates(ABSOLUTE)
			self.var_basepoint.set('USER')
		
		if self.var_width_base != var_x or self.var_height_base != var_y:
			
			if self.var_position.get()==ABSOLUTE:
				self.cnt_x_absolute=var_x
				self.cnt_y_absolute=var_y
			else:
				x,y=self.coordinates(ABSOLUTE, 'C')
				self.cnt_x_absolute=var_x+x
				self.cnt_y_absolute=var_y+y
			
			self.var_basepoint.set('USER')
			
		if arg and arg[0] == 'Duplicate':
			self.RotateAndCopy(var_a, Point(self.cnt_x_absolute, self.cnt_y_absolute))
		else:
			self.RotateSelected(var_a, Point(self.cnt_x_absolute, self.cnt_y_absolute))


	def apply_to_copy(self):
		self.apply_rotate('Duplicate')


	def coordinates(self, position, anchor=None):
		br=self.document.selection.coord_rect
		hor_sel=br.right - br.left
		ver_sel=br.top - br.bottom
		
		if position == RELATIVE:
			left, bottom = -hor_sel/2.0, -ver_sel/2.0
		else:
			left, bottom = br.left, br.bottom
		
		cnt_x,cnt_y=self.Basepoint.get_basepoint(hor_sel,ver_sel,left,bottom, anchor)
		return cnt_x, cnt_y

	def TestBasepoint(self):
		if self.cnt_x_absolute is None:
			return
		base = ['C', 'NW', 'N', 'NE', 'W', 'E', 'SW', 'S', 'SE']
		for b in xrange (len(base)):
			cnt_x,cnt_y=self.coordinates(ABSOLUTE, base[b])
			if round(cnt_x,2) == round(self.cnt_x_absolute,2) and \
								round(cnt_y,2) == round(self.cnt_y_absolute,2):
				self.var_basepoint.set(base[b])
				return
		self.var_basepoint.set('USER')

	def update_pref(self, *arg):
		self.labelwunit['text']=config.preferences.default_unit
		self.labelhunit['text']=config.preferences.default_unit
		self.entry_width.step=config.preferences.default_unit_jump
		self.entry_height.step=config.preferences.default_unit_jump
		self.update_var()

	def update_var(self, *arg):
		if len(self.document.selection.GetInfo()):
			
			self.var_width.unit=config.preferences.default_unit
			self.var_height.unit=config.preferences.default_unit
			
			if self.var_basepoint.get() == 'USER':
				
				if self.var_position.get()==ABSOLUTE:
					self.var_width.set(self.cnt_x_absolute)
					self.var_height.set(self.cnt_y_absolute)
				else:
					x, y=self.coordinates(ABSOLUTE, 'C')
					self.var_width.set(self.cnt_x_absolute-x)
					self.var_height.set(self.cnt_y_absolute-y)
				
			else:
				x, y = self.coordinates(self.var_position.get())
				self.var_width.set(x)
				self.var_height.set(y)
				self.var_width_base=self.var_width.get()
				self.var_height_base=self.var_height.get()

	def is_selection(self):
		return (len(self.document.selection) > 0)


instance=RotatePanel()
app.transform_plugins.append(instance)
