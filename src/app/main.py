# -*- coding: utf-8 -*-

# Copyright (C) 2003-2006 by Igor E. Novikov
# Copyright (C) 1997, 1998, 1999, 2000 by Bernhard Herzog
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

#
# main module
#
# Provides the main() function which reads the user specific
# configuration, creates the application object and enters the
# application's mainloop.
#
# This module also has some global variables:
#
# application
#
#	The application object. This is None until the application
#	object has been created.
#
#	XXX this variable should be in Sketch.__init__
#
#

import sys, getopt, string

import app
from app.utils import os_utils

usage = ''"""\
Usage:	sketch [options] [filename]

sketch accepts these options:

	-h --help		Print this help message
	-d --display=DISPLAY	Use DISPLAY a X Display
	-g --geometry=WxH+X+Y	The geometry of the main window in standard X fashion
	--run-script=script   Execute the file script after startup
	--version		Print the version number to stdout

for compatibility with other X software sketch also accepts geometry
specifications in the standard X format:

	-geometry WxH+X+Y

"""

version = """\
Sketch %s
Copyright (C) 1998, 1999, 2000 Bernhard Herzog
Sketch comes with ABSOLUTELY NO WARRANTY.
You may redistribute copies of Sketch
under the terms of the GNU Library General Public License.
For more information about these matters, see the files named COPYING.
"""

def process_args(args):
	# Read options from the command line. Return an instance object with the
	# instance variables:
	#	display		name of the X-display or None
	#	geometry	geometry of the main window or None
	#	args		rest of the arguments after the last option
	#
	# To behave more like other X-programs, sketch should accept the options
	# -display and -geometry with a single hyphen and no `='...

	# recognize a standard X geometry specification... (hack)
	if '-geometry' in args:
		try:
			idx = args.index('-geometry')
			geo = args[idx:idx + 2]
			if len(geo) == 2:
				del args[idx:idx + 2]
				geo[0] = '-g'
				args[0:0] = geo
		except:
			pass

	opts, args = getopt.getopt(args, 'd:g:hi', ['display=', 'geometry=', 'help', 'run-script=', 'version'])
	# the option -i is a hack to allow sketch to be used as a `python
	# interpreter' in the python shell in python-mode.el

	options = os_utils.Empty(args = args, display = None, geometry = None, run_script = None)

	for optchar, value in opts:
		if optchar == '-d' or optchar == '--display':
			options.display = value
		elif optchar == '-g' or optchar == '--geometry':
			options.geometry = value
		elif optchar == '--run-script':
			options.run_script = value
		elif optchar == '-h' or optchar == '--help':
			print app._(usage)
			sys.exit(0)
		elif optchar == '--version':
			print app._(version) % app.sKVersion
			sys.exit(0)

	return options


#
#	Global Variables
#

application = None

#
#
#

def main():
	global application

	try:
		options = process_args(sys.argv[1:])
	except getopt.error:
		sys.stderr.write(app._(usage))
		sys.exit(1)

	if options.args:
		filename = options.args[0]
	else:
		filename = ''

	app.init_ui()

	from skapp import SketchApplication

	application = SketchApplication(filename, options.display, options.geometry, run_script = options.run_script)
	app.Issue(None, app.conf.const.APP_INITIALIZED, application)
	application.Run()
	application.SavePreferences()
	application.Refresh()
