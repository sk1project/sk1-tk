/* tkcairo -  extension for pycairo context initialization
 * for Tkinter widgets under X.org
 * Copyright (C) 2014 by Igor E.Novikov
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

#include <X11/X.h>
#include <tcl.h>
#include <tk.h>
#include <Python.h>
#include <cairo-xlib.h>
#include <cairo.h>
#include <pycairo/pycairo.h>

static Pycairo_CAPI_t *Pycairo_CAPI;


static PyObject *
cairo_CreatePyCairoContext (PyObject *self, PyObject *args) {

	int width, height;
	char * tkwin_name;
	PyObject * interpaddr;
	Tcl_Interp * interp;
	Tk_Window	tkwin;
	Drawable drawable;
	Display * display;
	cairo_surface_t *winsurface;
	cairo_t *ctx;

	if (!PyArg_ParseTuple(args, "sOii", &tkwin_name, &interpaddr, &width, &height))
	return NULL;

	interp = (Tcl_Interp*)PyInt_AsLong(interpaddr);

	tkwin = Tk_NameToWindow(interp, tkwin_name, (ClientData)Tk_MainWindow(interp));
	if (!tkwin)
	{
		PyErr_SetString(PyExc_ValueError, Tcl_GetStringResult(interp));
		return NULL;
	}

	drawable = Tk_WindowId(tkwin);
	display = Tk_Display(tkwin);

	Visual *visual = DefaultVisual(display, DefaultScreen(display));
	winsurface = cairo_xlib_surface_create(display, drawable, visual, width, height);
	cairo_surface_set_device_offset(winsurface, 0, 0);
	ctx = cairo_create(winsurface);

	return PycairoContext_FromContext(ctx, &PycairoContext_Type, self);
}

static
PyMethodDef cairo_methods[] = {
	{"create_pycairo_context", cairo_CreatePyCairoContext, METH_VARARGS},
	{NULL, NULL}
};

void
init_tkcairo(void)
{
    Py_InitModule("_tkcairo", cairo_methods);
    Pycairo_IMPORT;
}
