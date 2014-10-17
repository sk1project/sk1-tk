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
from math import pi, tan

degrees = pi / 180.0

class SkewPanel(PluginPanel):
	name='Skew'
	title = _("Skew")


	def init(self, master):
		PluginPanel.init(self, master)

		self.width_priority=1
		
		root=self.mw.root
		
		self.var_angleX = DoubleVar(root)
		self.var_angleY = DoubleVar(root)
		
		jump=5
		self.var_angleX.set(0)
		self.var_angleY.set(0)
		
		self.var_proportional = IntVar(root)
		self.var_proportional.set(0)
		
		self.var_basepoint = StringVar(root)
		self.var_basepoint.set('C')
		
		#---------------------------------------------------------
		top = TFrame(self.panel, style='FlatFrame')
		top.pack(side = TOP, fill=BOTH)
		#---------------------------------------------------------
		# Horisontal 
		size_frameH = TFrame(top, style='FlatFrame', borderwidth=3)
		size_frameH.pack(side = TOP, fill = BOTH)
		
		label = TLabel(size_frameH, style='FlatLabel', image='skew_h')
		label.pack(side = LEFT, padx=5)
		self.entry_angleX = TSpinbox(size_frameH,  var=0, vartype=1, textvariable = self.var_angleX, 
									min = -75, max = 75, step = jump, width = 10, command=self.apply_skew)
		self.entry_angleX.pack(side = LEFT)
		
		self.labelwunit = TLabel(size_frameH, style='FlatLabel', text = _("deg"))
		self.labelwunit.pack(side = LEFT, padx=5)
		#---------------------------------------------------------
		# Vertical 
		
		size_frameV = TFrame(top, style='FlatFrame', borderwidth=3)
		size_frameV.pack(side = TOP, fill = BOTH)
		label = TLabel(size_frameV, style='FlatLabel', image='skew_v')
		label.pack(side = LEFT, padx=5)
		
		self.entry_angleY = TSpinbox(size_frameV, var=0, vartype=1, textvariable = self.var_angleY, 
									min = -75, max = 75, step = jump, width = 10, command=self.apply_skew)
		self.entry_angleY.pack(side = LEFT)
		
		self.labelhunit = TLabel(size_frameV, style='FlatLabel', text = _("deg"))
		self.labelhunit.pack(side = LEFT, padx=5)
		
		#---------------------------------------------------------
		# Basepoint check
		label = TLabel(top, style='FlatLabel', text = _("Basepoint:"))
		label.pack(side = TOP, fill = BOTH, padx=5)
		basepoint_frame=TLabelframe(top, labelwidget=label, style='Labelframe', borderwidth=4)
		basepoint_frame.pack(side = TOP, fill=X, padx=5, pady=2)
		
		self.Basepoint = BasePointSelector(basepoint_frame, anchor=self.var_basepoint)
		self.Basepoint.pack(side = LEFT, fill = BOTH, padx=5)
		
		label = TLabel(basepoint_frame, style='FlatLabel', image = 'coordinate_deg')
		label.pack(side = LEFT, fill = BOTH, padx=10)
		
		
		#---------------------------------------------------------
		# Button frame 
		
		button_frame = TFrame(top, style='FlatFrame', borderwidth=5)
		button_frame.pack(side = BOTTOM, fill = BOTH)

		self.update_buttons = []
		self.button = UpdatedButton(top, text = _("Apply"),
								command = self.apply_skew)
		self.button.pack(in_ = button_frame, side = BOTTOM, expand = 1, fill = X, pady=3)

		self.button_copy = UpdatedButton(top, text = _("Apply to Copy"),
								command = self.apply_to_copy)
		self.button_copy.pack(in_ = button_frame, side = BOTTOM, expand = 1, fill = X)
		
		self.init_from_doc()
		self.subscribe_receivers()


###############################################################################

	def subscribe_receivers(self):
		self.document.Subscribe(SELECTION, self.Update)

	def unsubscribe_receivers(self):
		self.document.Unsubscribe(SELECTION, self.Update)

	def init_from_doc(self):
		self.Update()

	def Update(self, *arg):
		if self.is_selection():
			self.entry_angleX.set_state(NORMAL)
			self.entry_angleY.set_state(NORMAL)
			self.button['state']=NORMAL
			self.button_copy['state']=NORMAL
		else:
			self.entry_angleX.set_state(DISABLED)
			self.entry_angleY.set_state(DISABLED)
			self.button['state']=DISABLED
			self.button_copy['state']=DISABLED

	def SkewSelected(self, axisX=0, axisY=0):
		if self.document.selection:
			self.document.begin_transaction()
			try:
				try:
					br=self.document.selection.coord_rect
					hor_sel=br.right - br.left
					ver_sel=br.top - br.bottom
					
					cnt_x,cnt_y=self.Basepoint.get_basepoint(hor_sel,ver_sel,br.left,br.bottom)
					
					text = _("Skew")
					ax,ay=tan(axisX),tan(axisY)
					sx=1.0
					sy=1.0-(ax*ay)
					tx=cnt_x*ax
					ty=cnt_y*ax*ay-cnt_y*ay
					# Move the selection in the coordinates x0 y0
					trafo = Trafo(1, 0, 0, 1, -cnt_x, -cnt_y)
					# Skew and Scaling
					trafo = Trafo(sx, ay, -ax, sy, 0, 0)(trafo)
					# Move the selection in the coordinates basepoint 
					trafo = Trafo(1, 0, 0, 1, cnt_x, cnt_y)(trafo)
					self.document.TransformSelected(trafo, text)
				except:
					self.document.abort_transaction()
			finally:
				self.document.end_transaction()

	def apply_skew(self, *arg):
		if self.button["state"]==DISABLED:
			return
		try:
			angleX=self.var_angleX.get()*degrees
			angleY=self.var_angleY.get()*degrees
			self.SkewSelected(angleX, angleY)
		except:
			return

	def apply_to_copy(self):
		if self.button["state"]==DISABLED:
			return
		self.document.begin_transaction(_("Skew&Copy"))
		try:
			try:
				self.document.ApplyToDuplicate()
				self.apply_skew()
			except:
				self.document.abort_transaction()
		finally:
			self.document.end_transaction()

	def is_selection(self):
		return (len(self.document.selection) > 0)


instance=SkewPanel()
app.transform_plugins.append(instance)
