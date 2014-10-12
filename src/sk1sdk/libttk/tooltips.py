# -*- coding: utf-8 -*-

# Copyright (C) 2003-2008 by Igor E. Novikov
# Copyright (C) 1997, 1998, 1999 by Bernhard Herzog
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

#
# Balloon help mechanism for Python/Tk
#

from types import InstanceType
from Tkinter import Toplevel
from sk1sdk.libttk import TLabel


class Tooltips:
	tooltip_delay = 100

	def __init__(self):
		self.descriptions = {}
		self.balloon = None
		self.balloon_label = None
		self.last_widget = ''
		self.after_id = None
		self.root = None

	def AddDescription(self, widget, description):
		self.descriptions[widget._w] = description
		if widget._w == self.last_widget:
			self.balloon_label['text'] = description

	def RemoveDescription(self, widget):
		if type(widget) == InstanceType:
			widget = widget._w
		if self.descriptions.has_key(widget):
			del self.descriptions[widget]

	def GetDescription(self, widget):
		if type(widget) == InstanceType:
			widget = widget._w
		if self.descriptions.has_key(widget):
			return self.descriptions[widget]
		return ''


	def create_balloon(self, root):
		self.root = root
		self.balloon = Toplevel(self.root)
		self.balloon.withdraw()
		self.balloon.overrideredirect(1)
		self.balloon["relief"] = 'flat'
		label = TLabel(self.balloon, text='Tooltip', style='Tooltips')
		label.pack(ipadx=2, ipady=2)
		self.balloon_label = label


	def popup_balloon(self, widget_name, x, y, text):
		self.last_widget = widget_name
		self.balloon.withdraw()
		self.balloon_label['text'] = text

		width = self.balloon_label.winfo_reqwidth()
		height = self.balloon_label.winfo_reqheight()

		screenwidth = self.root.winfo_screenwidth()
		screenheight = self.root.winfo_screenheight()

		x = self.root.winfo_pointerx()
		y = self.root.winfo_pointery() + 20

		if screenwidth < (x + width):
			x = x - width

		if screenheight < (y + height):
			y = y - height - 25

		self.balloon.geometry('%+d%+d' % (x, y))
		self.balloon.update()
		self.balloon.deiconify()
		self.balloon.tkraise()

	def popup_delayed(self, widget_name, x, y, text, *args):
		self.after_id = None
		self.popup_balloon(widget_name, x, y, text)

	def enter_widget(self, event):
		widget_name = event.widget
		text = self.GetDescription(widget_name)
		if text:
			x = event.x;y = event.y
			if self.after_id:
				print 'after_id in enter'
				self.root.after_cancel(self.after_id)
			self.after_id = self.root.after(self.tooltip_delay, self.popup_delayed, widget_name, x, y, text)

	def leave_widget(self, event):
		global last_widget, after_id
		if self.after_id is not None:
			self.root.after_cancel(self.after_id)
			self.after_id = None
			self.last_widget = ''
		last_widget = ''
		self.balloon.withdraw()

	button_press = leave_widget


	def destroy_widget(self, event):
		self.RemoveDescription(event.widget)


_tooltips = Tooltips()
AddDescription = _tooltips.AddDescription


def Init(root, tooltip_delay=100, activate_tooltips=1):
	if activate_tooltips:
		root.bind_all('<Enter>', _tooltips.enter_widget)
		root.bind_all('<Leave>', _tooltips.leave_widget)
		root.bind_all('<ButtonPress>', _tooltips.button_press)
		_tooltips.tooltip_delay = tooltip_delay
		_tooltips.create_balloon(root)
