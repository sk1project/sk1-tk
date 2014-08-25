#! /usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2010 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in root directory.

global LANG
LANG = ''

def sk1_run():
	global LANG
	import sys, os, warnings

#	if not os.environ['LANG'] == '':
#		lang = os.environ['LANG'].split('.')
#		LANG = os.environ['LANG']
#		os.environ['LANG'] = lang[0] + lang[1].upper()

	warnings.filterwarnings("ignore")

	_pkgdir = __path__[0]
	sys.path.insert(1, _pkgdir)

	import app
	app.config.sk_command = sys.argv[0]
	app.main.main()
