# Sketch - A Python-based interactive drawing program
# Copyright (C) 1997, 1998, 1999, 2000 by Bernhard Herzog
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

#
#       Font management...
#

import os, re, operator
from string import split, strip, atoi, atof, lower, translate, maketrans


import streamfilter, ft2

from app.Graphics.plugobj import TrafoPlugin
from app.Graphics.bezier import PolyBezier
from app.Graphics.pattern import SolidPattern

from app import _, config, Point, TrafoType, Scale, SketchError, \
		SketchInternalError, Subscribe, CreatePath, CreateFontMetric, SKCache

from app import Scale, CreatePath, Point, ContAngle, ContSmooth, \
     EmptyLineStyle, StandardColors
		
from app.conf import const
from app.Lib import encoding


from app.events.warn import warn, INTERNAL, USER, pdebug
from app.utils.os_utils import find_in_path, find_files_in_path, get_files_tree, gethome

minus_tilde = maketrans('-', '~')

def xlfd_matrix(trafo):
	mat = '[%f %f %f %f]' % trafo.matrix()
	return translate(mat, minus_tilde)


def _str(val):
	return strip(val)

def _bb(val):
	return tuple(map(int, map(round, map(atof, split(strip(val))))))

def _number(val):
	return int(round(atof(val)))

converters = {
	'EncodingScheme':       _str,
	'Ascender':             _number,
	'Descender':    _number,
	'ItalicAngle':  atof,
	'FontBBox':             _bb,
	'StartCharMetrics':     None,
	'EndFontMetrics':       None
}

StandardEncoding = 'AdobeStandardEncoding'

def read_char_metrics(afm):
	# read the individual char metrics. Assumes that each line contains
	# the keys C, W, N and B. Of these keys, only C (or CH, but that's
	# not implemented here) is really required by the AFM specification.
	charmetrics = {encoding.notdef: (0, 0,0,0,0)}
	font_encoding = [encoding.notdef] * 256
	while 1:
		line = afm.readline()
		if line == 'EndCharMetrics\n':
			break
		items = filter(None, map(strip, split(line, ';')))
		if not items:
			continue
		code = name = width = bbox = None
		for item in items:
			[key, value] = split(item, None, 1)
			if key == 'C':
				code = atoi(value)
			elif key == 'WX':
				width = int(round(atof(value)))
			elif key == 'N':
				name = value
			elif key == 'B':
				bbox = tuple(map(int,map(round,map(atof,split(value)))))
		charmetrics[name] = (width,) + bbox
		font_encoding[code] = name
	return charmetrics, font_encoding

def read_afm_file(filename):
	afm = streamfilter.LineDecode(open(filename, 'r'))

	attribs = {'ItalicAngle': 0.0}
	charmetrics = None
	font_encoding = [encoding.notdef] * 256

	while 1:
		line = afm.readline()
		if not line:
			break
		try:
			[key, value] = split(line, None, 1)
		except ValueError:
			# this normally means that a line contained only a keyword
			# but no value or that the line was empty
			continue
		try:
			action = converters[key]
		except KeyError:
			continue
		if action:
			attribs[key] = action(value)
		elif key == 'StartCharMetrics':
			charmetrics, font_encoding = read_char_metrics(afm)
			break
		else:
			# EndFontMetrics
			break

	if not charmetrics:
		raise ValueError, \
				'AFM files without individual char metrics not yet supported.'

	if attribs.get('EncodingScheme', StandardEncoding) == StandardEncoding:
		enc = encoding.iso_latin_1
	else:
		enc = font_encoding

	try:
		rescharmetrics = map(operator.getitem, [charmetrics] * len(enc), enc)
	except KeyError:
		# Some iso-latin-1 glyphs are not defined in the font. Try the
		# slower way and report missing glyphs.
		length = len(enc)
		rescharmetrics = [(0, 0,0,0,0)] * length
		for idx in range(length):
			name = enc[idx]
			try:
				rescharmetrics[idx] = charmetrics[name]
			except KeyError:
				# missing character...
				warn(INTERNAL, '%s: missing character %s', filename, name)

	# some fonts don't define ascender and descender (psyr.afm for
	# instance). use the values from the font bounding box instead. This
	# is not really a good idea, but how do we solve this?
	#
	# If psyr.afm is the only afm-file where these values are missing
	# (?) we could use the values from the file s050000l.afm shipped
	# with ghostscript (or replace psyr.afm with that file).
	#
	# This is a more general problem since many of the values Sketch
	# reads from afm files are only optional (including ascender and
	# descender).
	if not attribs.has_key('Ascender'):
		attribs['Ascender'] = attribs['FontBBox'][3]
	if not attribs.has_key('Descender'):
		attribs['Descender'] = attribs['FontBBox'][1]

	return (CreateFontMetric(attribs['Ascender'], attribs['Descender'],
								attribs['FontBBox'], attribs['ItalicAngle'],
								rescharmetrics),
			enc)


