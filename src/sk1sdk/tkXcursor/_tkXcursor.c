/* tkXcursor -  RGBA/animated cursor management extension 
 * for Tkinter widgets under X.org
 * Copyright (C) 2009 by Igor E.Novikov
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Library General Public
 * License as published by the Free Software Foundation; either
 * version 2 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Library General Public License for more details.
 *
 * You should have received a copy of the GNU Library General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
 */

#include <X11/Xcursor/Xcursor.h>
#include <X11/X.h>
#include <tcl.h>
#include <tk.h>
#include <Python.h>

static
PyObject * tkXcursor_IsSupportedARGB(PyObject * self, PyObject * args)
{
	char * tkwin_name;
	PyObject * interpaddr;
	Tcl_Interp * interp;
	Tk_Window	tkwin;
	Display * display;

	if (!PyArg_ParseTuple(args, "sO", &tkwin_name, &interpaddr))
	return NULL;
	
	interp = (Tcl_Interp*)PyInt_AsLong(interpaddr);

	tkwin = Tk_NameToWindow(interp, tkwin_name, (ClientData)Tk_MainWindow(interp));
	if (!tkwin)
	{
		PyErr_SetString(PyExc_ValueError, Tcl_GetStringResult(interp));
		return NULL;
	}

	display = Tk_Display(tkwin);

return PyInt_FromLong (XcursorSupportsARGB(display));
}

static
PyObject * tkXcursor_FilenameLoadCursor(PyObject * self, PyObject * args)
{
	char * filename;
	char * tkwin_name;
	PyObject * interpaddr;
	Tcl_Interp * interp;
	Tk_Window	tkwin;
	Display * display;
	
	if (!PyArg_ParseTuple(args, "sOs", &tkwin_name, &interpaddr, &filename))
	return NULL;
	
	interp = (Tcl_Interp*)PyInt_AsLong(interpaddr);

	tkwin = Tk_NameToWindow(interp, tkwin_name, (ClientData)Tk_MainWindow(interp));
	if (!tkwin)
	{
		PyErr_SetString(PyExc_ValueError, Tcl_GetStringResult(interp));
		return NULL;
	}

	display = Tk_Display(tkwin);

return PyInt_FromLong (XcursorFilenameLoadCursor(display, filename));
}

static
PyObject * tkXcursor_SetCursorByXID(PyObject * self, PyObject * args)
{
	char * tkwin_name;
	PyObject * interpaddr;
	int cursor_id;
	Tcl_Interp * interp;
	Tk_Window	tkwin;
	Drawable drawable;
	Display * display;
	Cursor cursor;
	
	if (!PyArg_ParseTuple(args, "sOi", &tkwin_name, &interpaddr, &cursor_id))
	return NULL;
	
	interp = (Tcl_Interp*)PyInt_AsLong(interpaddr);
	cursor = (Cursor)cursor_id;

	tkwin = Tk_NameToWindow(interp, tkwin_name, (ClientData)Tk_MainWindow(interp));
	if (!tkwin)
	{
		PyErr_SetString(PyExc_ValueError, Tcl_GetStringResult(interp));
		return NULL;
	}

	drawable = Tk_WindowId(tkwin);
	display = Tk_Display(tkwin);

	XDefineCursor(display, drawable, cursor);

    Py_INCREF(Py_None);
    return Py_None;
}


static
PyMethodDef tkXcursor_methods[] = {
	{"IsSupportedARGB", tkXcursor_IsSupportedARGB, METH_VARARGS},
	{"FilenameLoadCursor", tkXcursor_FilenameLoadCursor, METH_VARARGS},
	{"SetCursor", tkXcursor_SetCursorByXID, METH_VARARGS},
	{NULL, NULL}
};

void
init_tkXcursor(void)
{
    Py_InitModule("_tkXcursor", tkXcursor_methods);
}

