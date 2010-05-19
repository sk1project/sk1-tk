# -*- coding: utf-8 -*-

# Copyright (C) 2003-2006 by Igor E. Novikov
# Copyright (C) 1997, 1998, 2002 by Bernhard Herzog
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

import sys, os, string
import app


def get_sketch_modules():
	# return the sketch specific modules that are already imported.
	# Sketch specific means that the module comes from a file below the
	# sketch directory or that it has a name starting with "Sketch.".
	sketch_dir = app.config.sk_dir
	if sketch_dir[-1] != '/':
		sketch_dir = sketch_dir + '/'
	sketch_dir = os.path.normpath(os.path.abspath(sketch_dir))
	length = len(sketch_dir)
	result = []
	for module in sys.modules.values():
		try:
			mod_file = module.__file__
		except AttributeError:
			continue
		mod_file = os.path.normpath(os.path.abspath(mod_file))
		if mod_file[:length] == sketch_dir or module.__name__[:7] == "app.":
			result.append(module)
	return result



user_functions = {}
def add_sketch_objects(dict):
	from app import main
	from app.events import connector
	# some useful variables and functions
	dict['app'] = main.application
	dict['canv'] = main.application.main_window.canvas
	dict['doc'] = main.application.main_window.document
	dict['connections'] = connector._the_connector.print_connections
	dict['get_sketch_modules'] = get_sketch_modules
	for key, val in user_functions.items():
		dict[key] = val




locals = {}

def PythonPrompt(prompt = '>>>', prompt2 = '...'):
	# try to import readline in Python 1.5
	have_readline = 0
	try:
		import readline
		have_readline = 1
		app.Issue(None, app.conf.const.INIT_READLINE)
	except ImportError:
		pass
	globals = {}
	# put all of app.main and app into the globals
	exec 'from app.main import *' in globals
	exec 'from app import *' in globals
	# put all sketch specific modules into the globals
	for module in get_sketch_modules():
		globals[module.__name__] = module
	add_sketch_objects(globals)
	if have_readline:
		from app.Lib import skcompleter
		skcompleter.install(globals, locals)
	while 1:
		try:
			cmd = raw_input(prompt)
			#cmd = string.strip(cmd)
			if cmd:
				if cmd[-1] == ':':
					# a compound statement
					lines = []
					while string.strip(cmd):
						lines.append(cmd)
						cmd = raw_input(prompt2)
					cmd = string.join(lines + [''], '\n')
					kind = 'exec'
				else:
					kind = 'single'

				c = compile(cmd, '<string>', kind)
				exec c in globals, locals
		except EOFError:
			print '----- returning to app'
			return
		except:
			import traceback
			traceback.print_tb(sys.exc_traceback)
			print 'Exception %s: %s' % (sys.exc_type, sys.exc_value)
