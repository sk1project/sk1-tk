# -*- coding: utf-8 -*-

# Copyright (C) 2006 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

import os, sys, app
from xml.sax import handler

from app.events import connector
from const import CHANGED
from uc.utils.fs import gethome
from app import Point, PointType

class Configurator:
	"""Configuration class configs sK1 and loads preferences at start up."""
	def __init__(self, master=None, base_dir='~', cnf={}, **kw):

		self.name = 'sK1'
		self.sk_command = 'sk1'
		self.version = '0.9.3'

		self.sk_dir = base_dir
		self.sk1_dir = os.path.join(self.sk_dir, 'sk1')
		self.sk1sdk_dir = os.path.join(self.sk_dir, 'sk1sdk')
		self.sk_share_dir = os.path.join(self.sk1_dir, 'share')
		self.sk_palettes = os.path.join(self.sk_share_dir, 'palettes')
		self.sk_ps = os.path.join(self.sk_share_dir, 'ps_templates')

		self.user_home_dir = gethome()
		ucd = '%s-tk-%s' % (self.sk_command, self.version)
		self.user_config_dir = os.path.join(self.user_home_dir, '.config', ucd)
		ucd = self.user_config_dir
		self.user_palettes = os.path.join(ucd, 'palettes')
		self.user_themes = os.path.join(ucd, 'themes')
		self.user_icc = os.path.join(ucd, 'icc')
		self.user_fonts = os.path.join(ucd, 'fonts')
		self.user_plugins = os.path.join(ucd, 'plugins')
		self.user_color_themes = os.path.join(ucd, 'color_themes')
		self.user_icons = os.path.join(ucd, 'icons')

		# Directories where sK1 searches for plugins.
		# The expanded plugin_dir is appended to this
		self.plugin_path = []

		self.user_preferences_file = os.path.join(ucd, 'preferences.xml')

		#============USER CONFIG==================='
		self.check_user_config()
		if os.path.isfile(self.user_preferences_file):
			prefs = Preferences()
			prefs.load(self.user_preferences_file)
			if prefs.sk1_version == self.version:
				self.preferences = prefs
			else:
				self.preferences = Preferences()
				self.preferences.sk1_version = self.version
		else:
			self.preferences = Preferences()
			self.preferences.sk1_version = self.version

		#===============DEPRECATED VARIABLES===============
		self.std_res_dir = os.path.join(self.sk1_dir, 'share/resources')
		# Subdirectory for the pixmaps. On startup it is expanded
		# to an absolute pathname.
		self.pixmap_dir = os.path.join(self.sk1_dir, 'share/resources')
		# PostScript Prolog file
		self.postscript_prolog = os.path.join(self.sk_ps, 'sk1-proc.ps')
		#============================================

	def save_user_preferences(self):
		self.preferences.save(self.user_preferences_file)

	def get_preference(self, key, default):
		if hasattr(self.preferences, key):
			return getattr(self.preferences, key)
		return default

	def add_mru_file(self, filename):
		if not filename:
			return
		mru_list = self.preferences.mru_files
		if filename in mru_list:
			mru_list.remove(filename)
		mru_list.insert(0, filename)
		self.preferences.mru_files = mru_list[:4]

	def remove_mru_file(self, filename):
		if not filename:
			return
		mru_list = self.preferences.mru_files
		if filename in mru_list:
			mru_list.remove(filename)
			if len(mru_list) < 4:
				mru_list = mru_list + ['', '', '', '']
			self.preferences.mru_files = mru_list[:4]

	def check_user_config(self):
		if not os.path.isdir(self.user_config_dir):
			try:
				os.mkdir(self.user_config_dir, 0777)
			except (IOError, os.error), value:
				sys.stderr('Cannot write preferences into %s.' % user_config_dir)
				sys.exit(1)
		dirs = [
			self.user_palettes,
			self.user_themes,
			self.user_fonts,
			self.user_plugins,
			self.user_color_themes,
			self.user_icons,
			]

		for item in dirs:
			self.check_config_subdir(item)

	def check_config_subdir(self, path):
		if os.path.islink(path) or os.path.isfile(path):
			os.rename(path, '%s~' % path)
		if not os.path.isdir(path):
			os.mkdir(path, 0777)



