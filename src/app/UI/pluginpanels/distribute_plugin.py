# -*- coding: utf-8 -*-

# Copyright (C) 2003-2008 by Igor E. Novikov
# Copyright (C) 2009 by Maxim S. Barabash
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from Tkinter import IntVar, StringVar
from Ttk import TLabel, TFrame, TRadiobutton, TLabelframe, TCombobox
from Tkinter import BOTH, LEFT, RIGHT, TOP, X, Y, BOTTOM, W

from app.conf.const import SELECTION
from app.conf import const
from app import _, Point

from app.UI.tkext import UpdatedRadiobutton

import app
from ppanel import PluginPanel
import tooltips


SELECT=_("Selection")
PAGE=_("Page")

def make_button(*args, **kw):
	kw['style'] ='ToolBarCheckButton'
	return apply(TRadiobutton, args, kw)

class DistributePlugin(PluginPanel):
	
	name='Distribute'
	title = _("Distribute")
	
	def init(self, master):
		PluginPanel.init(self, master)
		top = self.panel
		
		self.var_reference = StringVar(top)
		self.var_reference.set(SELECT)
		#---------------------------------------------------------
		label=TLabel(top, text=_(" Relative to "), style="FlatLabel")
		label.pack()
		rel_frame=TLabelframe(top, labelwidget=label, style='Labelframe', borderwidth=4)
		rel_frame.pack(side = TOP, fill=X, padx=5, pady=2)
		button_frame=TFrame(rel_frame, style='FlatFrame')
		button_frame.pack(side = TOP, fill = BOTH, padx=5)
		
		self.reference = TCombobox(button_frame, state='readonly', values=self.make_cs_list(), style='ComboNormal',width=14,
									 textvariable=self.var_reference)
		self.reference.pack(side = TOP)

		#---------------------------------------------------------
		label=TLabel(top, text=_(" Distribute type "), style="FlatLabel")
		label.pack()
		framec=TLabelframe(top, labelwidget=label, style='Labelframe', borderwidth=4)
		framec.pack(side = TOP, fill=X, padx=5, pady=5)
		
		framex = TFrame(framec, style='FlatFrame')
		framex.pack(side = TOP, expand = 0)
		
		framey = TFrame(framec, style='FlatFrame')
		framey.pack(side = TOP, expand = 0)


		x_pixmaps = ['doleft', 'docenterh', 'dospacingh', 'doright']
		y_pixmaps = ['dotop', 'docenterv', 'dospacingv', 'dobottom']
		x_tooltips = [_('Distribute left sides equidistantly'),
						_('Distribute centers equidistantly horizontally'),
						_('Make horizontal gaps between objects equal'),
						_('Distribute right sides equidistantly')]

		y_tooltips = [_('Distribute tops sides equidistantly'),
						_('Distribute centers equidistantly vertically'),
						_('Make vertical gaps between objects equal'),
						_('Distribute bottoms sides equidistantly')]

		self.var_x = IntVar(top)
		self.var_x.set(0)
		self.var_y = IntVar(top)
		self.var_y.set(0)
		
		for i in range(1, 5):
			button = make_button(framex, image = x_pixmaps[i - 1], value = i, variable = self.var_x, command = self.apply_x)
			tooltips.AddDescription(button, x_tooltips[i - 1])
			button.pack(side = LEFT, padx = 3)
			button = make_button(framey, image = y_pixmaps[i - 1], value = i, variable = self.var_y, command = self.apply_y)
			tooltips.AddDescription(button, y_tooltips[i - 1])
			button.pack(side = LEFT, padx = 3)
		

