# -*- coding: utf-8 -*-

# Copyright (C) 2007 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

import Tkinter, app, os, string, math
from xml.sax import handler
import xml.sax
from xml.sax.xmlreader import InputSource
from app.conf.configurator import XMLPrefReader, ErrorHandler, EntityResolver, DTDHandler
from app.utils import os_utils
			
class ColorTheme:
	bg ='#959ba2'
	foreground ='#000000'
	highlightbackground ='#ededed'
	highlightcolor ='#000000'
	disabledforeground ='#a3a3a3'
	selectbackground ='#4e87da'
	selectforeground ='#000000'
	name=None
	
	def __init__(self, colorTheme=None):
		self.name=colorTheme
		if colorTheme and os.path.isfile(os.path.join(app.config.user_color_themes, self.name+'.xml')):
			self.load(os.path.join(app.config.user_color_themes, self.name+'.xml'))	
		else:
			self.name='System'
					
	def load(self, filename=None):
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
				
	def correctColor(self):
		self.disabledforeground=self.recalc(self.foreground, self.bg, 0.7)
				
	def recalc(self, dark, light, factor):
		r=int(string.atoi(dark[1:3], 0x10)+string.atoi(light[1:3], 0x10))*factor
		g=int(string.atoi(dark[3:5], 0x10)+string.atoi(light[3:5], 0x10))*factor
		b=int(string.atoi(dark[5:], 0x10)+string.atoi(light[5:], 0x10))*factor
		return '#%02X%02X%02X'%(r,g,b)
	
class UIManager:
	currentColorTheme=None
	systemColorTheme=None
	currentIconSet=None
	root=None
	
	small_font=''
	normal_font=''
	large_font=''	

	def __init__(self, root=None):
		if not root:
			self.root = Tkinter._default_root
		else:
			self.root=root
		self.uploadExtentions()
		self.loadIcons(app.config.preferences.icons)
		self.createTestWidgets()
		self.systemColorTheme=ColorTheme()
		self.getSystemColors()
		self.setColorTheme(app.config.preferences.color_theme)
		self.setFonts()
		self.resetTile()
			
	def uploadExtentions(self):
		self.root.tk.call('lappend', 'auto_path', app.config.user_themes)
		self.root.tk.call('package', 'require', 'tkpng')
		#self.root.tk.call('package', 'require', 'tile')
		tcl=os.path.join(app.config.sk_dir,'app','tcl')
		self.root.tk.call('source', os.path.join(tcl,'combobox.tcl'))
		self.root.tk.call('source', os.path.join(tcl,'tkmenu.tcl'))
		self.root.tk.call('source', os.path.join(tcl,'tkfbox.tcl'))
		self.root.tk.call('source', os.path.join(tcl,'repeater.tcl'))
	
	def createTestWidgets(self):
		self.testEntry = Tkinter.Entry(self.root, name='testEntry')
		self.testSmallLabel = Tkinter.Label(self.root, name='testSmallLabel', text='small')
		self.testNormalLabel = Tkinter.Label(self.root, name='testNormalLabel', text='normal')
		self.testLargeLabel = Tkinter.Label(self.root, name='testLargeLabel', text='large')
		
	def getSystemColors(self):
		self.systemColorTheme.bg=self.testEntry.cget('bg')
		self.systemColorTheme.foreground=self.testEntry.cget('foreground')
		self.systemColorTheme.highlightbackground=self.testEntry.cget('highlightbackground')
		self.systemColorTheme.highlightcolor=self.testEntry.cget('highlightcolor')
		self.systemColorTheme.disabledforeground=self.testEntry.cget('disabledforeground')
		self.systemColorTheme.selectbackground=self.testEntry.cget('selectbackground')
		self.systemColorTheme.selectforeground=self.testEntry.cget('selectforeground')
		self.systemColorTheme.correctColor()
		
	def refreshColors(self):
		self.testEntry['bg']=self.currentColorTheme.bg
		self.testEntry['foreground']=self.currentColorTheme.foreground
		self.testEntry['highlightbackground']=self.currentColorTheme.highlightbackground
		self.testEntry['highlightcolor']=self.currentColorTheme.highlightcolor
		self.testEntry['disabledforeground']=self.currentColorTheme.disabledforeground
		self.testEntry['selectbackground']=self.currentColorTheme.selectbackground
		self.testEntry['selectforeground']=self.currentColorTheme.selectforeground
		
		self.root.tk.call('option', 'add', '*background', self.currentColorTheme.bg, 'interactive')
		self.root.tk.call('option', 'add', '*foreground', self.currentColorTheme.foreground, 'interactive')
		self.root.tk.call('option', 'add', '*selectForeground', self.currentColorTheme.selectforeground, 'interactive')
		self.root.tk.call('option', 'add', '*selectBackground', self.currentColorTheme.selectbackground, 'interactive')
		self.root.tk.call('option', 'add', '*highlightBackground', self.currentColorTheme.highlightbackground, 'interactive')
		self.root.tk.call('option', 'add', '*highlightColor', self.currentColorTheme.highlightcolor, 'interactive')
	
	def setColorTheme(self, theme_name='System'):
		if theme_name=='System':
			self.currentColorTheme=self.systemColorTheme
		else:
			self.currentColorTheme=ColorTheme(app.config.preferences.color_theme)
			if self.currentColorTheme.name=='System':
				self.currentColorTheme=self.systemColorTheme			
		self.refreshColors()
	
	def getColorThemes(self):
		result=[]
		for item in os_utils.get_files(app.config.user_color_themes, 'xml'):
			result.append(item[:-4])	
		return result
	
	def getStyles(self):
		return os_utils.get_dirs(app.config.user_themes)
		
	def setApplicationIcon(self, icon='icon_sk1_16', iconname='sK1'):
		self.root.iconname(iconname)
		self.root.tk.call('wm', 'iconphoto', self.root, icon)
		
	def maximizeApp(self):
		self.root.tk.call('wm', 'attributes', self.root, '-zoomed', 1)	
	
	def resetTile(self):
		self.root.tk.call('ttk::setTheme', app.config.preferences.style)
		
	def setFonts(self):
		self.testSmallLabel['font'] = app.config.preferences.small_font
		self.testNormalLabel['font'] = app.config.preferences.normal_font 
		self.testLargeLabel['font'] = app.config.preferences.large_font 
		
	def getIconSets(self):
		return os_utils.get_dirs(app.config.user_icons)

	def loadIcons(self, iconset='CrystalSVG'):
		icons=[]
		path=os.path.join(app.config.user_icons, iconset)
		if not os.path.isdir(path):
			path=os.path.join(app.config.user_icons, self.getIconSets()[0])
		icons=os_utils.get_files_tree(path)	
		for icon in icons:
			item=os.path.basename(icon)[:-4]
			self.root.tk.call('image', 'create', 'photo', item, '-format', 'png', '-file', icon)
			
	def loadWidgetsElements(self):
		elements=[]
		path=os.path.join(app.config.user_themes, app.config.preferences.style, 'widgets')
		elements=os_utils.get_files_withpath(path,'png')
		for element in elements:
			item=os.path.basename(element)[:-4]
			self.root.tk.call('image', 'create', 'photo', item, '-format', 'png', '-file', element)		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
