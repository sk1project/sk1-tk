# -*- coding: utf-8 -*-

# Copyright (C) 2009 by Igor E. Novikov
# Copyright (C) 2002 by Tamito KAJIYAMA
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.


import math
import UserDict

from app import CreatePath, Point, Rect
from app import _, Bezier, Line
from app.Graphics.bezier import split_path_at

from sk1.dialogs.sketchdlg import MessageDialog

PRECISION = 8

###   USER INTERFACE   ###

def error(context, message):
	MessageDialog(context.root, _("Warning"), message)

def get_selection(context):
	if len(context.document.selection) < 2:
		error(context, _("Two or more objects must be selected"))
		return None
	buffer = []
	for object in context.document.selection.GetObjects():
		if object.is_Rectangle or object.is_Ellipse:
			pass
		elif object.is_Bezier:
			for path in object.Paths():
				if not path.closed:
					error(context, _("Paths in polygon objects must be closed"))
					return None
		else:
			error(context,
					_("Only rectangles, ellipses and polygons must be selected"))
			return None
		buffer.append(object.AsBezier())
	return buffer

###   CURVE APPROXIMATION   ###

def approximate_path(path):
	buffer = []
	last = path.Node(0)
	for i in range(path.len):
		type, control, point, continuity = path.Segment(i)
		if type == Bezier:
			for p, t in subdivide_curve(last, control[0], control[1], point):
				buffer.append((p, i - 1.0 + t))
			buffer.append((point, float(i)))
		elif type == Line:
			buffer.append((point, float(i)))
		last = point
	return buffer

# subdivide curve recursively so that all line segments get shorter
# than the specified threshold.
def subdivide_curve(p0, p1, p2, p3, threshold=1.0, r=(0.0, 1.0)):
	buffer = []
	p10 = Point(subdivide(p0.x, p1.x), subdivide(p0.y, p1.y))
	p11 = Point(subdivide(p1.x, p2.x), subdivide(p1.y, p2.y))
	p12 = Point(subdivide(p2.x, p3.x), subdivide(p2.y, p3.y))
	p20 = Point(subdivide(p10.x, p11.x), subdivide(p10.y, p11.y))
	p21 = Point(subdivide(p11.x, p12.x), subdivide(p11.y, p12.y))
	p30 = Point(subdivide(p20.x, p21.x), subdivide(p20.y, p21.y))
	t = subdivide(r[0], r[1])
	if math.hypot(p0.x - p30.x, p0.y - p30.y) > threshold:
		buffer.extend(subdivide_curve(p0, p10, p20, p30, threshold, (r[0], t)))
	buffer.append((p30, t))
	if math.hypot(p30.x - p3.x, p30.y - p3.y) > threshold:
		buffer.extend(subdivide_curve(p30, p21, p12, p3, threshold, (t, r[1])))
	return buffer

def subdivide(m, n, t=0.5):
	return m + t * (n - m)

###   CURVE INTERSECTION   ###

def intersect_objects(objects):
	##print "intersection_objects()"
	# approximate paths of each object
	approx_paths = []
	for i in range(len(objects)):
		paths = objects[i].Paths()
		for j in range(len(paths)):
			approx_path = approximate_path(paths[j])
			if len(approx_path) < 2:
				continue
			# for better performance, group every 10 line segments
			partials = []
			for k in range(0, len(approx_path), 10):
				partial = approx_path[k:k + 11]
				partials.append((i, j, partial, coord_rect(partial)))
			if len(partials[-1]) == 1:
				partial = partials.pop()
				partials[-1].extend(partial)
			assert 1 not in map(len, partials)
			approx_paths.append(partials)
	# find intersections for each pair of approximated paths
	table = IntersectionIndex()
	for i in range(len(approx_paths)):
		for j in range(i + 1, len(approx_paths)):
			for object1, path1, approx_path1, rect1 in approx_paths[i]:
				for object2, path2, approx_path2, rect2 in approx_paths[j]:
					if rect1.overlaps(rect2):
						for p in range(1, len(approx_path1)):
							(p0, t0), (p1, t1) = approx_path1[p - 1:p + 1]
							for q in range(1, len(approx_path2)):
								(p2, t2), (p3, t3) = approx_path2[q - 1:q + 1]
								if equal(p0, p2):
									cp = p0
								elif equal(p0, p3) or \
										equal(p1, p2) or \
										equal(p1, p3):
									cp = None
								else:
									cp = intersect_lines(p0, p1, p2, p3)
								if cp is not None:
									##print "crossed at", cp
									index1 = index(cp, p0, t0, p1, t1)
									index2 = index(cp, p2, t2, p3, t3)
									table.add(object1, path1, index1, cp)
									table.add(object2, path2, index2, cp)
	table.adjust()
	# split paths at each intersection
	new_paths = []
	for i in table.keys():
		new_paths.append((i, split_paths(objects[i], table[i])))
	# collect untouched paths
	untouched_paths = []
	for i in range(len(objects)):
		paths = objects[i].Paths()
		for j in range(len(paths)):
			if not table.has_key(i) or not table[i].has_key(j):
				untouched_paths.append((i, copy(paths[j])))
	return new_paths, untouched_paths

