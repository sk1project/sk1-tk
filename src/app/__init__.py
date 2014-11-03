# -*- coding: utf-8 -*-

# Copyright (C) 2003-2006 by Igor E. Novikov
# Copyright (C) 1998, 1999, 2000, 2002 by Bernhard Herzog
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.


import os, sys, string

uimanager = None
dialogman = None
mw = None

####Info variables for progress dialogs
info1 = None
info2 = None
info3 = None
info_win = None
#######################################


objprop_plugins = []
layout_plugins = []
transform_plugins = []
effects_plugins = []
extentions_plugins = []
shaping_plugins = []
pref_plugins = []


_pkgdir = __path__[0]

temp = string.split(_pkgdir, '/')
temp.remove(temp[-1])
_parentdir = string.join(temp, '/')



#-----------LOCALIZATION-------------------
import gettext
message_dir = os.path.join(_parentdir, 'sk1', 'share', 'locales')
if os.path.lexists(message_dir):
	gettext.bindtextdomain('sk1', message_dir)
	gettext.textdomain('sk1')
_ = gettext.gettext
#-------------------------------------------


from conf import const

from _sketch import Point, Polar, PointType
NullPoint = Point(0, 0)

from conf.configurator import Configurator
config = Configurator(base_dir=_parentdir)
sKVersion = config.version

from colormanager import ColorManager
colormanager = ColorManager()


from _sketch import Rect, PointsToRect, UnionRects, IntersectRects, EmptyRect, InfinityRect, RectType
UnitRect = Rect(0, 0, 1, 1)

from _sketch import Trafo, Scale, Translation, Rotation, SingularMatrix, TrafoType
Identity = Trafo(1, 0, 0, 1, 0, 0)
IdentityMatrix = Identity.matrix()

from _sketch import CreatePath, RectanglePath, RoundedRectanglePath, approx_arc, CreateFontMetric, SKCache, TransformRectangle
from _sketch import ContAngle, ContSmooth, ContSymmetrical, SelNone, SelNodes, SelSegmentFirst, SelSegmentLast, Bezier, Line

from events.skexceptions import *
from events.undo import Undo, UndoList, CreateListUndo, CreateMultiUndo, UndoAfter, UndoRedo, NullUndo
from events.connector import Connect, Disconnect, Issue, RemovePublisher, Subscribe, Publisher, QueueingPublisher

def updateInfo(inf1=None, inf2=None, inf3=None):
	if not inf1 is None:
		info1.set(inf1)
	if not inf2 is None:
		info2.set(inf2)
	if not inf3 is None:
		info3.set(inf3)
	if not info_win is None:
		info_win.update()

command_classes = []

def RegisterCommands(aclass):
	for cmd in aclass.commands:
		cmd.SetClass(aclass)
	command_classes.append(aclass)


# from Graphics.base import GraphicsObject, Primitive

from Graphics.renderer import DocRenderer
from Graphics.arrow import StandardArrows, Arrow
from Graphics.properties import Style, FillStyle, EmptyFillStyle, LineStyle, EmptyLineStyle, PropertyStack, EmptyProperties
from Graphics.blend import MismatchError, Blend, BlendTrafo
from Graphics.blendgroup import BlendGroup, CreateBlendGroup, BlendInterpolation
from Graphics.color import CreateRGBColor, XRGBColor, CreateCMYKColor, StandardColors, ParseSKColor
from Graphics.compound import Compound, EditableCompound
from Graphics.dashes import StandardDashes
from Graphics.document import EditDocument, SelectionMode, EditMode
Document = EditDocument
from uc.libpango import get_fontface as GetFont
from Graphics.gradient import MultiGradient, CreateSimpleGradient
from Graphics.graphics import SimpleGC, GraphicsDevice, InvertingDevice, HitTestDevice
from Graphics.group import Group
from Graphics.guide import GuideLine
from Graphics.image import Image, load_image, ImageData
from Graphics.layer import Layer, GuideLayer, GridLayer
from Graphics.maskgroup import MaskGroup
from Graphics.pattern import EmptyPattern, SolidPattern, HatchingPattern, LinearGradient, RadialGradient, ConicalGradient, ImageTilePattern
from Graphics.plugobj import PluginCompound, TrafoPlugin
from Graphics.rectangle import Rectangle, RectangleCreator
from Graphics.ellipse import Ellipse, EllipseCreator
from Graphics.bezier import PolyBezier, PolyBezierCreator, PolyLineCreator, CombineBeziers, CreatePath, ContAngle, ContSmooth, ContSymmetrical
from Graphics.psdevice import PostScriptDevice
from Graphics.text import SimpleText, SimpleTextCreator, PathText

from uc import filters

def init_ui():
	# workaround for a threaded _tkinter in Python 1.5.2
	if sys.version[:5] >= '1.5.2':
		import paxtkinter
		sys.modules['_tkinter'] = paxtkinter
	Issue(None, const.INITIALIZE)

def init_modules_from_widget(root):
	import pax
	import sk1.skpixmaps, Graphics.graphics
	import sk1.tkext, Graphics.color
	sk1.tkext.InitFromTkapp(root.tk)
	if hasattr(root.tk, 'interpaddr'):
		tkwin = pax.name_to_window('.', root.tk.interpaddr())
	else:
		tkwin = pax.name_to_window('.', root.tk)
	Graphics.color.InitFromWidget(tkwin, root)
	Graphics.graphics.InitFromWidget(tkwin)
	sk1.skpixmaps.InitFromWidget(tkwin)

