# -*- coding: utf-8 -*-

# Copyright (C) 2003-2006 by Igor E. Novikov
# Copyright (C) 1997, 1998 by Bernhard Herzog
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.


from sketchdlg import SketchPanel
from Tkinter import X, BOTH, LEFT, TOP
from Tkinter import Frame, Label
from tkext import UpdatedButton, MyEntry, UpdatedCheckbutton, \
		MyOptionMenu2

from view import SketchView

bitmap_types = [('Portable Pixmap (PPM)', 'ppmraw'),
				('Portable Graymap (PGM)', 'pgmraw'),
				('Portable Bitmap (PBM)', 'pbmraw')]



class ExportPanel(SketchPanel):

	title = 'Export'

	def __init__(self, master, main_window, doc):
		SketchPanel.__init__(self, master, main_window, doc, name = 'export')

	def build_dlg(self):
		top = self.top

		self.view = SketchView(top, self.document, width = 200, height = 200,
								background = 'white')
		self.view.pack(side = LEFT, fill = BOTH, expand = 1)

		self.opt_format = MyOptionMenu2(top, bitmap_types)
		self.opt_format.pack(side = TOP)

		frame = Frame(top)
		frame.pack(side = TOP, expand = 1, fill = X)
		label = Label(frame, text = 'Resolution')
		label.pack(side = LEFT)
		entry = MyEntry(frame, width = 4)
		entry.pack(side = LEFT)
		label = Label(frame, text = 'dpi')
		label.pack(side = LEFT)

		frame = Frame(top)
		frame.pack(side = TOP, expand = 1, fill = X)
		label = Label(frame, text = 'Size')
		label.pack(side = LEFT)
		entry = MyEntry(frame, width = 4)
		entry.pack(side = LEFT)
		label = Label(frame, text = 'x')
		label.pack(side = LEFT)
		entry = MyEntry(frame, width = 4)
		entry.pack(side = LEFT)
		label = Label(frame, text = 'pixel')
		label.pack(side = LEFT)

		check = UpdatedCheckbutton(top, text = 'antialiasing')
		check.pack(side = TOP)

		frame = Frame(top)
		frame.pack(side =TOP)
		button = UpdatedButton(frame, text = 'Export')
		button.pack(side = LEFT)
		button = UpdatedButton(frame, text = 'Close', command = self.close_dlg)
		button.pack(side = LEFT)


	def init_from_doc(self):
		self.view.SetDocument(self.document)




import os


def export_bitmap(document):
	from psdevice import PostScriptDevice
	width, height = document.PageSize()
	width = round(width)
	height = round(height)
	res = 72
	outfile = '/tmp/export.ppm'
	gs_cmd = 'gs -dNOPAUSE -g%(width)dx%(height)d -r%(res)d -sDEVICE=ppmraw '\
				'-sOutputFile=%(outfile)s -q -' % locals()
	#gs_cmd = 'cat > ' + outfile

	if __debug__:
		print gs_cmd
	file = os.popen(gs_cmd, 'w')
	try:
		device = PostScriptDevice(file, as_eps = 0)
		document.Draw(device)
		device.Close()
		file.write('quit\n')
	finally:
		file.close()



