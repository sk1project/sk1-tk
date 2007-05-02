# -*- coding: utf-8 -*-

# Copyright (C) 2003-2006 by Igor E. Novikov
# Copyright (C) 1997, 1998, 1999 by Bernhard Herzog
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

#
#       Color Handling
#

from string import atoi

from app.events.warn import warn, INTERNAL, USER
from app._sketch import RGBColor, XVisual
from app import config, _
from lcms.lcms import *

skvisual = None
CMYK = 'CMYK'
RGB = 'RGB'

def CreateRGBColor(r, g, b):
#       print 'CreateRGBColor', round(r, 3), round(g, 3), round(b, 3)
	return ExtColor(round(r, 3), round(g, 3), round(b, 3))

def XRGBColor(s):
	# only understands the old x specification with two hex digits per
	# component. e.g. `#00FF00'
	if s[0] != '#':
		raise ValueError("Color %s doesn't start with a '#'" % s)
	r = atoi(s[1:3], 16) / 255.0
	g = atoi(s[3:5], 16) / 255.0
	b = atoi(s[5:7], 16) / 255.0
	return CreateRGBColor(r, g, b)

def CreateCMYKColor(c, m, y, k):
	r,g,b = cmyk_to_rgb(c, m, y, k)
	return ExtColor(r, g, b, 'CMYK', c, m, y, k)

def cmyk_to_rgb(c, m, y, k):
#       print 'CMYK color: C-',c,' M-',m,' Y-',y,' K-',k
	r = round(1.0 - min(1.0, c + k), 3)
	g = round(1.0 - min(1.0, m + k), 3)
	b = round(1.0 - min(1.0, y + k), 3)
	return r, g, b
	
def rgb_to_tk((r, g, b)):
	return '#%04x%04x%04x' % (65535 * r, 65535 * g, 65535 * b)
	
# def rgb2cmyk(r,g,b):
#       r = 1.0 - min(1.0, c + k)
#       g = 1.0 - min(1.0, m + k)
#       b = 1.0 - min(1.0, y + k)
#       return c, m, y, k

def ParseSKColor(model, v1, v2, v3, v4=0, v5=0):
	if model=='CMYK':
		r,g,b = cmyk_to_rgb(v1, v2, v3, v4)
		return ExtColor(r, g, b, 'CMYK', v1, v2, v3, v4)
	else:
		return ExtColor(round(v1, 3), round(v2, 3), round(v3, 3))
		
def ICC_for_CMYK(c,m,y,k):
	
	CMYK = COLORB()
	CMYK[0] = int(round(c, 2)*255)
	CMYK[1] = int(round(m, 2)*255)
	CMYK[2] = int(round(y, 2)*255)
	CMYK[3] = int(round(k, 2)*255)
	
	RGB = COLORB()
	RGB[0] = 0
	RGB[1] = 0
	RGB[2] = 0
	
	#hRGB   = cmsCreate_sRGBProfile()
	hRGB   = cmsOpenProfileFromFile("/usr/local/lib/sK1/sRGB.icm", "r")
	hCMYK  = cmsOpenProfileFromFile("/usr/local/lib/sK1/GenericCMYK.icm", "r")

	xform = cmsCreateTransform(hCMYK, TYPE_CMYK_8, 
							   hRGB, TYPE_RGB_8, 
							   INTENT_PERCEPTUAL, cmsFLAGS_NOTPRECALC)
	cmsDoTransform(xform, CMYK, RGB, 1)
	
	cmsDeleteTransform(xform)
	cmsCloseProfile(hCMYK)
	cmsCloseProfile(hRGB)
	
	return round(RGB[0]/255.0, 3), round(RGB[1]/255.0, 3), round(RGB[2]/255.0, 3)

class ExtColor:
	
	def __init__(self, r, g, b, model = 'RGB', c = None, m = None, y = None, k = None, alpha=.3):
	
		'''Extended color class for multimodel color support.
		
		ExtColor class is a wrapper for old native RGBColor object. 
		Real Python object for color representation is more flexible and extendable way.
		At this time we support RGB and CMYK color models.'''
		
		self.model = model
		self.red=r
		self.green=g
		self.blue=b
		self.c=c
		self.m=m
		self.y=y
		self.k=k
		self.alpha=alpha
		
	def getCMYK(self):
		return self.c, self.m, self.y, self.k
	
	def RGB(self):
		'''This method is introduced for ICC support'''
		if self.model == 'CMYK':
			if app.config.use_cms:				
				r,g,b = app.colormanager.processCMYK(self.c,self.m,self.y,self.k)
			else:
				r,g,b = cmyk_to_rgb(self.c,self.m,self.y,self.k)
			return RGBColor(r, g, b)
		else:
			if app.config.use_cms:
				if app.config.simulate_printer:
					c,m,y,k = app.colormanager.convertRGB(self.red, self.green, self.blue)
					r,g,b = app.colormanager.processCMYK(c,m,y,k)                       
					return RGBColor(r, g, b)
				else:
					r,g,b = app.colormanager.processRGB(self.red, self.green, self.blue)
					return RGBColor(r, g, b)
			else:
				return RGBColor(self.red, self.green, self.blue)
	
	def cRGB(self):
		return (self.red, self.green, self.blue)
	
	def cRGBA(self):
		return (self.red, self.green, self.blue, self.alpha)
	
	def toString(self):
		if self.model == 'CMYK':
			C='C-'+str(int(round(self.c, 2)*100))+'% '
			M='M-'+str(int(round(self.m, 2)*100))+'% '
			Y='Y-'+str(int(round(self.y, 2)*100))+'% '
			K='K-'+str(int(round(self.k, 2)*100))+'%'
			return C+M+Y+K
		else:
			R='R-'+str(int(round(self.red*255, 0)))
			G=' G-'+str(int(round(self.green*255, 0)))
			B=' B-'+str(int(round(self.blue*255, 0)))
			return R+G+B
			
	def toSave(self):
		if self.model == 'CMYK':
			C= str(round(self.c, 3))+','
			M= str(round(self.m, 3))+','
			Y= str(round(self.y, 3))+','
			K= str(round(self.k, 3))
			return '("'+self.model+'",'+C+M+Y+K+')'
		else:
			R= str(round(self.red, 3))+','
			G= str(round(self.green, 3))+','
			B= str(round(self.blue, 3))
			return '("'+self.model+'",'+R+G+B+')'
		

