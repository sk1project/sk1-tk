# -*- coding: utf-8 -*-

# Copyright (C) 2003-2006 by Igor E. Novikov
# Copyright (C) 1997, 1998 by Bernhard Herzog
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.

#
# Class CursorStack
#
# A mix-in class for widgets.
#
# When switching to a temporary mode like the zoom mode in SketchCanvas,
# it is a good idea to change the mouse pointer into, for instance, a
# magnifying glass, while the temporary mode is active. When the mode
# becomes inactive, i.e. when the previous mode is restored, the
# appropriate pointer has to be shown again.
#
# CursorStack provides methods for dealing with these things.
#
import types

class CursorStack:

	def __init__(self, shape = None, function = None):
		self.cursor_stack = None
		self.cursor_function = self.set_handle_cursor
		self.cursor_shape = shape
		self.last_cursor = function

	def push_static_cursor(self, cursor):
		self.push_cursor_state()		
		self.set_static_cursor(cursor)		
		

	def set_static_cursor(self, cursor):
		self.cursor_function = None
		self.cursor_shape = cursor
		self.set_window_cursor(cursor)

	def push_active_cursor(self, function, standard_shape):
		self.push_cursor_state()
		self.set_active_cursor(function, standard_shape)

	def set_active_cursor(self, function, standard_shape):
		self.cursor_function = function
		self.cursor_shape = standard_shape
		if self.winfo_ismapped():
			x, y = self.tkwin.QueryPointer()[4:6]
			self.cursor_function(x, y)

	def push_cursor_state(self):
		self.cursor_stack = (self.cursor_shape, self.cursor_function,
								self.cursor_stack)

	def pop_cursor_state(self):
		self.cursor_shape, self.cursor_function, self.cursor_stack \
							= self.cursor_stack
		if self.cursor_function:
			x, y = self.tkwin.QueryPointer()[4:6]
			self.cursor_function(x, y)
		else:
			self.set_window_cursor(self.cursor_shape)

	def set_window_cursor(self, cursor):
		if cursor != self.last_cursor:
			if type(cursor) is types.IntType:
				from sk1sdk import tkXcursor
				tkXcursor.set_cursor(self, cursor)
				self.last_cursor = cursor
			else:
				self['cursor'] = self.last_cursor = cursor
