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
import properties

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
	for path in [config.preferences.system_font_dir, user_font_dir]:
		fontfile_list+=get_files_tree(path,'ttf')       
		fontfile_list+=get_files_tree(path,'TTF')  
		
	for fontfile in fontfile_list:
		try:
			f = open(fontfile, 'r')
			face = ft2.Face(freetype_lib, f, 0)
		except:
			sys.stderr.write("error opening file %s\n" % (fontfile))
			continue
		#Check for Unicode support into font
		is_unicode=0
		for index in range(face.num_charmaps):
			cm = ft2.CharMap(face, index)
			if cm.encoding_as_string == "unic":
				is_unicode = 1
				break
		if is_unicode:			
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
#			warn(USER, _("I can't find font %(fontname)s. "
#							"I'll use %(fallback)s instead"),
#					fontname = fontname,
#					fallback = config.preferences.fallback_font)
			_warned_about_font[fontname] = 1
		if fontname != config.preferences.fallback_font:
			return GetFont(config.preferences.fallback_font)
		else:
			names = fontmap.keys()
			names.sort()
			return GetFont(names[0])
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
		self.use_unicode = 0
		
		self.init_face()
		self.face.setCharSize(10240, 10240, resolution, resolution)

	def __del__(self):
		if font_cache.has_key(self.name):
			del font_cache[self.name]

	def __repr__(self):
		return "<Font %s>" % self.name

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
			
			for index in range(self.face.num_charmaps):
				cm = ft2.CharMap(self.face, index)
				if cm.encoding_as_string == "unic":
					self.use_unicode = 1
					self.face.setCharMap(cm)
					break
			
			if not self.use_unicode:
				self.face.setCharMap(ft2.CharMap(self.face, 0, 0))
			self.enc_vector = self.face.encodingVector()

################
	def TextBoundingBox(self, text, size, prop):
		# Return the bounding rectangle of TEXT when set in this font
		# with a size of SIZE. The coordinates of the rectangle are
		# relative to the origin of the first character.

		posx = posy = posx_max = posy_max= 0
		lastIndex = 0
		text_xmin = text_ymin = 0
		text_xmax = text_ymax = 0		
		
		fheight=self.getFontHeight(prop)*5
		lines=split(text, '\n')
		adv=0
		tab=1
		align_offset=0
		for line in lines:
			posx = 0
			for c in line:
				if c=='\t':
					c=' ';tab=3
				else:
					tab=1
				try:
					thisIndex = self.enc_vector[ord(c)]
				except:
					thisIndex = self.enc_vector[ord('?')]
				glyph = ft2.Glyph(self.face, thisIndex, 0)
				kerning = self.face.getKerning(lastIndex, thisIndex, 0)
				posx += kerning[0] << 10
				posy += kerning[1] << 10
				if c==' ':
					adv= glyph.advance[0]*prop.chargap*prop.wordgap*tab
				else:
					adv= glyph.advance[0]*prop.chargap
				posx+=adv
				posy += glyph.advance[1]
				lastIndex = thisIndex
				(gl_xmin, gl_ymin, gl_xmax, gl_ymax) = glyph.getCBox(ft2.ft_glyph_bbox_subpixels)
				gl_xmin += int(posx) >> 10
				gl_ymin += int(posy) >> 10 
				gl_xmax += int(posx) >> 10
				gl_ymax += int(posy) >> 10
				text_xmin = min(text_xmin, gl_xmin)
				text_ymin = min(text_ymin, gl_ymin)
				text_xmax = max(text_xmax, gl_xmax)
				text_ymax = max(text_ymax, gl_ymax)
			align_offset=min(self.getAlignOffset(line,prop),align_offset)
			posx_max = max(posx_max,posx)
			posy_max -= fheight
		posy_max =posy_max + fheight + text_ymin
		x1=text_xmin*size/10240.0
		y1=text_ymax*size/10240.0
		x2=posx_max*size/10240000.0
		y2=posy_max*size/10240.0
		if prop.align:
			if prop.align==const.ALIGN_RIGHT:
				return (-x2, y1, x1, y2)
			if prop.align==const.ALIGN_CENTER:
				return (x1-x2/2, y1, x2/2, y2)
		else:
			return (x1, y1, x2, y2)


	def TextCoordBox(self, text, size, prop):
		# Return the coord rectangle of TEXT when set in this font with
		# a size of SIZE. The coordinates of the rectangle are relative
		# to the origin of the first character.
		return self.TextBoundingBox(text, size, prop)