class Preferences(connector.Publisher):

	def __setattr__(self, attr, value):
		if not hasattr(self, attr) or getattr(self, attr) != value:
			self.__dict__[attr] = value
			self.issue(CHANGED, attr, value)
			if not app.mw is None:
				app.mw.issue(CHANGED)

	def load(self, filename=None):
		import xml.sax
		from xml.sax.xmlreader import InputSource

		content_handler = XMLPrefReader(pref=self)
		error_handler = ErrorHandler()
		entity_resolver = EntityResolver()
		dtd_handler = DTDHandler()
		try:
			input_file = open(filename, "r")
			input_source = InputSource()
			input_source.setByteStream(input_file)
			xml_reader = xml.sax.make_parser()
			xml_reader.setContentHandler(content_handler)
			xml_reader.setErrorHandler(error_handler)
			xml_reader.setEntityResolver(entity_resolver)
			xml_reader.setDTDHandler(dtd_handler)
			xml_reader.parse(input_source)
			input_file.close
		except:
			pass

	def save(self, filename=None):
		if len(self.__dict__) == 0 or filename == None:
			return
		from xml.sax.saxutils import XMLGenerator

		try:
			fileptr = open(filename, 'w')
		except (IOError, os.error), value:
			sys.stderr('cannot write preferences into %s: %s' % (`filename`, value[1]))
			return

		writer = XMLGenerator(out=fileptr, encoding=self.system_encoding)
		writer.startDocument()
		defaults = Preferences.__dict__
		items = self.__dict__.items()
		items.sort()
		writer.startElement('preferences', {})
		writer.characters('\n')
		for key, value in items:
			if defaults.has_key(key) and defaults[key] == value:
				continue
			writer.characters('	')
			writer.startElement('%s' % key, {})
			if type(value) == PointType:
				to_write = '(%g, %g)' % tuple(value)
				writer.characters('Point%s' % to_write)
			else:
				writer.characters('%s' % `value`)
			writer.endElement('%s' % key)
			writer.characters('\n')
		writer.endElement('preferences')
		writer.endDocument()
		fileptr.close

	#============== sK1 PREFERENCES ===================
	sk1_version = ''
	#How many undo steps sketch remembers. None means unlimited.
	undo_limit = None
	#Default encoding for sK1 (GUI uses utf-8 only)
	system_encoding = 'utf-8'

	#============== NEW DOCUMENT PREFERENCES ===================
	#The initial grid geometry for a new document. It must be a tuple of the
	#form (ORIG_X, ORIG_Y, WIDTH_X, WIDTH_Y). WIDTH_X and WIDTH_Y are
	#the horizontal and the vertical distance between points of the grid,
	#(ORIG_X, ORIG_X) is one point of the grid.
	#These coordinates are given in Point
	grid_geometry = (0, 0, 2.83465, 2.83465)

	#If the grid should be visible in a new document,
	#set grid_visible to a true value
	grid_visible = 0

	#Grid style: 0 - dotted; 1- lines
	grid_style = 1

	#The grid color of a new document as a tuple of RGB values in
	#the range 0..1. E.g. (0, 0, 1) for blue
	#grid_color = ('RGB', 0, 0, 1)
	grid_color = ('RGB', 0.0, 0.0, 1.0)
	grid_line_transparency = 0.15
	gridlayer_color = (0.0, 0.0, 1.0, 0.15)

	#The outline color of a new GuideLayer as a tuple of RGB values in
	#the range 0..1. E.g. (0, 0, 1) for blue
	guide_color = ('RGB', 0, 0.3, 1)
	guideline_color = (0.0, 0.3, 1.0, 1.0)
	horizontal_guide_shape = [5, 7]
	vertical_guide_shape = [5, 8]

	layer_color = ('RGB', 0.196, 0.314, 0.635)

	#Default paper format for new documents and documents read from a files
	#that don't specify a paper format. This should be one of the formats
	#defined in papersize.py.
	default_paper_format = 'A4'

	#Default page orientation. Portrait = 0, Landscape = 1.
	#Other values are silently ignored.
	default_page_orientation = 0

	#----------Document font managment-------------
	# The PS name of the font used for new text-objects
	default_font = 'Arial'

	system_font_dir = '/usr/share/fonts'

	# should be expanded to absolute path
	#If the font file for a font can't be found or if a requested font
	#is not known at all, the fallback_font is used (PS name here):
	user_font_dir = '.fonts'

	fallback_font = 'BitstreamVeraSans-Roman'

	#============== CANVAS PREFERENCES ===================

	#When objects are duplicated, the new copies are translated by
	#duplicate_offset, given in document coordinates
	duplicate_offset = (10, 10)

	#The default unit used in various places.
	#Supported values: 'pt', 'in', 'cm', 'mm'
	default_unit = 'mm'
	default_unit_jump = 0.1

	#Type of coordinate system:
	# 0 - left down corner of page
	# 1 - left upper corner of page
	# 2 - center of page
	coord_system = 0

	poslabel_sets_default_unit = 1

	#How many steps to draw in a gradient pattern
	gradient_steps_editor = 100
	gradient_steps_print = 50

	#If the text on the screen becomes smaller than greek_threshold,
	#don't render a font, but draw little lines instead.
	#XXX see comments in graphics.py
	greek_threshold = 5

	#When snapping is active, coordinates specified with the mouse are
	#snapped to the nearest `special' point (e.g. a grid point)
	#if that is nearer than max_snap_distance pixels.
	#(Thus, this length is given in window (pixel-) coordinates).
	max_snap_distance = 30

	#If true and snapping is active, the current position displayed in
	#the status bar is the position the mouse position would be snapped to.
	snap_current_pos = 1

	#If true, change the cursor when above a selected object or a guide line
	active_cursor = 1

	viewport_ring_length = 10

	#---------Color managment---------
	user_rgb_profile = 0
	user_cmyk_profile = 0
	user_monitor_profile = 0

	printer_intent = 0
	monitor_intent = 0

	use_cms = 1
	use_cms_for_bitmap = 1
	simulate_printer = 0

	# 0 - use RGB, 1 - use CMYK
	color_blending_rule = 1

	#==========CAIRO DATA SECTION============
	cairo_enabled = 1
	alpha_channel_enabled = 1
	bitmap_alpha_channel_enabled = 1
	cairo_tolerance = .1
	cairo_antialias = 0
	cairo_bitmap_filter = 0

	#==========PRINTING SECTION============
	print_command = ''
	pdf_level = '1.5'

	#============== UI PREFERENCES ===================

	window_title_template = '%(appname)s - [%(docname)s]'

	#Defines splashscreen appearance
	show_splash = 1

	#Icons
	color_icons = 1

	#Use Tooltips.
	activate_tooltips = 1

	#Delay for tooltips in milliseconds
	tooltip_delay = 500

	#---------UI managment---------
	style = 'Plastik'
	color_theme = 'built-in'
	icons = 'CrystalSVG'

	#---------UI fonts---------
	small_font = 'Tahoma 8'
	normal_font = 'Tahoma 9'
	large_font = 'Tahoma 10 bold'
	fixed_font = 'CourierNew 9'

	#Decreases UI font size to compensate difference between GNOME and Tk
	correct_font = 1

	#---------Ruler data---------
	ruler_min_tick_step = 4
	ruler_min_text_step = 33
	ruler_max_text_step = 100

	ruler_text_color = 'black'
	ruler_tick_color = 'black'
	ruler_color = '#F9F9FC'#Rulers background color

	#============== APPLICATION PREFERENCES ===================

	#List of most recently used files.
	mru_files = ['', '', '', '', '']

	#The standard palette. If this is a relative pathname it is
	#interpreted relative to std_res_dir.
	palette = ''
	builtin_palette = 'cmyk_std.skp'
	arrows = 'standard.arrow'
	dashes = 'standard.dashes'
	pattern = 'pattern.ppm'

	pattern_dir = ''
	image_dir = ''

	# whether the apply button in the property dialogs sets the default
	#properties for new objects. (   1 - do it, but ask; 0 - don't)
	set_default_properties = 1

	#Font dialog sample text. Can be changed by simply editing it in the font dialog.
	sample_text = 'Text'

	#TODO: Should be merged with show_page_outline!
	draw_page_border = 1
	page_border_size = 5

	#Screen resolution in pixel per point. Used by the canvas to convert
	#document coordinates to screen coordinates for a zoom factor of 100%
	#None means to compute it from information obtained from the X-Server
	#(ScreenWidth and ScreenMMWidth). 1.0 means 72 pixels per inch.
	screen_resolution = 1.0

	#If true, switch to selection mode after drawing an object.
	#Stay in creation mode otherwise.
	creation_is_temporary = 0

	# ms, 0 disables auto scrolling
	autoscroll_interval = 1

	# no. of scroll units
	autoscroll_amount = .5

	#Ask user for confirmation if the memory size of an image is larger than
	#huge_image_size (measured in bytes) (unused at the moment)
	huge_image_size = 1 << 20

	#Default resolution in pixels/inch for a new raster image that doesn't
	#specify it itself. (not implemented yet)
	default_image_resolution = 72

	#The resoulution in pixel/inch of the preview image sK1 renders for preview.
	#(using gs). Leave this at 72 for now.
	eps_preview_resolution = 72

	#Whether to print internal warning messages. Useful for debugging.
	print_internal_warnings = 0

	#print additional messages. these are usually only interesting for
	#development purposes.
	print_debug_messages = 0

	#Howto report warnings to the user:
	#   'dialog'	popup a dialog box;
	#   'stderr'	write the message to stderr
	warn_method = 'dialog'

	#whether to show the special menu. The special menu contains some commands
	#that provide access to sketch internals and new, experimental features.
	show_special_menu = 0

	#whether to show advanced snapping options.
	show_advanced_snap_commands = 0

	#If true, use the saved coordinates when opening a panel
	panel_use_coordinates = 1

	#If true, try to compensate for the coordinate changes the window manager
	#introduces by reparenting.
	panel_correct_wm = 1

	blend_panel_default_steps = 10
	print_destination = 'printer'#	Default print destination. 'file' for file, 'printer' for printer

	menu_tearoff_fix = 1#	Menus
	drawing_precision = 3

	#---------Open/save dialogs managment----
	dir_for_open = '~'
	dir_for_save = '~'
	dir_for_vector_import = '~'
	dir_for_vector_export = '~'
	dir_for_bitmap_import = '~'
	dir_for_bitmap_export = '~'
	dir_for_palettes = '~'
	#------------------------------------

	color_cube = (6, 6, 6, 20)#	For PseudoColor displays.
	reduce_color_flashing = 1

	#	Screen Gamma. (leave this at 1.0 for now)
	#screen_gamma = 1.0


	#
	#	Bezier Objects
	#

	#Whether the first click-drag-release in the PolyLine creator
	#defines the start and end of the first line segment or just the
	#start point.
	polyline_create_line_with_first_cklick = 1
	topmost_is_mask = 1#	Mask Group

	#How to insert from clipboard:
	#	0 - on the same place;
	#	1 - as a floating insertion
	insertion_mode = 0

	#How to insert imported graphics:
	#	0 - on the same place;
	#	1 - as a floating insertion
	import_insertion_mode = 0

	#If true, try to unload some of the import filter modules after
	#use. Only filters marked as unloadable in their config file are
	#affected.
	unload_import_filters = 1

	#Handle jump to manipulate objects by keyboard arrows (mm)
	handle_jump = 1

	#The line width for the outlines during a drag.
	editor_line_width = 1


class XMLPrefReader(handler.ContentHandler):
	"""Handler for xml file reading"""
	def __init__(self, pref=None):
		self.key = None
		self.value = None
		self.pref = pref

	def startElement(self, name, attrs):
		self.key = name

	def endElement(self, name):
		if name != 'preferences':
			code = compile('self.value=' + self.value, '<string>', 'exec')
			exec code
			self.pref.__dict__[self.key] = self.value

	def characters(self, data):
		self.value = data

class ErrorHandler(handler.ErrorHandler): pass
class EntityResolver(handler.EntityResolver): pass
class DTDHandler(handler.DTDHandler): pass