#
#       some standard colors.
#

class StandardColors:
	black   = CreateRGBColor(0.0, 0.0, 0.0)
	darkgray        = CreateRGBColor(0.25, 0.25, 0.25)
	gray    = CreateRGBColor(0.5, 0.5, 0.5)
	lightgray       = CreateRGBColor(0.75, 0.75, 0.75)
	white   = CreateRGBColor(1.0, 1.0, 1.0)
	red             = CreateRGBColor(1.0, 0.0, 0.0)
	green   = CreateRGBColor(0.0, 1.0, 0.0)
	blue    = CreateRGBColor(0.0, 0.0, 1.0)
	cyan    = CreateRGBColor(0.0, 1.0, 1.0)
	magenta = CreateRGBColor(1.0, 0.0, 1.0)
	yellow  = CreateRGBColor(1.0, 1.0, 0.0)


#
#       For 8-bit displays:
#

def float_to_x(float):
	return int(int(float * 63) / 63.0 * 65535)

def fill_colormap(cmap):
	max = 65535
	colors = []
	color_idx = []
	failed = 0
	
	shades_r, shades_g, shades_b, shades_gray = config.preferences.color_cube
	max_r = shades_r - 1
	max_g = shades_g - 1
	max_b = shades_b - 1

	for red in range(shades_r):
		red = float_to_x(red / float(max_r))
		for green in range(shades_g):
			green = float_to_x(green / float(max_g))
			for blue in range(shades_b):
				blue = float_to_x(blue / float(max_b))
				colors.append((red, green, blue))
	for i in range(shades_gray):
		value = int((i / float(shades_gray - 1)) * max)
		colors.append((value, value, value))

	for red, green, blue in colors:
		try:
			ret = cmap.AllocColor(red, green, blue)
			color_idx.append(ret[0])
		except:
			color_idx.append(None)
			failed = 1

	if failed:
		warn(USER,
				_("I can't alloc all needed colors. I'll use a private colormap"))
		warn(INTERNAL, "allocated colors without private colormap: %d",
				len(filter(lambda i: i is None, color_idx)))
		if config.preferences.reduce_color_flashing:
			#print 'reduce color flashing'
			cmap = cmap.CopyColormapAndFree()
			for idx in range(len(color_idx)):
				if color_idx[idx] is None:
					color_idx[idx] = apply(cmap.AllocColor, colors[idx])[0]
		else:
			#print "don't reduce color flashing"
			cmap = cmap.CopyColormapAndFree()
			cmap.FreeColors(filter(lambda i: i is not None, color_idx), 0)
			color_idx = []
			for red, green, blue in colors:
				color_idx.append(cmap.AllocColor(red, green, blue)[0])
				
	return cmap, color_idx

_init_from_widget_done = 0
global_colormap = None
def InitFromWidget(tkwin, root = None):
	global _init_from_widget_done, skvisual
	if _init_from_widget_done:
		return
	if root:
		visual = root.winfo_visual()
		if visual == 'truecolor':
			skvisual = XVisual(tkwin.c_display(), tkwin.c_visual())
			#skvisual.set_gamma(config.preferences.screen_gamma)
			alloc_function = skvisual.get_pixel
		if visual == 'pseudocolor' and root.winfo_depth() == 8:
			global global_colormap
			cmap = tkwin.colormap()
			newcmap, idxs = fill_colormap(cmap)
			if newcmap != cmap:
				cmap = newcmap
				tkwin.SetColormap(cmap)
			shades_r, shades_g, shades_b, shades_gray \
						= config.preferences.color_cube
			skvisual = XVisual(tkwin.c_display(), tkwin.c_visual(),
								(shades_r, shades_g, shades_b, shades_gray, idxs))
			global_colormap = cmap
	_init_from_widget_done = 1
