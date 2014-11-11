# -*- coding: utf-8 -*-

# Copyright (C) 2003-2006 by Igor E. Novikov
# Copyright (C) 1997, 1998, 1999 by Bernhard Herzog
#
# This library is covered by GNU Library General Public License.
# For more info see COPYRIGHTS file in sK1 root directory.


# A (Tkinter-) variable holding a length, i. e. a number and a unit.
# This is implemented with two Tkinter variable, a DoubleVar and a
# StringVar. The DoubleVar can be used for a Tk Entry widget and the
# StringVar, describing the unit, can be used for an OptionMenu.
# Internally the length is always represented as a length in PSpoint
# units (1/72 inch).
#
# XXX: This needs a cleaner reimplementation

from types import TupleType

from Tkinter import TclError, StringVar, DoubleVar
from Tkinter import RIGHT, E

from app import config
from app.Lib.units import unit_dict, unit_names

from sk1.ttk_ext import TComboSmall, TSpinbox
from sk1.tkext import UnitLabel



class LengthVar:

	def __init__(self, length, unit, number_var=None, unit_var=None,
					command=None, args=(),
					precision=config.preferences.drawing_precision):
		self.length = length
		self.number_var = number_var
		self.unit = unit
		self.precision = precision
		self.unit_var = unit_var
		self.callback = command
		if type(args) != TupleType:
			args = (args,)
		self.args = args
		self.set_vars()

	def __del__(self):
		pass

	def set_vars(self):
		number = self.length / unit_dict[self.unit]
		if self.number_var:
			self.number_var.set(round(number, self.precision))
		if self.unit_var:
			self.unit_var.set(self.unit)

	def get(self):
		try:
			number = self.number_var.get()
			self.length = number * unit_dict[self.unit]
		except TclError:
			pass
		return self.length

	def set(self, length):
		self.length = length
		self.set_vars()

	def UpdateUnit(self, unit=None):
		if unit is None:
			self.unit = self.unit_var.get()
		else:
			self.unit = unit
		self.set_vars()

	def UpdateNumber(self, number=None):
		try:
			number = self.number_var.get()
		except TclError:
			pass
		self.length = number * unit_dict[self.unit]
		self.set_vars()
		self.call_callback()

	def Factor(self):
		return unit_dict[self.unit]

	def UnitName(self):
		return self.unit

	def call_callback(self):
		if self.callback:
			apply(self.callback, (self.length,) + self.args)




def create_unit_menu(master, command, variable=None, **options):
	optmenu = TComboSmall(master, unit_names, command=command, variable=variable)
	optmenu.configure(options)
	return optmenu

def create_length_widgets(top, master, command):
	var_number = DoubleVar(top)
	var_unit = StringVar(top)
	var_length = LengthVar(1.0, config.preferences.default_unit, var_number, var_unit, command=command)
	entry = TSpinbox(master, textvariable=var_number, vartype=1, min=0, max=50000, step=.1, width=6, command=var_length.UpdateNumber)
	unitlabel = UnitLabel(master)
	return var_length, entry, unitlabel



def create_length_entry(top, master, command, scroll_pad=2):
	var, entry, unitlabel = create_length_widgets(top, master, command)
	unitlabel.pack(side=RIGHT, expand=0, anchor=E)
	entry.pack(side=RIGHT, expand=0, anchor=E, padx=2)

	return var