_warned_about_afm = {}
def read_metric(ps_name):
	for afm in ps_to_filename[ps_name]:
		afm = afm + '.afm'
		filename = find_in_path(config.font_path, afm)
		if filename:
			if __debug__:
				import time
				start = time.clock()
			metric = read_afm_file(filename)
			if __debug__:
				pdebug('timing', 'time to read afm %s: %g', afm,
						time.clock() - start)
			return metric
	else:
		if not _warned_about_afm.get(afm):
			warn(USER,
					_("I cannot find the metrics for the font %(ps_name)s.\n"
					"The file %(afm)s is not in the font_path.\n"
					"I'll use the metrics for %(fallback)s instead."),
					ps_name = ps_name, afm = afm,
					fallback = config.preferences.fallback_font)
			_warned_about_afm[afm] = 1
		if ps_name != config.preferences.fallback_font:
			return read_metric(config.preferences.fallback_font)
		else:
			raise SketchError("Can't load metrics for fallback font %s",
								config.preferences.fallback_font)


def font_file_name(ps_name):
	names = []
	for basename in ps_to_filename[ps_name]:
		names.append(basename + '.pfb')
		names.append(basename + '.pfa')
	filename = find_files_in_path(config.font_path, names)
	return filename

	
def read_outlines(ps_name):
	filename = font_file_name(ps_name)
	if filename:
		if __debug__:
			pdebug('font', 'read_outlines: %s', filename)

		import app.Lib.type1
		return app.Lib.type1.read_outlines(filename)
	else:
		raise SketchInternalError('Cannot find file for font %s' % ps_name)

def convert_outline(outline):
	paths = []
	trafo = Scale(0.001)
	for closed, sub in outline:
		if closed:
			sub.append(sub[0])
		path = CreatePath()
		paths.append(path)
		for item in sub:
			if len(item) == 2:
				apply(path.AppendLine, item)
			else:
				apply(path.AppendBezier, item)
		if closed:
			path.load_close()
	for path in paths:
		path.Transform(trafo)
	return tuple(paths)




fontlist = []
fontmap = {}
ps_to_filename = {}

def _add_ps_filename(ps_name, filename):
	filename = (filename,)
	if ps_to_filename.has_key(ps_name):
		filename = ps_to_filename[ps_name] + filename
	ps_to_filename[ps_name] = filename

