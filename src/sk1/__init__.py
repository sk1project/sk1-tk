# -*- coding: utf-8 -*-

# Copyright (C) 2010 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in root directory.

import os

LANG = os.environ['LANG']

import app

def dummy_translator(text):
	return text

_ = dummy_translator

def sk1_run():
	import sys, warnings

	warnings.filterwarnings("ignore")

	from sk1 import main
	app.config.sk_command = sys.argv[0]
	main.main()
