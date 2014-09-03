# -*- coding: utf-8 -*-

# Routines for Tk and Ttk UI color theme management

# Copyright (c) 2010 by Igor E.Novikov
#
#This library is free software; you can redistribute it and/or
#modify it under the terms of the GNU Library General Public
#License as published by the Free Software Foundation; either
#version 2 of the License, or (at your option) any later version.
#
#This library is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#Library General Public License for more details.
#
#You should have received a copy of the GNU Library General Public
#License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

from xml.sax import handler
import xml.sax, os
from xml.sax.xmlreader import InputSource
from tempfile import NamedTemporaryFile

SYSTEM_SCHEME='System'
BUILTIN_SCHEME='Built-in'

			
def gtk_to_tk_color(color):
	"""
	Converts gtk color representation to tk.
	For example: #0000ffff0000 will be converted to #00ff00
	"""
	return color[0]+color[1]+color[2]+color[5]+color[6]+color[9]+color[10]

def tkcolor_to_rgb(tkcolor):
	"""
	Converts tk color string as tuple of integer values.
	For example: #ff00ff => (255,0,255)
	"""
	return (int(tkcolor[1:3], 0x10),int(tkcolor[3:5], 0x10),int(tkcolor[5:], 0x10))

def saturated_color(color):
	"""
	Returns saturated color value. 
	"""
	r,g,b=tkcolor_to_rgb(color)
	delta=255-max(r,g,b)
	return '#%02X%02X%02X'%(r+delta,g+delta,b+delta)
				
def middle_color(dark, light, factor=0.5):
	"""
	Calcs middle color value.
	
	dark, light - tk color strings
	factor - resulted color shift 
	"""
	dark=tkcolor_to_rgb(dark)
	light=tkcolor_to_rgb(light)
	r=dark[0]+(light[0]-dark[0])*factor
	g=dark[1]+(light[1]-dark[1])*factor
	b=dark[2]+(light[2]-dark[2])*factor
	return '#%02X%02X%02X'%(r,g,b)

def lighter_color(color, factor):
	"""
	Calcs lighted color value according factor.
	
	color - tk color strings
	factor - resulted color shift   
	"""
	return middle_color(color, saturated_color(color), factor)
	


