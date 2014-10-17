# -*- coding: utf-8 -*-

# Copyright (C) 2003-2008 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from Tkinter import BOTTOM, X, BOTH, LEFT, TOP, E, DISABLED, NORMAL, IntVar

import app
from app import _, config
from app.conf.const import SELECTION

from app.Graphics.blendgroup import SelectStart, SelectEnd

from sk1sdk.libttk import TFrame, TLabel

from sk1.tkext import UpdatedButton
from sk1.ttk_ext import TSpinbox
from sk1.pluginpanels.ppanel import PluginPanel

class BlendPlugin(PluginPanel):

	name = 'Blend'
	title = _("Blend")

	def init(self, master):
		PluginPanel.init(self, master)

		top = TFrame(self.panel, style='FlatFrame', borderwidth=5)
		top.pack(side=TOP, fill=BOTH)

		sign = TFrame(top, style='RoundedFrame', borderwidth=5)
		sign.pack(side=TOP)

		self.sign = TLabel(sign, image='effects_blend')
		self.sign.pack(side=TOP)

		button_frame = TFrame(top, style='FlatFrame')
		button_frame.pack(side=BOTTOM, fill=BOTH, expand=1)

		self.update_buttons = []
		button = UpdatedButton(top, text=_("Apply"),
								command=self.apply_blend,
								sensitivecb=self.doc_can_blend)
		button.pack(in_=button_frame, side=LEFT, expand=1, fill=X)
		self.document.Subscribe(SELECTION, button.Update)
		self.update_buttons.append(button)


		steps_frame = TFrame(top, style='FlatFrame', borderwidth=15)
		steps_frame.pack(side=TOP)
		label = TLabel(steps_frame, text="  " + _("Steps:") + " ")
		label.pack(side=LEFT, anchor=E)

		self.var_steps = IntVar(top)
		self.var_steps.set(config.preferences.blend_panel_default_steps)

		self.entry = TSpinbox(steps_frame, var=10, vartype=0, textvariable=self.var_steps,
									min=1, max=100000, step=1, width=6, command=self.apply_blend)
		self.entry.pack(side=LEFT, anchor=E)


		button = UpdatedButton(top, text=_("Select Start"),
								sensitivecb=self.can_select,
								command=self.select_control,
								args=SelectStart)
		button.pack(side=BOTTOM, fill=X, expand=1, pady=3)
		self.document.Subscribe(SELECTION, button.Update)
		self.update_buttons.append(button)

		button = UpdatedButton(top, text=_("Select End"),
								sensitivecb=self.can_select,
								command=self.select_control,
								args=SelectEnd)
		button.pack(side=BOTTOM, fill=X, expand=1)
		self.document.Subscribe(SELECTION, button.Update)
		self.update_buttons.append(button)

		self.init_from_doc()
		self.subscribe_receivers()

	def subscribe_receivers(self):
		self.document.Subscribe(SELECTION, self.Update)

	def unsubscribe_receivers(self):
		self.document.Unsubscribe(SELECTION, self.Update)

	def doc_can_blend(self):
		return ((self.document.CanBlend() or self.current_obj_is_blend())
				and self.var_steps.get() >= 2)

	def current_obj_is_blend(self):
		object = self.document.CurrentObject()
		return (object is not None
				and (object.is_BlendInterpolation
						or (object.is_Blend and object.NumObjects() == 3)))

	def current_object(self):
		# assume current_obj_is_blend() yields true
		object = self.document.CurrentObject()
		if object.is_Blend:
			# XXX reaching into object.objects is ugly
			object = object.objects[1]
		return object

	def init_from_doc(self):
		for button in self.update_buttons:
			button.Update()
		self.Update()
		self.issue(SELECTION)

	def Update(self):
		if self.current_obj_is_blend():
			steps = self.current_object().Steps()
			self.var_steps.set(steps)
		if self.doc_can_blend():
			self.entry.set_state(NORMAL)
		else:
			self.entry.set_state(DISABLED)

	def apply_blend(self, *args):
		steps = self.var_steps.get()
		if self.current_obj_is_blend() and steps >= 2:
			doc = self.document
			doc.BeginTransaction(_("Set %d Blend Steps") % steps)
			try:
				try:
					doc.AddUndo(self.current_object().SetParameters(steps))
				except:
					doc.AbortTransaction()
			finally:
				doc.EndTransaction()
		else:
			self.document.Blend(steps)

	def can_select(self):
		object = self.document.CurrentObject()
		return (object is not None
				and (object.parent.is_Blend or object.is_Blend))

	def select_control(self, which):
		object = self.document.CurrentObject()
		if object is not None:
			if object.is_Blend:
				# XXX reaching into object.objects is ugly
				if which == SelectStart:
					child = object.objects[0]
				else:
					child = object.objects[-1]
				self.document.SelectObject(child)
			elif object.parent.is_Blend:
				object.parent.SelectControl(object, which)



instance = BlendPlugin()
app.effects_plugins.append(instance)
