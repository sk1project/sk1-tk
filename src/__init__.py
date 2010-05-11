#! /usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2010 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in root directory.

def sk1_run():
	import sys, os, warnings
	
	warnings.filterwarnings("ignore")
	
	_pkgdir = __path__[0]
	sys.path.insert(1, _pkgdir)
	
	import app
	app.config.sk_command = sys.argv[0]
#	print "MAIN"
	app.main.main()
