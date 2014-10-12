# -*- coding: utf-8 -*-

# Copyright (C) 2003-2008 by Igor E. Novikov
# Copyright (C) 1997, 1998, 1999, 2003 by Bernhard Herzog 
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.


from app.events.warn import pdebug

from Tkinter import Toplevel


class ModalDialog:

	title = ''

	class_name = 'ModalDialog'

	old_focus = None
	focus_widget = None
	wait=1
	width=0
	height=0

	def __init__(self, master, **kw):
		self.master = master

		kw['class'] = self.class_name
		top = apply(Toplevel, (master,), kw)
		top.withdraw()
		top.title(self.title)
		top.transient(master)
		top.group(master)
		top.iconname(self.title)
		top.protocol('WM_DELETE_WINDOW', self.close_dlg)

		self.top = top
		self.build_dlg()
		top.update()
		mcx = master.winfo_rootx() + master.winfo_width()/ 2
		mcy = master.winfo_rooty() + master.winfo_height() / 2
#		top.withdraw()
		if self.width==0 and self.height==0:
			width = top.winfo_reqwidth()
			height = top.winfo_reqheight()
		else:
			width = self.width
			height = self.height
		posx = max(min(top.winfo_screenwidth() - width, mcx - width / 2), 0)
		posy = max(min(top.winfo_screenheight() - height, mcy - height / 2), 0)
		top.geometry('%dx%d%+d%+d' % (width, height, posx, posy))
		top.update()
		top.deiconify()

		self.result = None

	if __debug__:
		def __del__(self):
			pdebug('__del__', '__del__', self)

	def build_dlg(self):
		pass
		
	def stub(self):
		pass

	def ok(self, *args):
		self.close_dlg()

	def cancel(self):
		self.close_dlg(None)

	def close_dlg(self, result = None):
		self.result = result
		if self.old_focus is not None:
#			self.old_focus.focus_set()
			self.old_focus = None
		self.top.destroy()

	def RunDialog(self, grab = 1):
		try:
			self.old_focus = self.top.focus_get()
		except KeyError:
			# focus_get fails when the focus widget is a torn-off menu,
			# since there's no corresponding Tkinter object.
			self.old_focus = None
		grab_widget = None
		if grab:
			if not self.top.winfo_ismapped():
				self.top.wait_visibility()
			grab_widget = self.top.grab_current()
			if grab_widget is not None:
				grab_status = grab_widget.grab_status()
			self.top.grab_set()
		if self.focus_widget is not None:
			self.focus_widget.focus_set()
		else:
			self.top.focus_set()
		self.result = None
		if self.wait:
			self.master.wait_window(self.top)
			if grab_widget is not None:
				if grab_status == 'global':
					grab_widget.grab_set_global()
				else:
					grab_widget.grab_set()
			return self.result
		else:
			return