# -*- coding: utf-8 -*-

# Copyright (C) 2014 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.


import os, sys, gtk

ARGS = {
	'start_dir':'~',
	'caption':'Open file',
	'filetypes':'',
	'window-icon':'',
	}

def process_args():
	for arg in sys.argv:
		res = arg.split('=')
		if len(res) == 2:
			ARGS[res[0]] = res[1]

def expanduser_unicode(path):
	path = os.path.expanduser(path.encode(sys.getfilesystemencoding()))
	return path.decode(sys.getfilesystemencoding())

def _get_open_fiters():
	result = []
	typelist = ARGS['filetypes'].split('@')
	for item in typelist:
		item = item.strip()
		if item:
			descr, extensions = item.split('|')
			extensions = extensions.split()
			file_filter = gtk.FileFilter()
			file_filter.set_name(descr)
			for ext in extensions:
				file_filter.add_pattern(ext)
				file_filter.add_pattern(ext.upper())
			result.append(file_filter)
	return result

def get_open_file_name(start_dir='~'):
	result = ''
	caption = ARGS['caption']
	dialog = gtk.FileChooserDialog(caption,
				None,
				gtk.FILE_CHOOSER_ACTION_OPEN,
				(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
				gtk.STOCK_OPEN, gtk.RESPONSE_OK))

	dialog.set_default_response(gtk.RESPONSE_OK)
	start_dir = expanduser_unicode(start_dir)
	dialog.set_current_folder(start_dir)
	dialog.set_show_hidden(False)
	dialog.set_position(gtk.WIN_POS_CENTER)
	if ARGS['window-icon'] and os.path.lexists(ARGS['window-icon']):
		dialog.set_icon_from_file(ARGS['window-icon'])

	for file_filter in _get_open_fiters():
		dialog.add_filter(file_filter)

	ret = dialog.run()
	if ret == gtk.RESPONSE_OK:
		result = dialog.get_filename()
	dialog.destroy()
	if result is None: result = ''
	return result

process_args()
print get_open_file_name(ARGS['start_dir'])
