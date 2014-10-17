# -*- coding: utf-8 -*-

# Copyright (C) 2009 by Igor E. Novikov
# Copyright (c) 2003 Simon Budig  <simon@gimp.org>
#
# This library is covered by GNU General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.


from sk1sdk.libttk import TFrame, TLabel, TCheckbutton, TButton
from Tkinter import IntVar
from Tkinter import RIGHT, BOTTOM, X, Y, BOTH, LEFT, TOP, W, E, DISABLED, NORMAL

from app.conf.const import SELECTION, DOCUMENT, EDITED

from app import _, config, Rect, mw
from app.conf import const
import app, math
from sk1.tkext import UpdatedButton

from sk1.pluginpanels.ppanel import PluginPanel

import base

class Outline2CurvePanel(PluginPanel):
	name='Outline2Curve'
	title = _("Outline to Curve")

	def init(self, master):
		PluginPanel.init(self, master)

		top = TFrame(self.panel, style='FlatFrame', borderwidth=5)
		top.pack(side = TOP, fill=BOTH)
		
		sign = TFrame(top, style='RoundedFrame', borderwidth=5)
		sign.pack(side = TOP)

		self.sign=TLabel(sign, image='messagebox_construct')
		self.sign.pack(side=TOP)

		button = UpdatedButton(top, text = _("Apply"),
								command = self.apply_action,
								sensitivecb = self.is_correct_selection)
		button.pack(side = BOTTOM, expand = 1, fill = X)
		self.Subscribe(SELECTION, button.Update)

		self.init_from_doc()
		self.subscribe_receivers()

###############################################################################
	def is_correct_selection(self):
		return (len(self.document.selection) ==1 and self.document.selection.GetObjects()[0].is_Bezier)
	
	def subscribe_receivers(self):
		self.document.Subscribe(SELECTION, self.init_from_doc)	
		self.document.Subscribe(EDITED, self.init_from_doc)

	def unsubscribe_receivers(self):
		self.document.Unsubscribe(SELECTION, self.init_from_doc)	
		self.document.Unsubscribe(EDITED, self.init_from_doc)

	def init_from_doc(self, *arg):
		self.issue(SELECTION)

	def apply_action(self):
		selected_objects = self.document.selection.GetObjects ()
		objects = []
		for path in selected_objects:
			if path.is_Bezier and path.has_line:
				properties = path.Properties ()
				radius = properties.line_width * 0.5
				linejoin = properties.line_join
				captype = properties.line_cap

				paths = []
				for stroke in path.paths:
					fw_segments, bw_segments = create_stroke_outline (stroke, radius,
                                                              linejoin, captype)

					if stroke.closed:
						# inner and outer side
						new_path = mksketchpath (fw_segments)
						paths.append (new_path)
						new_path = mksketchpath (bw_segments)
						paths.append (new_path)
					else:
						new_path = mksketchpath (fw_segments + bw_segments)
						paths.append (new_path)
               
				if paths:
					obj = app.PolyBezier (paths = tuple (paths))
					obj.properties.set_property ('line_cap', captype)
					obj.properties.set_property ('line_join', linejoin)
					objects.append (obj)

		if objects:
			for obj in objects:
				self.document.Insert (obj)
			self.document.SelectObject (objects)
		
instance=Outline2CurvePanel()
app.shaping_plugins.append(instance)




###################################################################
# This constant is used to calculate the length of the bezier
# tangents to approximate a circle.

CircleConstant = 4.0 / 3.0 * (math.sqrt (2) - 1)



###################################################################
# Convenience function to make the code more readable. Returns
# the length of a Vector from the origin to the given Point

def length (p):
   return p.polar ()[0]



###################################################################
# This subdivides a bezier segment at the (optional) Parameter t

def subdivide (p, t=0.5):
   assert len (p) == 4
   p01   = p[0] * (1-t) + p[1] * t
   p12   = p[1] * (1-t) + p[2] * t
   p23   = p[2] * (1-t) + p[3] * t
   p012  = p01  * (1-t) + p12  * t
   p123  = p12  * (1-t) + p23  * t
   p0123 = p012 * (1-t) + p123 * t

   return (p[0], p01, p012, p0123, p123, p23, p[3])



###################################################################
# For joining lines we need circle-segments with arbitrary
# angles, we need to subdivide the approximating bezier segments.
# Iterative approach to determine at what parameter t0 you have
# to subdivide a circle segment to get height h.

def circleparam (h):
   t0 = 0.5
   dt = 0.25

   while dt >= 0.0001:
      pt0 = subdivide ([0, CircleConstant, 1, 1], t0)[3]
      if pt0 > h:
         t0 = t0-dt
      elif pt0 < h:
         t0 = t0+dt
      else:
         break
      dt = dt / 2
   return t0



