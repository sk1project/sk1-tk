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

import sys, getopt

import app
from uc.utils import Empty

usage = ''"""\
Usage:	sk1 [OPTION] [INPUT FILE]
sk1 command without parameters just launches sK1 with new document.

sK1 is an open source vector graphics editor similar to CorelDRAW(tm), 
Adobe (R) Illustrator(tm), or Adobe (R)Freehand(tm). 
First of all sK1 is oriented for prepress industry.
sK1 Team (http://sk1project.org), copyright (C) 2003-2008 by Igor E. Novikov.

Allowed input formats:
     AI  - Adobe Illustrator files (postscript based)
     CDR - CorelDRAW Graphics files (7-X4 versions)
     CDT - CorelDRAW templates files (7-X4 versions)
     CCX - Corel Compressed Exchange files
     CMX - Corel Presentation Exchange files (CMX1 format)
     SVG - Scalable Vector Graphics files
     FIG - XFig files
     CGM - Computer Graphics Metafile files
     AFF - Draw files
     WMF - Windows Metafile files
     SK  - Sketch/Skencil files
     SK1 - sK1 vector graphics files

Example: sk1 drawing.cdr

sK1 accepts these options:

	-h --help		Print this help message
	-d --display=DISPLAY	Use DISPLAY a X Display
	-g --geometry=WxH+X+Y	The geometry of the main window in standard X fashion
	--run-script=script   Execute the file script after startup
	--version		Print the version number to stdout
"""

version = """\
sK1 %s
Copyright (C) 2003-2008 Igor E. Novikov
sK1 is a Sketch fork
Sketch (C) 1998, 1999, 2000 Bernhard Herzog
Application comes with ABSOLUTELY NO WARRANTY.
You may redistribute copies of sK1
under the terms of the GNU Library General Public License.
For more information about these matters, see the files named COPYRIGHTS.
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

	options = Empty(args=args, display=None, geometry=None, run_script=None)

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

	application = SketchApplication(filename, options.display, options.geometry, run_script=options.run_script)
	app.Issue(None, app.conf.const.APP_INITIALIZED, application)
	application.Run()
	application.SavePreferences()
	application.Refresh()