#def read_font_dirs():
	##print 'read_font_dirs'
	#if __debug__:
		#import time
		#start = time.clock()

	#rx_sfd = re.compile(r'^.*\.sfd$')
	#for directory in config.font_path:
		##print directory
		#try:
			#filenames = os.listdir(directory)
		#except os.error, exc:
			#warn(USER, _("Cannot list directory %s:%s\n"
							#"ignoring it in font_path"),
					#directory, str(exc))
			#continue
		#dirfiles = filter(rx_sfd.match, filenames)
		#for filename in dirfiles:
			#filename = os.path.join(directory, filename)
			##print filename
			#try:
				#file = open(filename, 'r')
				#line_nr = 0
				#for line in file.readlines():
					#line_nr = line_nr + 1
					#line = strip(line)
					#if not line or line[0] == '#':
						#continue
					#info = map(intern, split(line, ','))
					#if len(info) == 6:
						#psname = info[0]
						#fontlist.append(tuple(info[:-1]))
						#_add_ps_filename(psname, info[-1])
						#fontmap[psname] = tuple(info[1:-1])
					#elif len(info) == 2:
						#psname, basename = info
						#_add_ps_filename(psname, basename)
					#else:
						#warn(INTERNAL,'%s:%d: line must have exactly 6 fields',
								#filename, line_nr)
				#file.close()
			#except IOError, value:
				#warn(USER, _("Cannot load sfd file %(filename)s:%(message)s;"
								#"ignoring it"),
						#filename = filename, message = value.strerror)
	#if __debug__:
		#pdebug('timing', 'time to read font dirs: %g', time.clock() - start)

def make_family_to_fonts():
	families = {}
	for item in fontlist:
		family = item[1]
		fontname = item[0]
		if families.has_key(family):
			families[family] = families[family] + (fontname,)
		else:
			families[family] = (fontname,)
	return families



xlfd_template = "%s--%s-*-*-*-*-*-%s"

font_cache = SKCache()


#_warned_about_font = {}
#def GetFont(fontname):
	#if font_cache.has_key(fontname):
		#return font_cache[fontname]
	#if not fontmap.has_key(fontname):
		#if not _warned_about_font.get(fontname):
			#warn(USER, _("I can't find font %(fontname)s. "
							#"I'll use %(fallback)s instead"),
					#fontname = fontname,
					#fallback = config.preferences.fallback_font)
			#_warned_about_font[fontname] = 1
		#if fontname != config.preferences.fallback_font:
			#return GetFont(config.preferences.fallback_font)
		#raise ValueError, 'Cannot find font %s.' % fontname
	#return Font(fontname)


#class Font:

	#def __init__(self, name):
		#self.name = name
		#info = fontmap[name]
		#family, font_attrs, xlfd_start, encoding_name = info
		#self.family = family
		#self.font_attrs = font_attrs
		#self.xlfd_start = lower(xlfd_start)
		#self.encoding_name = encoding_name
		#self.metric, self.encoding = read_metric(self.PostScriptName())
		#self.outlines = None

		#self.ref_count = 0
		#font_cache[self.name] = self

	#def __del__(self):
		#if font_cache.has_key(self.name):
			#del font_cache[self.name]

	#def __repr__(self):
		#return "<Font %s>" % self.name

	#def GetXLFD(self, size_trafo):
		#if type(size_trafo) == TrafoType:
			#if size_trafo.m11 == size_trafo.m22 > 0\
				#and size_trafo.m12 == size_trafo.m21 == 0:
				## a uniform scaling. Special case for better X11R5
				## compatibility
				#return xlfd_template % (self.xlfd_start,
										#int(round(size_trafo.m11)),
										#self.encoding_name)
			#return xlfd_template % (self.xlfd_start, xlfd_matrix(size_trafo),
									#self.encoding_name)
		#return xlfd_template % (self.xlfd_start, int(round(size_trafo)),
								#self.encoding_name)

	#def PostScriptName(self):
		#return self.name

	#def TextBoundingBox(self, text, size):
		## Return the bounding rectangle of TEXT when set in this font
		## with a size of SIZE. The coordinates of the rectangle are
		## relative to the origin of the first character.
		#llx, lly, urx, ury = self.metric.string_bbox(text)
		#size = size / 1000.0
		#return (llx * size, lly * size, urx * size, ury * size)

	#def TextCoordBox(self, text, size):
		## Return the coord rectangle of TEXT when set in this font with
		## a size of SIZE. The coordinates of the rectangle are relative
		## to the origin of the first character.
		#metric = self.metric
		#width = metric.string_width(text)
		#size = size / 1000.0
		#return (0,             metric.descender * size,
				#width * size,  metric.ascender * size)

	#def TextCaretData(self, text, pos, size):
		#from math import tan, pi
		#size = size / 1000.0
		#x = self.metric.string_width(text, pos) * size
		#lly = self.metric.lly * size
		#ury = self.metric.ury * size
		#t = tan(self.metric.italic_angle * pi / 180.0);
		#up = ury - lly
		#return Point(x - t * lly, lly), Point(-t * up, up)

	#def TypesetText(self, text):
		#return self.metric.typeset_string(text)

	#def IsPrintable(self, char):
		#return self.encoding[ord(char)] != encoding.notdef

	#def GetOutline(self, char):
		#if self.outlines is None:
			#self.char_strings, self.cs_interp \
								#= read_outlines(self.PostScriptName())
			#self.outlines = {}
		#char_name = self.encoding[ord(char)]
		#outline = self.outlines.get(char_name)
		#if outline is None:
			#self.cs_interp.execute(self.char_strings[char_name])
			#outline = convert_outline(self.cs_interp.paths)
			#self.outlines[char_name] = outline
			#self.cs_interp.reset()
		#copy = []
		#for path in outline:
			#path = path.Duplicate()
			#copy.append(path)
		#return tuple(copy)

	#def FontFileName(self):
		#return font_file_name(self.PostScriptName())

