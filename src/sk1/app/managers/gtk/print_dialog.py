# -*- coding: utf-8 -*-

# Copyright (C) 2014 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.


import os, sys, gtk, gtkunixprint

ARGS = {
	'filepath':'',
	'caption':'Print file',
	'window-icon':'',
	}

def process_args():
	for arg in sys.argv:
		res = arg.split('=')
		if len(res) == 2:
			ARGS[res[0]] = res[1]

def print_dialog(filepath):
	dialog = gtkunixprint.PrintUnixDialog()
	dialog.set_position(gtk.WIN_POS_CENTER)
	if ARGS['window-icon'] and os.path.lexists(ARGS['window-icon']):
		dialog.set_icon_from_file(ARGS['window-icon'])
	response = dialog.run()
	if response == gtk.RESPONSE_OK:
		printer = dialog.get_selected_printer()
		printer_name = dialog.get_selected_printer().get_name()
		settings = dialog.get_settings()
		numcopies = settings.get_n_copies()
		collate = ''
		if settings.get_collate(): collate = '-o Collate=True'

		setup = dialog.get_page_setup()
		orientation = ''
		if setup.get_orientation() == gtk.PAGE_ORIENTATION_LANDSCAPE:
			orientation = '-o landscape'
		if not printer.is_virtual():
			os.system('lpr -P "%s" -#%d %s %s %s' % (printer_name,
												numcopies,
												collate,
												orientation,
												filepath))
		else:
			msg = gtk.MessageDialog(dialog, type=gtk.MESSAGE_ERROR,
								buttons=gtk.BUTTONS_OK)
			msg.set_markup("Sorry, virtual printers are not supported!")
			msg.run()
	dialog.destroy()

process_args()
print_dialog(ARGS['filepath'])