class ColorScheme:
	"""
	The class represents UI color scheme.
	Colors can be imported from system (SYSTEM_SCHEME),
	default built-in values (BUILTIN_SCHEME)
	or loaded from well-formated xml file.
	"""
	
	bg ='#d4d0c8'
	foreground ='#000000'
	highlightbackground ='#f3f2ef'
	highlightcolor ='#b0ada5'
	disabledforeground ='#b0ada6'
	selectbackground ='#002468'
	selectforeground ='#ffffff'
	
	menubackground='#dedad2'
	menuforeground='#000000'
	menuselectbackground='#002468'
	menuselectforeground='#ffffff'
	menudisabledforeground='#b0ada6'
	menubordercolor='#7e7b77'
	
	editfieldbackground='#ffffff'
	editfieldforeground='#000000'
	treelinescolor='#000000'
	
	evencolor='#f0f0f0'
	
	name=BUILTIN_SCHEME
	
	def __init__(self, filepath=BUILTIN_SCHEME):
		self.name=filepath
		if filepath==BUILTIN_SCHEME:
			return
		if filepath==SYSTEM_SCHEME:
			self.import_gtk_colors()
			return
		if filepath and os.path.isfile(filepath):
			self.load_from_file(filepath)	
		else:
			self.name=SYSTEM_SCHEME
			self.import_gtk_colors()
			
	def import_gtk_colors(self):
		"""
		Imports system gtk color scheme using pygtk binding. 
		"""
		colors={}
		tmpfile=NamedTemporaryFile()
		command="import gtk;w = gtk.Window();w.realize();style=w.get_style();"
		command+="print style.base[gtk.STATE_NORMAL].to_string(),"+ \
			" style.base[gtk.STATE_ACTIVE].to_string(),"+ \
			" style.base[gtk.STATE_PRELIGHT].to_string(),"+ \
			" style.base[gtk.STATE_SELECTED].to_string(),"+ \
			" style.base[gtk.STATE_INSENSITIVE].to_string();"
		command+="print style.text[gtk.STATE_NORMAL].to_string(),"+ \
			" style.text[gtk.STATE_ACTIVE].to_string(),"+ \
			" style.text[gtk.STATE_PRELIGHT].to_string(),"+ \
			" style.text[gtk.STATE_SELECTED].to_string(),"+ \
			" style.text[gtk.STATE_INSENSITIVE].to_string();"
		command+="print style.fg[gtk.STATE_NORMAL].to_string(),"+ \
			" style.fg[gtk.STATE_ACTIVE].to_string(),"+ \
			" style.fg[gtk.STATE_PRELIGHT].to_string(),"+ \
			" style.fg[gtk.STATE_SELECTED].to_string(),"+ \
			" style.fg[gtk.STATE_INSENSITIVE].to_string();"
		command+="print style.bg[gtk.STATE_NORMAL].to_string(),"+ \
			" style.bg[gtk.STATE_ACTIVE].to_string(),"+ \
			" style.bg[gtk.STATE_PRELIGHT].to_string(),"+ \
			" style.bg[gtk.STATE_SELECTED].to_string(),"+ \
			" style.bg[gtk.STATE_INSENSITIVE].to_string();"
	
		os.system('python -c "%s" >%s 2>/dev/null'%(command, tmpfile.name))	

		for type in ["base","text","fg","bg"]:
			line=tmpfile.readline().strip().split()
			colors[type+' normal']=gtk_to_tk_color(line[0])
			colors[type+' active']=gtk_to_tk_color(line[1])
			colors[type+' prelight']=gtk_to_tk_color(line[2])
			colors[type+' selected']=gtk_to_tk_color(line[3])
			colors[type+' insensitive']=gtk_to_tk_color(line[4])
		tmpfile.close()
		
		self.map_gtk_colors(colors)
	
	def map_gtk_colors(self,gtk_colors):
		"""
		Maps gtk colors to ColorScheme fields.
		"""
		
		self.bg = gtk_colors['bg normal']
		self.foreground = gtk_colors['text normal']
		
		self.highlightbackground = gtk_colors['bg active']
		self.highlightcolor = gtk_colors['fg active']
		self.disabledforeground = gtk_colors['fg insensitive']
		self.selectbackground = gtk_colors['bg selected']
		self.selectforeground = gtk_colors['text selected']
		
		self.menubackground = lighter_color(self.bg, .25)
		self.menuforeground = gtk_colors['fg normal']
		self.menuselectbackground = gtk_colors['bg selected']
		self.menuselectforeground = gtk_colors['fg selected']
		self.menudisabledforeground = gtk_colors['text insensitive']
		self.menubordercolor = gtk_colors['fg insensitive']
		
		self.editfieldbackground = gtk_colors['base normal']
		self.editfieldforeground = gtk_colors['text normal']
		self.treelinescolor = gtk_colors['text normal']
		
		self.evencolor = middle_color(self.bg, self.editfieldbackground, 0.7)
					
	def load_from_file(self, filename=None):
		"""
		Loads color scheme from well-formated xml file.
		
		filename - full path to xml file
		"""
		if filename:
			content_handler = XMLPrefReader(pref=self)
			error_handler = ErrorHandler()
			entity_resolver = EntityResolver()
			dtd_handler = DTDHandler()
			try:
				input = open(filename, "r")
				input_source = InputSource()
				input_source.setByteStream(input)
				xml_reader = xml.sax.make_parser()
				xml_reader.setContentHandler(content_handler)
				xml_reader.setErrorHandler(error_handler)
				xml_reader.setEntityResolver(entity_resolver)
				xml_reader.setDTDHandler(dtd_handler)
				xml_reader.parse(input_source)
				input.close
			except:
				import traceback
				traceback.print_exc()
				raise
				self.name=None
		if self.disabledforeground is None:
			self.disabledforeground=lighter_color(self.foreground, .3)
		if self.menubackground is None:
			self.menubackground=self.bg
		if self.menuforeground is None:
			self.menuforeground=self.foreground
		if self.menuselectbackground is None:
			self.menuselectbackground=self.selectbackground
		if self.menuselectforeground is None:
			self.menuselectforeground=self.selectforeground
		if self.menudisabledforeground is None:
			self.menudisabledforeground=self.disabledforeground
		if self.menubordercolor is None:
			self.menubordercolor=self.disabledforeground
		if self.editfieldbackground is None:
			self.editfieldbackground='#ffffff'
		if self.editfieldforeground is None:
			self.editfieldforeground=self.foreground
		if self.evencolor is None:
			self.evencolor=middle_color(self.bg, self.editfieldbackground, 0.7)	
		if self.treelinescolor is None:
			self.treelinescolor=self.editfieldforeground	

	
class XMLPrefReader(handler.ContentHandler):
	"""
	Handler for xml file reading.
	"""
	def __init__(self, pref=None):
		self.key = None
		self.value = None
		self.pref = pref

	def startElement(self, name, attrs):
		self.key = name

	def endElement(self, name):
		if name!='preferences':
			code=compile('self.value='+self.value,'<string>','exec')
			exec code
			self.pref.__dict__[self.key] = self.value

	def characters(self, data):
		self.value = data

class ErrorHandler(handler.ErrorHandler): pass
class EntityResolver(handler.EntityResolver): pass
class DTDHandler(handler.DTDHandler): pass	


if __name__ == '__main__':
	theme=ColorScheme(SYSTEM_SCHEME)
	colors=theme.__dict__
	keys=colors.keys()
	keys.sort()
	for key in keys:
		print key,'=',colors[key]
		