#_warned_about_font = {}
#def GetFont(fontname):
	#if font_cache.has_key(fontname):
		#return font_cache[fontname]
	#if not fontmap.has_key(fontname):
		#if not _warned_about_font.get(fontname):
			#warn(USER, _("I can't find font %(fontname)s. "
							#"I'll use %(fallback)s instead"),
					#fontname = fontname,
					#fallback = config.preferences.fallback_font)
			#_warned_about_font[fontname] = 1
		#if fontname != config.preferences.fallback_font:
			#return GetFont(config.preferences.fallback_font)
		#raise ValueError, 'Cannot find font %s.' % fontname
	#return Font(fontname)

#===============NEW FONT ENGINE IMPLEMENTATION===========================
# font types: PS1 - Postscript Type1; TTF - TrueType; OTF - OpenType
# Currently TTF support only

# Fontlist definition (list of tuples):
#-------------------
#PS name
#family name
#style
#xlfd name
#encoding
#filename
#bold -flag
#italic -flag
freetype_lib = ft2.Library()

def scan_fonts_dirs():
	fontfile_list=[]
	user_font_dir=os.path.join(gethome(),config.preferences.user_font_dir)
	win_dir='/mnt/win_c/WINDOWS/Fonts'
	for path in [config.preferences.system_font_dir, win_dir]:# user_font_dir]:
		fontfile_list+=get_files_tree(path,'ttf')       
		fontfile_list+=get_files_tree(path,'TTF')       
		
	for fontfile in fontfile_list:
		try:
			f = open(fontfile, 'r')
			face = ft2.Face(freetype_lib, f, 0)
		except:
			sys.stderr.write("error opening file %s\n" % (fontfile))
			continue
		ps_name=face.getPostscriptName()
		info=(ps_name,
				face.family_name,
				face.style_name,
				'',
				'UTF8',
				fontfile,
				face.style_flags & ft2.FT_STYLE_FLAG_BOLD,
				face.style_flags & ft2.FT_STYLE_FLAG_ITALIC)
		fontlist.append(info)
		fontmap[ps_name] = (face.family_name,
				face.style_name,
				'',
				'UTF8',
				fontfile,
				face.style_flags & ft2.FT_STYLE_FLAG_BOLD,
				face.style_flags & ft2.FT_STYLE_FLAG_ITALIC)

		filename = (fontfile,)
		if ps_to_filename.has_key(ps_name):
			filename = ps_to_filename[ps_name] + filename
		ps_to_filename[ps_name] = filename
		
		f.close()
		
	
_warned_about_font = {}

