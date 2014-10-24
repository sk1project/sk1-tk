# -*- coding: utf-8 -*-

# Copyright (C) 2010 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in root directory.

import os

global LANG
LANG = 'uk_UA.UTF-8'
os.environ['LANG'] = LANG

import app

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

	from sk1 import main
	app.config.sk_command = sys.argv[0]
	main.main()
