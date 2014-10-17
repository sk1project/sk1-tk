# -*- coding: utf-8 -*-

# Copyright (C) 2003-2008 by Igor E. Novikov
# Copyright (C) 2009 by Maxim S. Barabash
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from Tkinter import Frame, Radiobutton, IntVar, StringVar, Label
from sk1sdk.libttk import TLabel, TFrame, TRadiobutton, TLabelframe, TCombobox, TCheckbutton, TButton
from Tkinter import BOTH, LEFT, RIGHT, TOP, X, Y, BOTTOM, W, DISABLED, NORMAL

from app.conf.const import SELECTION
from app.conf import const
from app import _

from sk1.tkext import UpdatedButton, UpdatedCheckbutton, UpdatedRadiobutton

import app
from sk1.pluginpanels.ppanel import PluginPanel
from sk1sdk.libttk import tooltips

SELECT=_("Selection")
LOWERMOST=_("Lowermost")
PAGE=_("Page")


def make_button(*args, **kw):
	kw['style'] ='FineRadiobutton'
	return apply(TRadiobutton, args, kw)

class AlignPlugin(PluginPanel):
	
	name='Alignment'
	title = _("Alignment")
	
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
		rel_frame=TLabelframe(top, labelwidget=label, style='Labelframe', borderwidth=3)
		rel_frame.pack(side = TOP, fill=X, padx=5, pady=2)
		
		self.reference = TCombobox(rel_frame, state='readonly', values=self.make_cs_list(), style='ComboNormal',width=14,
									 textvariable=self.var_reference, postcommand = self.set_cs)
		self.reference.pack(side = TOP)
		#---------------------------------------------------------

		label=TLabel(top, text=" "+_("Alignment type")+" ", style="FlatLabel")
		label.pack(side = TOP, fill = BOTH, padx=5)
		framec=TLabelframe(top, labelwidget=label, style='Labelframe', borderwidth=3)
		framec.pack(side = TOP, fill=X, padx=5, pady=2)
		
		framex = TFrame(framec, style='FlatFrame')
		framex.pack(side = TOP, expand = 0, padx = 5, pady = 5)
		
		framey = TFrame(framec, style='FlatFrame')
		framey.pack(side = TOP, expand = 0, padx = 5, pady = 5)


		x_pixmaps = ['aoleft', 'aocenterh', 'aoright']
		y_pixmaps = ['aotop', 'aocenterv', 'aobottom']
		x_tooltips = [_('Align left sides'),
						_('Center on vertical axis'),
						_('Align right sides')]

		y_tooltips = [_('Align tops'),
						_('Center on horizontal axis'),
						_('Align bottoms')]
						
		self.var_x = IntVar(top)
		self.var_x.set(0)
		self.value_x = 0
		self.var_y = IntVar(top)
		self.var_y.set(0)
		self.value_y = 0

		for i in range(1, 4):
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
								command = self.apply)
		
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
		self.issue(SELECTION)

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
		cs+=(SELECT,LOWERMOST,PAGE)
		return cs

	def set_cs(self):
		self.Update()

	def is_selection(self, reference = SELECT):
		if not self.var_auto_apply.get() and self.value_x==0 and self.value_y==0:
			return 0
		if reference == PAGE:
			return (len(self.document.selection) > 0)
		else:
			return (len(self.document.selection) > 1)

	def apply_x(self):
		x = self.var_x.get()
		if self.var_auto_apply.get():
			self.reset()
			self.apply(x=x)
		else:
			if self.value_x==x:
				self.var_x.set(0)
				self.value_x = 0
			else:
				self.value_x = x
			self.Update()

	def apply_y(self):
		y = self.var_y.get()
		if self.var_auto_apply.get():
			self.reset()
			self.apply(y=y)
		else:
			if self.value_y==y:
				self.var_y.set(0)
				self.value_y = 0
			else:
				self.value_y = y
			self.Update()

	def apply(self, x=None, y=None, reference = None):
		reference = self.var_reference.get()
		if not self.is_selection(reference):
			return
		
		if x is None:
			x = self.var_x.get()
			
		if y is None:
			y = self.var_y.get()
			
		if reference is None:
			reference = self.var_reference.get()
		
		reference = self.reference_command(reference)
		
		self.document.AlignSelection(x, y, reference = reference)

	def reference_command(self, reference):
		if reference == SELECT:
			return 'selection'
		if reference == LOWERMOST:
			return 'lowermost'
		if reference == PAGE:
			return 'page'

	def reset(self):
		self.var_x.set(0)
		self.value_x = 0
		self.var_y.set(0)
		self.value_y = 0
##		self.apply_button_show(not self.var_auto_apply.get())
		self.Update()


instance=AlignPlugin()
app.effects_plugins.append(instance)

