# -*- coding: utf-8 -*-

# Copyright (C) 2010 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in root directory.

import os

from sk1.app_conf import get_app_config, AppData

global LANG, config

LANG = ''
config = None

def dummy_translator(text):
	return text

_ = dummy_translator

def sk1_run():
	global LANG
	import sys, warnings

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

def sk1_2_run():

	"""sK1 application launch routine."""

	global config

	_pkgdir = __path__[0]
	config = get_app_config(_pkgdir)
	appdata = AppData()
	config.load(appdata.app_config)
	config.resource_dir = os.path.join(_pkgdir, 'share')

	from sk1.application import SK1_Application
	application = SK1_Application(appdata)
	application.run()
