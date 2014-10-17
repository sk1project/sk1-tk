# -*- coding: utf-8 -*-

# Copyright (C) 2014 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from app import _
import app, os
from dialog import ModalDialog
from msgdialog import msgDialog

from Tkinter import TOP, BOTH, X, LEFT, BOTTOM, RIGHT, Y
from Tkinter import Label, Frame, Canvas
from sk1sdk.libttk import TButton, TLabel, TFrame

ACTION_SAVE = _('Save')
ACTION_OPEN = _('Open')
ACTION_OPEN = _('Import')
ACTION_OPEN = _('Export')

PLACE_HOME = 'PLACE_HOME'
DESKTOP_DIR = 'XDG_DESKTOP_DIR'
DOCUMENTS_DIR = 'XDG_DOCUMENTS_DIR'
PICTURES_DIR = 'XDG_PICTURES_DIR'
DOWNLOAD_DIR = 'XDG_DOWNLOAD_DIR'
TEMPLATES_DIR = 'XDG_TEMPLATES_DIR'

PLACES_DICT = {
PLACE_HOME:['fd-user-home', _('Home'), ''],
DESKTOP_DIR:['fd-user-desktop', _('Desktop'), ''],
DOCUMENTS_DIR:['fd-documents', _('Documents'), ''],
PICTURES_DIR:['fd-user-home', _('Pictures'), ''],
DOWNLOAD_DIR:['fd-downloads', _('Downloads'), ''],
TEMPLATES_DIR:['fd-user-home', _('Templates'), ''],
}
PLACES = [PLACE_HOME, DESKTOP_DIR, DOCUMENTS_DIR,
	PICTURES_DIR, DOWNLOAD_DIR, TEMPLATES_DIR]

PLACES_FLAG = []

def update_places():
	if PLACES_FLAG:return
	home_path = os.path.expanduser('~')
	PLACES_DICT[PLACE_HOME][2] = '' + home_path
	path = os.path.join(home_path, '.config', 'user-dirs.dirs')
	if os.path.lexists(path):
		data_file = open(path, 'rb')
		while 1:
			line = data_file.readline()
			if line == '': break
			line = line.strip()
			if line[-1:] == '\n': line = line[:-1]
			if line:
				parts = line.split('#')
				if not parts[0]:continue
				parts = parts[0].split('=')
				place = parts[0]
				if PLACES_DICT.has_key(place):
					path = parts[1].replace('"', '')
					path = path.replace('$HOME', home_path)
					PLACES_DICT[place][2] = path
			else: continue
		data_file.close()
	PLACES_FLAG.append(True)

class BrdFrame(Frame):

	top = None

	def __init__(self, master, clr=None, **kw):
		apply(Frame.__init__, (self, master), kw)
		self['background'] = 'gray'
		self['borderwidth'] = 1
		self['relief'] = 'flat'
		self.top = Frame(self, relief='flat')
		self.top.pack(side=TOP, fill=BOTH, expand=1)
		if clr: self.top['background'] = clr


class SK1FileDialog(ModalDialog):

	class_name = 'SK1FileDialog'

	def __init__(self, master, dlgname='__dialog__'):
		self.master = master
		self.title = _("Open")
		self.init_vars()
		ModalDialog.__init__(self, master, name=dlgname)

	def init_vars(self):
		self.width = 700
		self.height = 430
		update_places()

	def build_dlg(self):

		parent = TFrame(self.top, style='FlatFrame', borderwidth=10)
		parent.pack(side=TOP, fill=BOTH, expand=1)

		bwpanel = BrowsePanel(parent, self, style='FlatFrame')
		bwpanel.pack(side=TOP, fill=X, expand=0)

		Frame(parent, relief='flat', height=5).pack(side=TOP, fill=X, expand=0)

		cmdpanel = CommandPanel(parent, self, style='FlatFrame')
		cmdpanel.pack(side=BOTTOM, fill=X, expand=0)

		Frame(parent, relief='flat', height=5).pack(side=BOTTOM, fill=X, expand=0)

		places = PlacesPanel(parent, self, borderwidth=3)
		places.pack(side=LEFT, fill=Y, expand=0)

		Frame(parent, relief='flat', width=5).pack(side=LEFT, fill=Y, expand=0)

		filepnl = FilePanel(parent, self, clr='white')
		filepnl.pack(side=TOP, fill=BOTH, expand=1)

		self.top.bind('<Escape>', self.cancel)
		self.top.protocol('WM_DELETE_WINDOW', self.cancel)

	def ok(self, *args):
		self.close_dlg(None)

	def cancel(self, *args):
		self.close_dlg(None)

