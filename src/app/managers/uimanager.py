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
from app.conf import const
from Tkinter import StringVar

	
class ColorTheme:
	bg ='#959ba2'
	foreground ='#000000'
	highlightbackground ='#ededed'
	highlightcolor ='#000000'
	disabledforeground =None
	selectbackground ='#4e87da'
	selectforeground ='#000000'
	
	menubackground=None
	menuforeground=None
	menuselectbackground=None
	menuselectforeground=None
	menudisabledforeground=None
	menubordercolor=None
	
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
							
	def correctColor(self):
		self.disabledforeground=self.recalc(self.foreground, self.bg, 0.7)
		if self.menudisabledforeground is None:
			self.menudisabledforeground=self.disabledforeground
		if self.menubordercolor is None:
			self.menubordercolor=self.disabledforeground
				
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
		self.initGlobalVariables()
		self.createTestWidgets()
		self.systemColorTheme=ColorTheme()
		self.getSystemColors()
		self.setColorTheme(app.config.preferences.color_theme)
		self.setFonts()
		self.uploadExtentions()
		self.loadIcons()
		self.loadIcons(app.config.preferences.icons)
		self.resetTile()
		self.defineCursors()
		
	def initGlobalVariables(self):
		self.sk1_bg = StringVar(self.root, name='sk1_bg')
		self.sk1_fg = StringVar(self.root, name='sk1_fg')
		self.sk1_highlightbg = StringVar(self.root, name='sk1_highlightbg')
		self.sk1_highlightcolor = StringVar(self.root, name='sk1_highlightcolor')
		self.sk1_disabledfg = StringVar(self.root, name='sk1_disabledfg')
		self.sk1_selectbg = StringVar(self.root, name='sk1_selectbg')
		self.sk1_selectfg= StringVar(self.root, name='sk1_selectfg')
		
		self.sk1_txtsmall= StringVar(self.root, name='sk1_txtsmall')
		self.sk1_txtnormal= StringVar(self.root, name='sk1_txtnormal')
		self.sk1_txtlarge= StringVar(self.root, name='sk1_txtlarge')
		
	def defineCursors(self):
		cur_dir=os.path.join(app.config.sk_share_dir,'cursors')
		setattr(const, 'CurEdit', ('@' + os.path.join(cur_dir,'CurEdit.xbm'),'black'))
		setattr(const, 'CurZoom', ('@' + os.path.join(cur_dir,'CurZoom.xbm'),'black'))
		
	def uploadExtentions(self):
		self.root.tk.call('lappend', 'auto_path', os.path.join(app.config.sk_dir,'app'))
		self.root.tk.call('lappend', 'auto_path', app.config.sk_themes)
		self.root.tk.call('package', 'require', 'tkpng')
		tcl=os.path.join(app.config.sk_dir,'app','tcl')
		self.root.tk.call('source', os.path.join(tcl,'combobox.tcl'))
		self.root.tk.call('source', os.path.join(tcl,'button.tcl'))
		self.root.tk.call('source', os.path.join(tcl,'tkmenu.tcl'))
		self.root.tk.call('source', os.path.join(tcl,'tkfbox.tcl'))
		self.root.tk.call('source', os.path.join(tcl,'repeater.tcl'))
		self.root.tk.call('source', os.path.join(tcl,'launch_dialog.tcl'))
	
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
		
		self.systemColorTheme.menubackground = self.systemColorTheme.bg
		self.systemColorTheme.menuforeground = self.systemColorTheme.foreground
		self.systemColorTheme.menuselectbackground = self.systemColorTheme.selectbackground
		self.systemColorTheme.menuselectforeground = self.systemColorTheme.selectforeground
		
		self.systemColorTheme.correctColor()
		
	def refreshColors(self):
		self.sk1_bg.set(self.currentColorTheme.bg)
		self.sk1_fg.set(self.currentColorTheme.foreground)
		self.sk1_highlightbg.set(self.currentColorTheme.highlightbackground)
		self.sk1_highlightcolor.set(self.currentColorTheme.highlightcolor)
		self.sk1_disabledfg.set(self.currentColorTheme.disabledforeground)
		self.sk1_selectbg.set(self.currentColorTheme.selectbackground)
		self.sk1_selectfg.set(self.currentColorTheme.selectforeground)
			
		if not self.currentColorTheme.name=='System':
			self.root.tk.call('tk_setPalette', self.currentColorTheme.bg)
					
		self.root.tk.call('option', 'add', '*background', self.currentColorTheme.bg, 'interactive')
		self.root.tk.call('option', 'add', '*foreground', self.currentColorTheme.foreground, 'interactive')
		self.root.tk.call('option', 'add', '*selectForeground', self.currentColorTheme.selectforeground, 'interactive')
		self.root.tk.call('option', 'add', '*selectBackground', self.currentColorTheme.selectbackground, 'interactive')
		self.root.tk.call('option', 'add', '*highlightBackground', self.currentColorTheme.highlightbackground, 'interactive')
		self.root.tk.call('option', 'add', '*highlightColor', self.currentColorTheme.highlightcolor, 'interactive')
		
		self.root.tk.call('option', 'add', '*highlightThickness', '0', 'interactive')
		self.root.tk.call('option', 'add', '*borderWidth', '0', 'interactive')		
		
	
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
		return os_utils.get_dirs(app.config.sk_themes)
		
	def setApplicationIcon(self, icon='icon_sk1_16', iconname='sK1'):
		self.root.iconname(iconname)
		self.root.tk.call('wm', 'iconphoto', self.root, icon)
		
	def maximizeApp(self):
		self.root.tk.call('wm', 'attributes', self.root, '-zoomed', 1)	
	
	def resetTile(self):
		self.root.tk.call('ttk::setTheme', app.config.preferences.style)
		
	def setFonts(self):
		self.root.tk.call('option', 'add', '*font', app.config.preferences.normal_font )
		self.sk1_txtsmall.set(app.config.preferences.small_font)
		self.sk1_txtnormal.set(app.config.preferences.normal_font)
		self.sk1_txtlarge.set(app.config.preferences.large_font)
		
	def getIconSets(self):
		return os_utils.get_dirs(app.config.user_icons)

	def loadIcons(self, iconset='CrystalSVG'):
		icons=[]
		if iconset=='CrystalSVG':
			path=os.path.join(app.config.sk_icons, iconset)
		else:
			path=os.path.join(app.config.user_icons, iconset)
		if not os.path.isdir(path):
			path=os.path.join(app.config.sk_icons, 'CrystalSVG')
			#path=os.path.join(app.config.user_icons, self.getIconSets()[0])
		self.load_icons(path)

	def load_icons(self, path):
		icons=os_utils.get_files_tree(path)	
		for icon in icons:
			item=os.path.basename(icon)[:-4]
			self.root.tk.call('image', 'create', 'photo', item, '-format', 'png', '-file', icon)
			
	def loadWidgetsElements(self):
		elements=[]
		path=os.path.join(app.config.sk_themes, app.config.preferences.style, 'widgets')
		elements=os_utils.get_files_withpath(path,'png')
		for element in elements:
			item=os.path.basename(element)[:-4]
			self.root.tk.call('image', 'create', 'photo', item, '-format', 'png', '-file', element)		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