def intersect_lines(p0, p1, p2, p3):
	a1 = p1.x - p0.x
	a2 = p3.x - p2.x
	b1 = p0.y - p1.y
	b2 = p2.y - p3.y
	if b1 * a2 - b2 * a1 == 0 or b2 * a1 - b1 * a2 == 0:
		return None
	c1 = p0.x * p1.y - p1.x * p0.y
	c2 = p2.x * p3.y - p3.x * p2.y
	cp = Point((a1 * c2 - a2 * c1) / (b1 * a2 - a1 * b2),
				(b1 * c2 - b2 * c1) / (a1 * b2 - b1 * a2))
	if in_range(cp, p0, p1) and  in_range(cp, p2, p3):
		return cp
	return None

def in_range(p, a, b):
	x_min = round(min(a.x, b.x), PRECISION)
	x_max = round(max(a.x, b.x), PRECISION)
	y_min = round(min(a.y, b.y), PRECISION)
	y_max = round(max(a.y, b.y), PRECISION)
	return x_min <= round(p.x, PRECISION) <= x_max and \
			y_min <= round(p.y, PRECISION) <= y_max

def equal(a, b):
	return round(a.x, PRECISION) == round(b.x, PRECISION) and \
			round(a.y, PRECISION) == round(b.y, PRECISION)

def coord_rect(points):
	p, t = points[0]
	x1 = x2 = p.x
	y1 = y2 = p.y
	for i in range(1, len(points)):
		p, t = points[i]
		x1 = min(x1, p.x)
		x2 = max(x2, p.x)
		y1 = min(y1, p.y)
		y2 = max(y2, p.y)
	return Rect(x1, y1, x2, y2)

def index(cp, p0, t0, p1, t1):
	if p1.x - p0.x == 0:
		return subdivide(t0, t1, (cp.y - p0.y) / (p1.y - p0.y))
	else:
		return subdivide(t0, t1, (cp.x - p0.x) / (p1.x - p0.x))

class IntersectionIndex(UserDict.UserDict):
	def add(self, object, path, index, cp):
		index_table = self[object] = self.get(object, {})
		segment_table = index_table[path] = index_table.get(path, {})
		segment = int(index)
		indexes = segment_table[segment] = segment_table.get(segment, [])
		indexes.append([index - segment, cp])
	def adjust(self):
		for index_table in self.values():
			for segment_table in index_table.values():
				for indexes in segment_table.values():
					indexes.sort()
					for i in range(len(indexes)):
						r = 1.0 - indexes[i][0]
						for j in range(i + 1, len(indexes)):
							indexes[j][0] = (indexes[j][0] - indexes[i][0]) / r

def split_paths(object, index_table):
	buffer = []
	paths = list(object.Paths())
	for i in index_table.keys():
		segments = index_table[i].keys()
		segments.sort()
		first = last = None
		for j in range(len(segments)):
			segment = segments[j]
			for index, cp in index_table[i][segment]:
				index = index + segment
				if j > 0 and segment > 0:
					index = index - segments[j - 1]
				result = split_path_at(paths[i], index)
				if paths[i].closed:
					paths[i] = result[0]
					first = cp
				else:
					paths[i] = result[1]
					path = tidy(result[0])
					if path.len > 1:
						buffer.append((last, path, cp))
				segment = 0
				last = cp
		assert first is not None
		path = tidy(paths[i])
		if path.len > 1:
			buffer.append((last, path, first))
	return buffer

