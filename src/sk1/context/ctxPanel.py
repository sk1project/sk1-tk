# -*- coding: utf-8 -*-

# Copyright (C) 2008 by Igor E. Novikov
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

from sk1sdk.libttk import TFrame, TLabel
from Tkinter import LEFT, RIGHT
from app import Publisher
from app.conf.const import DOCUMENT, SELECTION, MODE
from guides_panel import GuidesPanel
from resize_panel import ResizePanel
from rotation_panel import RotatePanel
from flip_panel import FlipPanel
from unit_panel import UnitPanel
from jump_panel import JumpPanel
from page_panel import PagePanel
from image_panel import ImagePanel
from rectangle_panel import RectanglePanel
from ellipse_panel import EllipsePanel
from group_panel import GroupPanel, CombinePanel, ToCurvePanel
from text_prop_panel import TextPropPanel
from textalign_panel import TextAlignPanel
from font_panel import FontPanel
from subpanel import CtxSubPanel
from nodeedit_panel import NodeEditPanel


UNKNOWN_OBJ = -1
GROUP = 0
RECTANGLE = 1
BEZIER = 2
ELLIPSE = 3
IMAGE = 4
SIMPLE_TEXT = 5

SelectionMode = 0
EditMode = 1

forPage = ['PagePanel', 'UnitPanel', 'JumpPanel', 'GuidesPanel']
forObject = ['ResizePanel', 'UnitPanel', 'FlipPanel', 'RotatePanel', 'CombinePanel', 'ToCurvePanel']
forSimpleText = ['FontPanel', 'TextAlignPanel', 'ToCurvePanel']#,'TextPropPanel'
forGroup = ['ResizePanel', 'UnitPanel', 'FlipPanel', 'RotatePanel', 'GroupPanel', 'CombinePanel', 'ToCurvePanel']
forNodes = ['ResizePanel', 'UnitPanel', 'CombinePanel', 'NodeEditPanel']
forImage = ['ResizePanel', 'UnitPanel', 'FlipPanel', 'RotatePanel', 'ImagePanel']
forRectangle = ['ResizePanel', 'FlipPanel', 'RotatePanel', 'RectanglePanel', 'ToCurvePanel']
forEllipse = ['ResizePanel', 'FlipPanel', 'RotatePanel', 'EllipsePanel', 'ToCurvePanel']

class ContexPanel(Publisher):

	panelRegistry = {}
	currentContent = []
	current_type = ''

	def __init__(self, parent, mainwindow):
		self.parent = parent
		self.mainwindow = mainwindow
		self.doc = self.mainwindow.document
		self.panel = TFrame(self.parent, name='ctxPanel', style='ToolBarFrame', borderwidth=2)
		label = TLabel(self.panel, image="toolbar_left")
		label.pack(side=LEFT)
		self.initPanels()
		self.mainwindow.Subscribe(DOCUMENT, self.doc_changed)
		self.ReSubscribe()
		self.changeContent(forPage)

	def initPanels(self):
		for panel in PanelList:
			self.panelRegistry[panel.name] = panel(self)

	def ReSubscribe(self):
		self.doc.Subscribe(SELECTION, self.check)
		self.doc.Subscribe(MODE, self.check)
		self.check()

	def doc_changed(self, doc):
		self.doc = doc
		self.ReSubscribe()

	def changeContent(self, panelgroup):
		if not self.current_type == panelgroup:
			if len(self.currentContent):
				for panel in self.currentContent:
					panel.panel.forget()
				self.currentContent[-1].setNormal()
				self.currentContent = []
			for panelname in panelgroup:
				self.currentContent.append(self.panelRegistry[panelname])
				self.panelRegistry[panelname].panel.pack(side=LEFT)
			self.currentContent[-1].setLast()
			self.current_type = panelgroup

	def check(self):
		doc = self.mainwindow.document
		mode = doc.Mode()
#		content=forPage
		selinf = doc.selection.GetInfo()
		if len(selinf) == 0:
			self.changeContent(forPage)
		elif len(selinf) == 1:
			obj_type = self.checkObject(selinf[0][-1])
			if mode == SelectionMode:
				if obj_type == GROUP:
					self.changeContent(forGroup)
				elif obj_type == SIMPLE_TEXT:
					self.changeContent(forSimpleText)
				elif obj_type == RECTANGLE:
					self.changeContent(forObject)
				elif obj_type == ELLIPSE:
					self.changeContent(forObject)
				elif obj_type == IMAGE:
					self.changeContent(forImage)
				else:
					self.changeContent(forObject)
			else:
				if obj_type == GROUP:
					self.changeContent(forGroup)
				elif obj_type == SIMPLE_TEXT:
					self.changeContent(forSimpleText)
				elif obj_type == RECTANGLE:
					self.changeContent(forRectangle)
				elif obj_type == ELLIPSE:
					self.changeContent(forEllipse)
				elif obj_type == BEZIER:
					self.changeContent(forNodes)
				elif obj_type == IMAGE:
					self.changeContent(forImage)
				else:
					self.changeContent(forObject)
		else:
			if mode == SelectionMode:
				self.changeContent(forGroup)
			else:
				self.changeContent(forGroup)

	def checkObject(self, obj):
		if obj.is_Group:
			return GROUP
		if obj.is_Bezier:
			return BEZIER
		if obj.is_Ellipse:
			return ELLIPSE
		if obj.is_Rectangle:
			return RECTANGLE
		if obj.is_SimpleText:
			return SIMPLE_TEXT
		if obj.is_Image:
			return IMAGE
		return UNKNOWN_OBJ

PanelList = [PagePanel, ResizePanel, GuidesPanel, RotatePanel, JumpPanel,
		TextPropPanel, TextAlignPanel, FlipPanel, UnitPanel, GroupPanel,
		FontPanel, CombinePanel, ToCurvePanel, NodeEditPanel, ImagePanel,
		RectanglePanel, EllipsePanel]