################
	def TextCaretData(self, text, pos, size, prop):
		fheight=self.getFontHeight(prop)*5*size/10240.0
		vofset=-(len(split(text[0:pos], '\n'))-1)*fheight
		lly=vofset-fheight*1/4*.75
		ury=vofset+fheight*3/4
		
		line=split(text, '\n')[len(split(text[0:pos], '\n'))-1]
		x1,y1,x2,y2=self.TextBoundingBox(line,size, prop)
		align_offset=x1-x2
		
		fragment=split(text[0:pos], '\n')[-1]
		x1,y1,x2,y2=self.TextBoundingBox(fragment,size, prop)
		if prop.align:
			if prop.align==const.ALIGN_RIGHT:
				x=align_offset-x1
			if prop.align==const.ALIGN_CENTER:
				x=x2*2+align_offset/2
		else:
			x=x2	
		up = ury - lly
		return Point(x, lly), Point(0, up)

################
	def TypesetText(self, text, prop):					
		return self.cacl_typeset(text, prop)[0:-1]

	def IsPrintable(self, char):
		return 1

################	
	# face.getMetrics() returns tuple:	
	#(x_ppem, y_ppem, x_scale, y_scale, 
	# ascender, descender, height, max_advance)
	def getFontHeight(self,prop):
		return (abs(self.face.getMetrics()[5])+abs(self.face.getMetrics()[6]))*prop.linegap/5.583
#		return abs(self.face.getMetrics()[7]/5.35)*prop.linegap
	
	def getAlignOffset(self,line,prop):
		if prop.align:
			typeset=self.cacl_typeset(line, prop,1)
			x1,y1=typeset[0]
			x2,y2=typeset[-1]
			if prop.align==const.ALIGN_RIGHT:
				return x1-x2
			if prop.align==const.ALIGN_CENTER:
				return (x1-x2)/2	
		else:
			return 0
		
	def cacl_typeset(self, text, prop, noalign=0): 
		posx = 0
		posy = 0
		lastIndex = 0
		result=[]
		tab=1
		
		fheight=self.getFontHeight(prop)*5
		voffset=0
		lines=split(text, '\n')
		for line in lines:
			if noalign:
				align_offset=0
			else:
				align_offset=self.getAlignOffset(line,prop)
			result.append(Point(align_offset,voffset/10240.0))
			for c in line:
				if c=='\t':
					c=' ';tab=3
				else:
					tab=1
				try:
					thisIndex = self.enc_vector[ord(c)]
				except:
					thisIndex = self.enc_vector[ord('?')]
				glyph = ft2.Glyph(self.face, thisIndex, 0)
				kerning = self.face.getKerning(lastIndex, thisIndex, 0)
				posx += kerning[0]
				posy += kerning[1]
				if c==' ':
					posx += glyph.advance[0]*prop.chargap*prop.wordgap*tab/1000
				else:
					posx += glyph.advance[0]*prop.chargap/1000
				posy += glyph.advance[1]/1000
				lastIndex = thisIndex
				result.append(Point(posx/10240.0+align_offset,voffset/10240.0))				
			voffset-=fheight
			posx = 0
		return result
					
################		
	def GetPaths(self, text, prop):
		# convert glyph data into bezier polygons	
		paths = []
		fheight=self.getFontHeight(prop)
		voffset=0
		tab=1
		lastIndex=0
		lines=split(text, '\n')
		for line in lines:
			offset = c = 0
			align_offset=self.getAlignOffset(line,prop)
			for c in line:
				if c=='\t':
					c=' ';tab=3
				else:
					tab=1		
				try:
					thisIndex = self.enc_vector[ord(c)]
				except:
					thisIndex = self.enc_vector[ord('?')]
				glyph = ft2.Glyph(self.face, thisIndex, 1)
				kerning = self.face.getKerning(lastIndex, thisIndex, 0)
				lastIndex = thisIndex
				offset += kerning[0]  / 4.0
				voffset += kerning[1] / 4.0
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
					path.Translate(offset, voffset)
					path.Transform(Scale(0.5/1024.0))
					path.Translate(align_offset, 0)
					paths.append(path)
				if c==' ':
					offset = offset + glyph.advance[0]*prop.chargap*prop.wordgap*tab/1000
				else:
					offset = offset + glyph.advance[0]*prop.chargap/1000
			voffset-=fheight
		return tuple(paths)

	def GetOutline(self, char):		
		return self.GetPaths(char)

	def FontFileName(self):
		return font_file_name(self.PostScriptName())

#
#       Initialization on import
#

Subscribe(const.INITIALIZE, scan_fonts_dirs)