###############################################################################

	def make_cs_list(self):
		cs=()
		cs+=(SELECT,PAGE)
		return cs

	def set_cs(self):
		pass

	def is_selection(self):
		return (len(self.document.selection) > 1)

	def HDistributeSelection(self, x, reference = SELECT):
		if self.is_selection() and x:
			self.document.begin_transaction(_("Distribute Objects"))
			try:
				try:
					add_undo = self.document.add_undo
					objects = self.document.selection.GetObjects()
					if reference == PAGE:
						brleft, brbottom, brright, brtop = self.document.PageRect()
					else:
						brleft,  brbottom, brright, brtop = self.document.selection.coord_rect
					
					posh = []
					total_width=0
					for obj in objects:
						rect = obj.coord_rect
						posh.append((rect.left, rect.right - rect.left, obj))
						total_width += rect.right - rect.left
					posh.sort()
					
					first_obj_left, first_obj_width, first_obj = posh[0]
					last_obj_left, last_obj_width, last_obj = posh[-1]
					
					# how much influence of the width. 1-no, 0-full
					part_obj_dict=[None, 1.0, 0.5, 1.0, 0]
					# influence the width last object
					first_obj_dict = [None, 0, first_obj_width*0.5, 0, first_obj_width]
					# influence the width last object
					last_obj_dict  = [None, last_obj_width, last_obj_width*0.5, 0, 0]
					# influence the width. 0-no , 1-yes
					width_obj_dict = [None, 0,0,1,0]
					
					brleft  += first_obj_dict[x]
					brright -= last_obj_dict[x]
					brwidth = (brright-brleft - total_width*width_obj_dict[x])
					step = brwidth / (len(self.document.selection)-1)
					
					part=part_obj_dict[x]
					next = 0
					for left, width, obj in posh[0:]:
						off = Point(next - left +brleft - width + width*part, 0)
						self.document.add_undo(obj.Translate(off))
						next += step+width*width_obj_dict[x]
					add_undo(self.document.queue_edited())
				except:
					self.document.abort_transaction()
			finally:
				self.document.end_transaction()



	def VDistributeSelection(self, y, reference = SELECT):
		if self.is_selection() and y:
			self.document.begin_transaction(_("Distribute Objects"))
			try:
				try:
					add_undo = self.document.add_undo
					objects = self.document.selection.GetObjects()
					if reference == PAGE:
						brleft, brbottom, brright, brtop = self.document.PageRect()
					else:
						brleft,  brbottom, brright, brtop = self.document.selection.coord_rect
					
					posv = []
					total_height=0
					for obj in objects:
						rect = obj.coord_rect
						posv.append((rect.top, rect.bottom - rect.top, obj))
						total_height += rect.bottom - rect.top
					posv.sort()
					posv.reverse()
					
					first_obj_top, first_obj_height, first_obj = posv[0]
					last_obj_top, last_obj_height, last_obj = posv[-1]
					
					# how much influence of the height. 1-no, 0-full
					part_obj_dict=[None, 1.0, 0.5, 1.0, 0]
					# influence the height last object
					first_obj_dict = [None, 0, first_obj_height*0.5, 0, first_obj_height]
					# influence the height last object
					last_obj_dict  = [None, last_obj_height, last_obj_height*0.5, 0, 0]
					# influence the height. 0-no , 1-yes
					height_obj_dict = [None, 0,0,1,0]
					
					brtop  += first_obj_dict[y]
					brbottom -= last_obj_dict[y]
					brwidth = (brbottom-brtop - total_height*height_obj_dict[y])
					step = brwidth / (len(self.document.selection)-1)
					part=part_obj_dict[y]
					next = 0
					for top, height, obj in posv[0:]:
						off = Point(0, next - top +brtop - height + height*part)
						self.document.add_undo(obj.Translate(off))
						next += step+height*height_obj_dict[y]
					add_undo(self.document.queue_edited())
				except:
					self.document.abort_transaction()
			finally:
					self.document.end_transaction()

	def apply_x(self):
		x = self.var_x.get()
		reference = self.var_reference.get()
		self.reset()
		self.HDistributeSelection(x, reference = reference)

	def apply_y(self):
		y = self.var_y.get()
		reference = self.var_reference.get()
		self.reset()
		self.VDistributeSelection(y, reference = reference)

	def reset(self):
		self.var_x.set(0)
		self.var_y.set(0)

instance=DistributePlugin()
app.effects_plugins.append(instance)