def GetFont(fontname):
	if font_cache.has_key(fontname):
		return font_cache[fontname]
	if not fontmap.has_key(fontname):
		if not _warned_about_font.get(fontname):
			warn(USER, _("I can't find font %(fontname)s. "
							"I'll use %(fallback)s instead"),
					fontname = fontname,
					fallback = config.preferences.fallback_font)
			_warned_about_font[fontname] = 1
		if fontname != config.preferences.fallback_font:
			return GetFont(config.preferences.fallback_font)
		raise ValueError, 'Cannot find font %s.' % fontname
	return Font(fontname)

default_encoding = 'utf-8'
resolution=72  

class Font:
	def __init__(self, name):
		self.name = name
		info = fontmap[name]
		family, font_attrs, xlfd_start, encoding_name, fontfile, bold, italic = info
		self.bold=bold
		self.italic=italic
		self.fontfile=fontfile
		self.family = family
		self.font_attrs = font_attrs
		self.xlfd_start = lower(xlfd_start)
		self.encoding_name = encoding_name
		self.metric = None
		self.encoding = self.encoding_name
		self.outlines = None
		self.face = None
		self.enc_vector=None
		self.ref_count = 0
		font_cache[self.name] = self
		self.fontstream=None
		self.fontsize=10

	def __del__(self):
		if font_cache.has_key(self.name):
			del font_cache[self.name]

	def __repr__(self):
		return "<Font %s>" % self.name

	def GetXLFD(self, size_trafo):
		if type(size_trafo) == TrafoType:
			if size_trafo.m11 == size_trafo.m22 > 0\
				and size_trafo.m12 == size_trafo.m21 == 0:
				# a uniform scaling. Special case for better X11R5
				# compatibility
				return xlfd_template % (self.xlfd_start,
										int(round(size_trafo.m11)),
										self.encoding_name)
			return xlfd_template % (self.xlfd_start, xlfd_matrix(size_trafo),
									self.encoding_name)
		return xlfd_template % (self.xlfd_start, int(round(size_trafo)),
								self.encoding_name)

	def PostScriptName(self):
		return self.name
	
	def init_face(self):
		if not self.face:
			if not self.fontstream:
				f = open(self.fontfile)
				import StringIO
				s = f.read()
				f.close()
				self.fontstream= StringIO.StringIO(s)
						
			self.face=ft2.Face(freetype_lib, self.fontstream, 0)
			use_unicode = 0
			
			for index in range(self.face.num_charmaps):
				cm = ft2.CharMap(self.face, index)
				if cm.encoding_as_string == "unic":
					use_unicode = 1
					self.face.setCharMap(cm)
					break
			
			if not use_unicode:
				self.face.setCharMap(ft2.CharMap(self.face, 0, 0))
			self.enc_vector = self.face.encodingVector()

	def TextBoundingBox(self, text, size):
		# Return the bounding rectangle of TEXT when set in this font
		# with a size of SIZE. The coordinates of the rectangle are
		# relative to the origin of the first character.
		self.init_face()
		self.fontsize=size
		self.face.setCharSize(10240, 10240, resolution, resolution)

		posx = posy = 0
		lastIndex = 0
		text_xmin = text_ymin = 0
		text_xmax = text_ymax = 0

		for c in text:
			thisIndex = self.enc_vector[ord(c)]
			glyph = ft2.Glyph(self.face, thisIndex, 0)
			kerning = self.face.getKerning(lastIndex, thisIndex, 0)
			posx += kerning[0] << 10
			posy += kerning[1] << 10
			posx += glyph.advance[0]
			posy += glyph.advance[1]
			lastIndex = thisIndex
			(gl_xmin, gl_ymin, gl_xmax, gl_ymax) = glyph.getCBox(ft2.ft_glyph_bbox_subpixels)
			gl_xmin += posx >> 10
			gl_ymin += posy >> 10 
			gl_xmax += posx >> 10
			gl_ymax += posy >> 10
			text_xmin = min(text_xmin, gl_xmin)
			text_ymin = min(text_ymin, gl_ymin)
			text_xmax = max(text_xmax, gl_xmax)
			text_ymax = max(text_ymax, gl_ymax)             
		return (text_xmin*self.fontsize/10240.0, text_ymin*self.fontsize/10240.0, 
				text_xmax*self.fontsize/10240.0, text_ymax*self.fontsize/10240.0)
		#llx, lly, urx, ury = self.metric.string_bbox(text)
		#size = size / 1000.0
		#return (llx * size, lly * size, urx * size, ury * size)

	def TextCoordBox(self, text, size):
		# Return the coord rectangle of TEXT when set in this font with
		# a size of SIZE. The coordinates of the rectangle are relative
		# to the origin of the first character.
		#metric = self.metric
		#width = metric.string_width(text)
		#size = size / 1000.0
		return self.TextBoundingBox(text, size)
		#return (0,              metric.descender * size,
				#width * size,   metric.ascender * size)

	def TextCaretData(self, text, pos, size):
		llx,lly,urx,ury=self.TextBoundingBox(text[0:pos],size)
		x = urx-llx
		t = 0;
		up = ury - lly
		return Point(x - t * lly, lly), Point(-t * up, up)

	def TypesetText(self, text):
		return self.metric.typeset_string(text)

	def IsPrintable(self, char):
		return 1
	
	def GetPaths(self, text):
		self.init_face()
		# convert glyph data into bezier polygons
		print self.fontfile		
		paths = []
		offset = i = 0
		for i in text:		
			#print "character:", i,
			thisIndex = self.enc_vector[ord(i)]
			glyph = ft2.Glyph(self.face, thisIndex, 1)
			for contour in glyph.outline:
				# rotate contour so that it begins with an onpoint
				x, y, onpoint = contour[0]
				if onpoint:
					for j in range(1, len(contour)):
						x, y, onpoint = contour[j]
						if onpoint:
							contour = contour[j:] + contour[:j]
							break
				else:
					print "unsupported type of contour (no onpoint)"
				# create a sK1 path object
				path = CreatePath()
				j = 0
				npoints = len(contour)
				x, y, onpoint = contour[0]
				last_point = Point(x, y)
				while j <= npoints:
					if j == npoints:
						x, y, onpoint = contour[0]
					else:
						x, y, onpoint = contour[j]
					point = Point(x, y)
					j = j + 1
					if onpoint:
						path.AppendLine(point)
						last_point = point
					else:
						c1 = last_point + (point - last_point) * 2.0 / 3.0
						x, y, onpoint = contour[j % npoints]
						if onpoint:
							j = j + 1
							cont = ContAngle
						else:
							x = point.x + (x - point.x) * 0.5
							y = point.y + (y - point.y) * 0.5
							cont = ContSmooth
						last_point = Point(x, y)
						c2 = last_point + (point - last_point) * 2.0 / 3.0
						path.AppendBezier(c1, c2, last_point, cont)
				path.ClosePath()
				path.Translate(offset, 0)
				path.Transform(Scale(2*self.fontsize/102400.0))
				paths.append(path)
			offset = offset + glyph.advance[0]/1000
		print 'glyph.advance[0]:' ,glyph.advance[0]/1000, 'fontsize: ', self.fontsize
		return tuple(paths)

	def GetOutline(self, char):		
		if self.outlines is None:
			self.char_strings, self.cs_interp = read_outlines(self.PostScriptName())
			self.outlines = {}
		char_name = self.encoding[ord(char)]
		outline = self.outlines.get(char_name)
		if outline is None:
			self.cs_interp.execute(self.char_strings[char_name])
			outline = convert_outline(self.cs_interp.paths)
			self.outlines[char_name] = outline
			self.cs_interp.reset()
		copy = []
		for path in outline:
			path = path.Duplicate()
			copy.append(path)
		return tuple(copy)

	def FontFileName(self):
		return font_file_name(self.PostScriptName())

#
#       Initialization on import
#

Subscribe(const.INITIALIZE, scan_fonts_dirs)
