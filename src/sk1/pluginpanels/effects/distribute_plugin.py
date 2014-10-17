# -*- coding: utf-8 -*-

# Copyright (C) 2003-2008 by Igor E. Novikov
# Copyright (C) 2009 by Maxim S. Barabash
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from Tkinter import IntVar, StringVar
from sk1sdk.libttk import TLabel, TFrame, TRadiobutton, TLabelframe, TCombobox, TCheckbutton, TButton
from Tkinter import BOTH, LEFT, RIGHT, TOP, X, Y, BOTTOM, W, DISABLED, NORMAL

from app.conf.const import SELECTION
from app.conf import const
from app import _, Point

from sk1.tkext import UpdatedRadiobutton

import app
from app import config
from sk1.pluginpanels.ppanel import PluginPanel
from sk1sdk.libttk import tooltips


TRANSACTION=_("Distribute Objects")

SELECT=_("Selection")
PAGE=_("Page")
EDGE=_("Edge + Jump")

def make_button(*args, **kw):
	kw['style'] ='FineRadiobutton'
	return apply(TRadiobutton, args, kw)

class DistributePlugin(PluginPanel):
	
	name='Distribute'
	title = _("Distribution")
	
	def init(self, master):
		PluginPanel.init(self, master)
		root=self.mw.root
		self.var_reference = StringVar(root)
		self.var_reference.set(SELECT)
		
		#---------------------------------------------------------
		top = TFrame(self.panel, style='FlatFrame')
		top.pack(side = TOP, fill=BOTH)
		#---------------------------------------------------------
		label=TLabel(top, text=" "+_("Relative to")+" ", style="FlatLabel")
		label.pack(side = TOP, fill = BOTH, padx=5)
		rel_frame=TLabelframe(top, labelwidget=label, style='Labelframe', borderwidth=4)
		rel_frame.pack(side = TOP, fill=X, padx=5, pady=2)
		button_frame=TFrame(rel_frame, style='FlatFrame')
		button_frame.pack(side = TOP, fill = BOTH, padx=5)
		
		self.reference = TCombobox(button_frame, state='readonly', values=self.make_cs_list(), style='ComboNormal',width=14,
									 textvariable=self.var_reference, postcommand = self.set_cs)
		self.reference.pack(side = TOP)
		#---------------------------------------------------------
		label=TLabel(top, text=" "+_("Distribute type")+" ", style="FlatLabel")
		label.pack(side = TOP, fill = BOTH, padx=5)
		framec=TLabelframe(top, labelwidget=label, style='Labelframe', borderwidth=3)
		framec.pack(side = TOP, fill=X, padx=5, pady=2)
		
		
		framex = TFrame(framec, style='FlatFrame')
		framex.pack(side = TOP, expand = 0, padx = 5, pady = 5)
		
		framey = TFrame(framec, style='FlatFrame')
		framey.pack(side = TOP, expand = 0, padx = 5, pady = 5)


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
		self.value_x = 0
		self.var_y = IntVar(top)
		self.var_y.set(0)
		self.value_y = 0
		
		for i in range(1, 5):
			button = make_button(framex, image = x_pixmaps[i - 1], value = i, variable = self.var_x, command = self.apply_x)
			tooltips.AddDescription(button, x_tooltips[i - 1])
			button.pack(side = LEFT, padx = 3)
			button = make_button(framey, image = y_pixmaps[i - 1], value = i, variable = self.var_y, command = self.apply_y)
			tooltips.AddDescription(button, y_tooltips[i - 1])
			button.pack(side = LEFT, padx = 3)
		
		#---------------------------------------------------------
		# Auto Apply Check
		self.var_auto_apply = IntVar(top)
		self.var_auto_apply.set(0)
		
		self.auto_apply_check = TCheckbutton(top, text = _("Auto Apply"), variable = self.var_auto_apply, command = self.reset)
		self.auto_apply_check.pack(side = TOP, anchor=W, padx=5,pady=5)
		
		#---------------------------------------------------------
		# Button frame 
		
		self.button_frame = TFrame(top, style='FlatFrame', borderwidth=5)
		self.button_frame.pack(side = BOTTOM, fill = BOTH)
		
		self.update_buttons = []
		self.button_apply = TButton(self.button_frame, text = _("Apply"),
								command = self.apply_distribute)
		
		self.apply_button_show(1)

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
		reference = self.var_reference.get()
		if self.is_selection(reference):
			state=NORMAL
		else:
			state=DISABLED
		self.button_apply['state']=state

	def apply_button_show(self, state):
		if not state:
			self.button_apply.pack_forget()
		else:
			self.button_apply.pack(side = BOTTOM, expand = 1, fill = X, pady=3)

	def make_cs_list(self):
		cs=()
		cs+=(SELECT,PAGE,EDGE)
		return cs

	def set_cs(self):
		self.Update()

	def is_selection(self, reference = SELECT):
		if not self.var_auto_apply.get() and self.value_x==0 and self.value_y==0:
			return 0
		if reference == SELECT:
			return (len(self.document.selection) > 2)
		else:
			return (len(self.document.selection) > 1)

	def HDistributeSelection(self, x, reference = SELECT):
		if self.is_selection(reference) and x:
			self.document.begin_transaction(TRANSACTION)
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
					if reference == EDGE:
						step = config.preferences.handle_jump
					else:
						step = brwidth / (len(posh)-1)
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
		if self.is_selection(reference) and y:
			self.document.begin_transaction(TRANSACTION)
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
					if reference == EDGE:
						step = -1*config.preferences.handle_jump
					else:
						step = brwidth / (len(posv)-1)
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
		if self.var_auto_apply.get():
			self.reset()
			self.HDistributeSelection(x, reference = reference)
		else:
			if self.value_x==x:
				self.var_x.set(0)
				self.value_x = 0
			else:
				self.value_x = x
			self.Update()

	def apply_y(self):
		y = self.var_y.get()
		reference = self.var_reference.get()
		if self.var_auto_apply.get():
			self.reset()
			self.VDistributeSelection(y, reference = reference)
		else:
			if self.value_y==y:
				self.var_y.set(0)
				self.value_y = 0
			else:
				self.value_y = y
			self.Update()

	def apply_distribute(self):
		if self.var_auto_apply.get():
			return
		self.document.begin_transaction(TRANSACTION)
		try:
			try:
				reference = self.var_reference.get()
				x = self.value_x
				y = self.value_y
				self.HDistributeSelection(x, reference = reference)
				self.VDistributeSelection(y, reference = reference)
			except:
				self.document.abort_transaction()
		finally:
					self.document.end_transaction()

	def reset(self):
		self.var_x.set(0)
		self.value_x = 0
		self.var_y.set(0)
		self.value_y = 0
##		self.apply_button_show(not self.var_auto_apply.get())
		self.Update()

instance=DistributePlugin()
app.effects_plugins.append(instance)