def tidy(path):
	# remove redundant node at the end of the path
	if path.len > 1:
		type, control, node, cont = path.Segment(path.len - 1)
		if type == Line and equal(node, path.Node(path.len - 2)):
			new_path = CreatePath()
			for i in range(path.len - 1):
				type, control, node, cont = path.Segment(i)
				new_path.AppendSegment(type, control, node, cont)
			path = new_path
	return path

###   PATH CONCATENATION   ###

def on_line(p, a, b):
	if not in_range(p, a, b):
		return 0
	x1 = round(b.x - a.x, PRECISION)
	x2 = round(p.x - a.x, PRECISION)
	y1 = round(b.y - a.y, PRECISION)
	y2 = round(p.y - a.y, PRECISION)
	if x1 == 0:
		return x2 == 0
	if y1 == 0:
		return y2 == 0
	return round(x2 / x1, PRECISION) == round(y2 / y1, PRECISION)

def on_outline(p0, p1, object_paths):
	for approx_path in object_paths:
		for i in range(1, len(approx_path)):
			(p2, t), (p3, t) = approx_path[i - 1:i + 1]
			if on_line(p0, p2, p3) and on_line(p1, p2, p3):
				return 1
	return 0

def contained(path, object):
	approx_path = approximate_path(path)
	object_paths = map(approximate_path, object.Paths())
	for i in range(1, len(approx_path)):
		(p0, t), (p1, t) = approx_path[i - 1:i + 1]
		if not on_outline(p0, p1, object_paths):
			break
	else:
		return 1
	p0 = Point(subdivide(p0.x, p1.x), subdivide(p0.y, p1.y))
	p1 = Point(object.coord_rect.left - 1.0,
				object.coord_rect.bottom - 1.0)
	count = 0
	for approx_path in object_paths:
		for i in range(1, len(approx_path)):
			(p2, t), (p3, t) = approx_path[i - 1:i + 1]
			cp = intersect_lines(p0, p1, p2, p3)
			if cp is not None and (i == 1 or not equal(cp, p2)):
				count = count + 1
	return count % 2 == 1

def join(paths):
#	print "join()"
#	for cp1, path, cp2 in paths:
#		print cp1, "--", path.len, "--", cp2
	buffer = []
	paths = list(paths)
	while paths:
		end, path, start = paths.pop()
		circuit = find_circuit(paths, start, end, range(len(paths)), [])
		assert circuit is not None
		new_path = copy(path)
		for i in circuit:
			cp1, path, cp2 = paths[i]
			if equal(cp1, start):
				for j in range(1, path.len):
					type, control, node, cont = path.Segment(j)
					new_path.AppendSegment(type, control, node, cont)
				start = cp2
			elif equal(cp2, start):
				last_type, last_control, node, cont = path.Segment(path.len - 1)
				for j in range(path.len - 2, -1, -1):
					type, control, node, cont = path.Segment(j)
					if last_type == Bezier:
						last_control = (last_control[1], last_control[0])
					new_path.AppendSegment(last_type, last_control, node, cont)
					last_type = type
					last_control = control
				start = cp1
			else:
				raise RuntimeError, "should not reach here"
			paths[i] = None
		new_path.ClosePath()
		buffer.append(new_path)
		paths = filter(lambda x: x is not None, paths)
	return buffer

def find_circuit(paths, start, end, rest, circuit):
	candidates = []
	for i in rest:
		cp1, path, cp2 = paths[i]
		if equal(cp1, start):
			candidates.append((i, cp2))
		elif equal(cp2, start):
			candidates.append((i, cp1))
	if not candidates:
		if equal(start, end):
			return circuit
		return None
	longest_circuit = []
	for i, next in candidates:
		rest.remove(i)
		new_circuit = find_circuit(paths, next, end, rest, circuit + [i])
		if new_circuit is not None and len(longest_circuit) < len(new_circuit):
			longest_circuit = new_circuit
		rest.append(i)
	return longest_circuit

def copy(path):
	new_path = CreatePath()
	for i in range(path.len):
		type, control, node, cont = path.Segment(i)
		new_path.AppendSegment(type, control, node, cont)
	return new_path