###################################################################
# This function checks, if two bezier segments are "sufficiently"
# parallel. It checks, if the points for the parameters 0.25, 0.5
# and 0.75 of the tested segment are orthogonal to the resp.
# points of the source segment. 1% tolerance is default.

# It does not check the start and endpoints, since they are
# assumed to be correct by construction.

def check_parallel (source, parallel, radius, tolerance = 0.01):
   for t0 in [0.25, 0.5, 0.75]:
      s = subdivide (source, t0)
      t = subdivide (parallel, t0)
      ccenter = (s[4] - s[3]).normalized () * radius
      orig = s[3] + app.Point (ccenter.y, - ccenter.x)

      if length (orig - t[3]) >= tolerance * radius:
         return 0

   return 1



###################################################################
# this builds a list of bezier segments that are "sufficiently"
# close to a given source segment. It recursively subdivides, if
# the check for parallelity fails.

def build_parallel (p, radius, recursionlimit=6):
   # find tangent to calculate orthogonal neighbor of endpoint
   for i in p[1:]:
      c1 = i - p[0]
      if c1:
         break
   if not c1:
      return []

   t1 = c1.normalized () * radius
   p0 = p[0] + app.Point (t1.y, -t1.x)
   c1 = p[1] - p[0]

   for i in [p[2], p[1], p[0]]:
      c2 = p[3] - i
      if c2:
         break

   t2 = c2.normalized () * radius
   p3 = p[3] + app.Point (t2.y, -t2.x)
   c2 = p[3] - p[2]
   
   sd = subdivide (p)
   center = sd[3]
   ccenter = (sd[4] - sd[3]).normalized () * radius

   new_center = center + app.Point (ccenter.y, - ccenter.x)
   now_center = subdivide ([p0, p0+c1, p3-c2, p3])[3]

   offset = (new_center - now_center) * 8.0 / 3

   det = c1.x * c2.y - c1.y * c2.x
   if det:
      ndet = det / length (c1) / length (c2)
   else:
      ndet = 0

   if math.fabs (ndet) >= 0.1:
      # "sufficiently" linear independant, cramers rule:
      oc1 = c1 * ((offset.x * c2.y - offset.y * c2.x) / det)
      oc2 = c2 * ((c1.x * offset.y - c1.y * offset.x) / det)
   else:
      # don't bother to try to correct the error, will figure out
      # soon if subdivision is necessary.
      oc1 = app.Point (0,0)
      oc2 = app.Point (0,0)

   proposed_segment = [p0, p0 + c1 + oc1, p3 - c2 + oc2, p3]
   if check_parallel (p, proposed_segment, radius) or recursionlimit <= 0:
      return proposed_segment
   else:
      # "Not parallel enough" - subdivide.
      return (build_parallel (sd[:4], radius, recursionlimit - 1) +
              build_parallel (sd[3:], radius, recursionlimit - 1)[1:])
                     


###################################################################
# This returns a list of bezier segments that joins two points
# with a given radius (fails if the radius is smaller than the
# distance between start- and endpoint). jointype is one of
#    JoinMiter, JoinRound, JoinBevel

def get_join_segment (startpoint, endpoint, radius, jointype):

   if jointype == app.const.JoinMiter:
      d = (endpoint - startpoint) * 0.5

      if not d:
         return []

      o = app.Point (d.y, -d.x).normalized ()
      h = math.sqrt (radius*radius - length (d)*length (d))

      h2 = length (d)*length (d) / h

      # Hmm - Postscript defines 10 as miter limit...
      if h2 + h > 10.433 * radius:
         # Hit miter limit
         return [startpoint, endpoint]

      edge = startpoint + d + o * h2

      return [startpoint, startpoint, edge, edge, edge, endpoint, endpoint]

   elif jointype == app.const.JoinRound:
      f = CircleConstant
      d = (endpoint - startpoint) * 0.5

      if not d:
         return []

      o = app.Point (d.y, -d.x).normalized () * radius

      h = math.sqrt (radius*radius - length (d)*length (d)) / radius

      center = startpoint + d - h * o
      d = d.normalized () * radius

      t0 = circleparam (h)
      quadseg = [center - d, center - d + f * o,
                 center - f * d + o, center + o]
      ret = [startpoint] + list (subdivide (quadseg, t0)[4:])
      quadseg = [center + o, center + o + f * d,
                 center + d + f * o, center + d]
      ret = ret + list (subdivide (quadseg, 1-t0)[1:3]) + [endpoint]

      return ret

   elif jointype == app.const.JoinBevel:
      return [startpoint, endpoint]

   else:
      raise "Unknown jointype %d" % jointype