class CommandPanel(TFrame):

	def __init__(self, master, dialog, **kw):
		self.dialog = dialog
		apply(TFrame.__init__, (self, master), kw)

		cancel_bt = TButton(self, text=_("Cancel"), command=self.dialog.cancel)
		cancel_bt.pack(side=RIGHT)

		ok_bt = TButton(self, text=_("OK"), command=self.dialog.ok)
		ok_bt.pack(side=RIGHT, padx=5)

class BrowsePanel(TFrame):

	def __init__(self, master, dialog, **kw):
		apply(TFrame.__init__, (self, master), kw)
		self.prev_btn = TButton(self, image='fd-go-previous', style="Toolbutton")
		self.prev_btn.pack(side=LEFT)
		self.up_btn = TButton(self, image='fd-go-up', style="Toolbutton")
		self.up_btn.pack(side=LEFT)
		self.next_btn = TButton(self, image='fd-go-next', style="Toolbutton")
		self.next_btn.pack(side=LEFT)

class PlaceItem(Frame):

	def __init__(self, master, item=PLACE_HOME, **kw):
		apply(Frame.__init__, (self, master), kw)
		self.item = item
		self['borderwidth'] = 3
		self['relief'] = 'flat'
		self.bg_color = self['background']
		self.bind('<Button-1>', self.callback)
		self.bind('<Enter>', self.mouse_enter)
		self.bind('<Leave>', self.mouse_leave)

		self.icon = Label(self, image=PLACES_DICT[item][0])
		self.icon.pack(side=LEFT)
		self.icon.bind('<Button-1>', self.callback)
		self.icon.bind('<Enter>', self.mouse_enter)
		self.icon.bind('<Leave>', self.mouse_leave)

		self.text = Label(self, text=PLACES_DICT[item][1])
		self.text.pack(side=LEFT, padx=5)
		self.text.bind('<Button-1>', self.callback)
		self.text.bind('<Enter>', self.mouse_enter)
		self.text.bind('<Leave>', self.mouse_leave)

	def callback(self, *args):
		print PLACES_DICT[self.item][2]

	def mouse_enter(self, *args):
		self['background'] = 'gray'
		self.text['background'] = 'gray'
		self.icon['background'] = 'gray'

	def mouse_leave(self, *args):
		self['background'] = self.bg_color
		self.text['background'] = self.bg_color
		self.icon['background'] = self.bg_color

class PlacesPanel(BrdFrame):

	def __init__(self, master, dialog, clr=None, **kw):
		apply(BrdFrame.__init__, (self, master, clr), kw)

		for item in PLACES:
			if PLACES_DICT[item][2]:
				lbl = PlaceItem(self.top, item)
				lbl.pack(side=TOP, fill=X)

class FilePanel(BrdFrame):

	def __init__(self, master, dialog, clr=None, **kw):
		apply(BrdFrame.__init__, (self, master, clr), kw)
		self.viewer = FileViewer(self.top)
		self.viewer.pack(side=TOP, fill=BOTH, expand=1)

class FileViewer(Canvas):

	icon_size = 22

	def __init__(self, master, path='/home', **kw):
		apply(Canvas.__init__, (self, master), kw)
		self['background'] = 'white'
		self.browse()

	def browse(self, path='/'):
		self.create_image((5, 15), anchor='w', image='mime_folder_22')
		self.create_text((30, 15), anchor='w', text='mime_folder_22')

def get_file_dlg(master):
	dlg = SK1FileDialog(master)
	dlg.RunDialog()
	return dlg.result