###################################################################
# this returns a list of bezier segments that form the end cap of
# a line. valid captypes are:
#     CapButt, CapRound, CapProjecting

def get_cap_segment (startpoint, endpoint, captype):

   #  =====|
   if captype == app.const.CapButt:
      return [startpoint, endpoint]

   #  =====)
   elif captype == app.const.CapRound:
      f = CircleConstant
      d = (endpoint - startpoint) * 0.5
      o = app.Point (d.y, -d.x)

      return [startpoint, startpoint + f * o,
              startpoint + (1-f) * d + o,
              startpoint + d + o,
              startpoint + (1+f) * d + o,
              endpoint + f * o, endpoint]

   #  =====]
   elif captype == app.const.CapProjecting:
      d = (endpoint - startpoint) * 0.5
      o = app.Point (d.y, -d.x)

      # Ok, this is nasty...
      return [startpoint, startpoint,
              startpoint + o, startpoint + o, startpoint + o,
              endpoint   + o, endpoint   + o, endpoint   + o,
              endpoint, endpoint]

   else:
      raise "Unknown captype %d" % captype



###################################################################
# This function prepares a path given by a list of lists of
# coordinates for the use with app.

def mksketchpath (path, close=1):
   first_point = path[0][0]
   last_point = first_point

   new_path = app.CreatePath ()
   new_path.AppendLine (first_point, app.ContAngle)

   for seg in path:
      if seg[0] != last_point:
         print "Need to fix up! Should not happen."
         new_path.AppendLine (seg[0], app.ContAngle)

      if len (seg) == 2:
         new_path.AppendLine (seg[1], app.ContAngle)
         last_point = seg[1]

      while len (seg) >= 4:
         new_path.AppendBezier (seg[1], seg[2],
                                seg[3], app.ContAngle)
         last_point = seg[3]
         seg= seg[3:]

   if close:
      new_path.ClosePath ()
   
   return new_path

   

###################################################################
# outlines a single stroke. returns two lists of lists of bezier
# segments for both sides of the stroke.

def create_stroke_outline (stroke, radius, linejoin, captype):
   fw_segments = []
   bw_segments = []

   last_point = None

   for i in range (stroke.len):
      segment = stroke.Segment (i)
      if segment[0] == app.Line:
         if last_point:
            c1 = segment[2] - last_point
            if c1:
               t1 = c1.normalized () * radius
               fw_segments.append (
                        [last_point + app.Point (t1.y, -t1.x),
                         segment[2] + app.Point (t1.y, -t1.x)])
               bw_segments.insert (0,
                        [segment[2] - app.Point (t1.y, -t1.x),
                         last_point - app.Point (t1.y, -t1.x)])
         last_point = segment[2]

      elif segment[0] == app.Bezier:
         segments = build_parallel ([last_point, segment[1][0],
                                     segment[1][1], segment[2]],
                                     radius)
         fw_segments.append (segments)

         segments = build_parallel ([segment[2], segment[1][1],
                                     segment[1][0], last_point],
                                    radius)
         bw_segments.insert (0, segments)
         last_point = segment[2]

      else:
         raise "Unknown segment type: %s" % repr(stroke.Segment (i))
         

   # fix the connections between the parallels if necessary

   i = 0
   while i < len (fw_segments) - 1:
      if fw_segments[i][-1] != fw_segments[i+1][0]:
         fw_segments.insert (i+1,
                             get_join_segment (fw_segments[i][-1],
                                               fw_segments[i+1][0],
                                               radius, linejoin))
         i += 1
      i += 1
         
      
   i = 0
   while i < len (bw_segments) - 1:
      if bw_segments[i][-1] != bw_segments[i+1][0]:
         bw_segments.insert (i+1,
                             get_join_segment (bw_segments[i][-1],
                                               bw_segments[i+1][0],
                                               radius, linejoin))
         i += 1
      i += 1
         

   # fix the connection between both sides of a stroke.
   # depends on the state of the path.

   if stroke.closed:
      if fw_segments[0][0] != fw_segments[-1][-1]:
         fw_segments.append (get_join_segment (fw_segments[-1][-1],
                                               fw_segments[0][0],
                                               radius, linejoin))
      if bw_segments[0][0] != bw_segments[-1][-1]:
         bw_segments.append (get_join_segment (bw_segments[-1][-1],
                                               bw_segments[0][0],
                                               radius, linejoin))
   else:
      fw_segments.insert (0, get_cap_segment (bw_segments[-1][-1],
                                              fw_segments[0][0],
                                              captype))
      bw_segments.insert (0, get_cap_segment (fw_segments[-1][-1],
                                              bw_segments[0][0],
                                              captype))

   return fw_segments, bw_segments
