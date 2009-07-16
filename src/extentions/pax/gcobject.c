#include "Python.h"
#include <tk.h>
#include <X11/X.h>
#include <X11/Xlib.h>
#include <X11/Xutil.h>

#include "tkwinobject.h"
#include "gcobject.h"
#include "pixmapobject.h"
#include "regionobject.h"
#include "fontobject.h"
#include "imageobject.h"
#include "clipmask.h"
#include "paxutil.h"

#ifndef offsetof
#define offsetof(type, member) ( (int) & ((type*)0) -> member )
#endif


#define OFF(member) offsetof(XGCValues, member)
static struct GCattr {
	char *type;
	char *name;
	int offset;
	unsigned long mask;
} GCattrdefs[] = {
	{"int", "function", OFF(function), GCFunction},
	{"unsigned long", "plane_mask", OFF(plane_mask), GCPlaneMask},
	{"unsigned long", "foreground", OFF(foreground), GCForeground},
	{"unsigned long", "background", OFF(background), GCBackground},
	{"int", "line_width", OFF(line_width), GCLineWidth},
	{"int", "line_style", OFF(line_style), GCLineStyle},
	{"int", "cap_style", OFF(cap_style), GCCapStyle},
	{"int", "join_style", OFF(join_style), GCJoinStyle},
	{"int", "fill_style", OFF(fill_style), GCFillStyle},
	{"int", "fill_rule", OFF(fill_rule), GCFillRule},
	{"int", "arc_mode", OFF(arc_mode), GCArcMode},
	{"Pixmap", "tile", OFF(tile), GCTile},
	{"Pixmap", "stipple", OFF(stipple), GCStipple},
	{"int", "ts_x_origin", OFF(ts_x_origin), GCTileStipXOrigin},
	{"int", "ts_y_origin", OFF(ts_y_origin), GCTileStipYOrigin},
	{"Font", "font", OFF(font), GCFont},
	{"int", "subwindow_mode", OFF(subwindow_mode), GCSubwindowMode},
	{"Bool", "graphics_exposures", OFF(graphics_exposures),
		 					GCGraphicsExposures},
	{"int", "clip_x_origin", OFF(clip_x_origin), GCClipXOrigin},
	{"int", "clip_y_origin", OFF(clip_y_origin), GCClipYOrigin},
	{"Pixmask", "clip_mask", OFF(clip_mask), GCClipMask},
	{"int", "dash_offset", OFF(dash_offset), GCDashOffset},
	{"char", "dashes", OFF(dashes), GCDashList},
	{NULL}
};
#undef OFF

int
PaxGC_MakeValues(PyObject *dict, unsigned long *pmask, XGCValues *pvalues)
{
    Py_ssize_t pos;
    struct GCattr *p;
    PyObject *key, *value;
    if (dict == NULL || !PyDict_Check(dict))
    {
	PyErr_SetString(PyExc_TypeError, "XGCValues should be dictionary");
	return 0;
    }
    *pmask = 0;
    pos = 0;
    while (PyDict_Next(dict, &pos, &key, &value))
    {
	char *name;
	if (!PyString_Check(key))
	{
	    PyErr_SetString(PyExc_TypeError,
			    "XGCValues' keys should be strings");
	    return 0;
	}
	name = PyString_AsString(key);
	for (p = GCattrdefs; ; p++)
	{
	    if (p->name == NULL)
	    {
		PyErr_SetString(PyExc_TypeError,
				"XGCValues contains unknown name");
		return 0;
	    }
	    if (strcmp(name, p->name) != 0)
		continue;
	    *pmask |= p->mask;
	    if (strcmp(p->type, "Pixmap") == 0)
	    {
		if (!PaxPixmap_Check(value))
		{
		    PyErr_SetString(PyExc_TypeError,
				"XGCValues should map to int, Pixmap or Font");
		    return 0;
		}
		*(Pixmap*)((char*)pvalues+p->offset)=PaxPixmap_AsPixmap(value);
	    }
	    else if (strcmp(p->type, "Font") == 0)
	    {
		if (!PaxFont_Check(value))
		{
		    PyErr_SetString(PyExc_TypeError, "XGCValues should map to "
				    "int, Pixmap or Font");
		    return 0;
		}
		*(Font*)((char*)pvalues+p->offset) = PaxFont_AsFont(value);
	    }
	    else
	    {
		if (!PyInt_Check(value))
		{
		    PyErr_SetString(PyExc_TypeError,
				"XGCValues should map to int, Pixmap or Font");
		    return 0;
		}
		if (p->type[0] == 'c')
		    *((char*)pvalues + p->offset) = PyInt_AsLong(value);
		else
		    /* XXX Assume sizeof(int) == sizeof(long)! */
		    *(long*)((char*)pvalues + p->offset) = PyInt_AsLong(value);
	    }
	    break;
	}
    }
    return 1;
}


static int
pax_checkcharlist(PyObject *list, char **parray, int *pnitems)
{
    int i, n;
    if (!PyList_Check(list))
    {
	PyErr_SetString(PyExc_TypeError, "list of ints expected");
	return 0;
    }

    n = PyList_Size(list);
    *pnitems = n;
    *parray = PyMem_Malloc(n);
    if (*parray == NULL)
    {
	PyErr_NoMemory();
	return 0;
    }

    for (i = 0; i < n; i++)
    {
	PyObject *item = PyList_GetItem(list, i);
	if (!PyInt_Check(item))
	{
	    PyMem_Free(*parray);
	    PyErr_SetString(PyExc_TypeError, "list of ints expected");
	    return 0;
	}
	(*parray)[i] = PyInt_AsLong(item);
    }
    return 1;
}


extern PyTypeObject PaxGCType; /* Really forward */

GC
PaxGC_AsGC(PyObject *gcobj)
{
    if (!PaxGC_Check(gcobj))
    {
	PyErr_BadInternalCall();
	return (GC) NULL;
    }

    return ((PaxGCObject *) gcobj)->gc;
}

PyObject *
PaxGC_FromGC(Display *display, Drawable drawable, GC gc, int shared,
	     PyObject * drawable_object)
{
    PaxGCObject *gp = PyObject_New(PaxGCObject, &PaxGCType);
    if (gp == NULL)
	return NULL;
    gp->display = display;
    gp->drawable = drawable;
    gp->gc = gc;
    gp->shared = shared;
    gp->drawable_object = drawable_object;
    gp->cairo = NULL;
    gp->cairo_pattern = NULL;
    Py_XINCREF(gp->drawable_object);

    return (PyObject *)gp;
}


static PyObject *
PaxGC_SetDrawable(PaxGCObject * self, PyObject * args)
{
    PyObject * obj;

    if (!PyArg_ParseTuple(args, "O", &obj))
	return NULL;

    if (PaxPixmap_Check(obj))
    {
	Py_XDECREF(self->drawable_object);
	self->drawable = PaxPixmap_AsPixmap(obj);
	self->drawable_object = obj;
	Py_INCREF(self->drawable_object);
    }
    else if (TkWin_Check(obj))
    {
	self->drawable = TkWin_AsWindowID(obj);
	Py_XDECREF(self->drawable_object);
	self->drawable_object = NULL;
    }
    else
    {
	PyErr_SetString(PyExc_TypeError,
			"The new drawable must be a Tkwindow or a pixmap");
	return NULL;
    }

    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *
PaxGC_SetDashes(PaxGCObject * self, PyObject * args)
{
    PyObject * list;
    char * dashes;
    int num_dashes;
    int dash_offset = 0;

    if (!PyArg_ParseTuple(args, "O|i", &list, &dash_offset))
	return NULL;

    if (!pax_checkcharlist(list, &dashes, &num_dashes))
	return NULL;

    XSetDashes(self->display, self->gc, dash_offset, dashes, num_dashes);
    PyMem_Free(dashes);

    Py_INCREF(Py_None);
    return Py_None;
}


static PyObject *
PaxGC_SetForegroundAndFill(PaxGCObject *self, PyObject *args)
{
    PyObject * pixel_or_pixmap;

    if (self->shared != PAXGC_OWNED)
    {
	PyErr_SetString(PyExc_TypeError, "can't modify shared GC");
	return NULL;
    }
    if (!PyArg_ParseTuple(args, "O", &pixel_or_pixmap))
	return NULL;
    if (PyInt_Check(pixel_or_pixmap))
    {
	XSetForeground(self->display, self->gc, PyInt_AsLong(pixel_or_pixmap));
	XSetFillStyle(self->display, self->gc, FillSolid);
    }
    else if (PaxPixmap_Check(pixel_or_pixmap))
    {
	XSetTile(self->display, self->gc, PaxPixmap_AsPixmap(pixel_or_pixmap));
	XSetFillStyle(self->display, self->gc, FillTiled);
    }
    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *
PaxGC_SetClipMask(PaxGCObject *self, PyObject *args)
{
    PyObject *object;

    if (self->shared)
    {
	PyErr_SetString(PyExc_TypeError, "can't modify shared GC");
	return NULL;
    }
    if (!PyArg_ParseTuple(args, "O", &object))
	return NULL;
    if (PaxPixmap_CheckOpt(object))
    {
	XSetClipMask(self->display, self->gc, PaxPixmap_AsPixmapOpt(object));
    }
    else if (PaxRegion_Check(object))
    {
	XSetRegion(self->display, self->gc, PaxRegion_AsRegion(object));
    }
    else
    {
	PyErr_SetString(PyExc_TypeError,
		     "arg must be a region, a bitmap o a clkip mask object");
	return NULL;
    }

    Py_INCREF(Py_None);
    return Py_None;
}


#ifndef PAX_NO_XSHM
static PyObject *
PaxGC_ShmPutImage(PaxGCObject *self, PyObject *args)
{
    PyObject *image;
    int srcx;
    int srcy;
    int destx;
    int desty;
    unsigned int width;
    unsigned int height;
    int send_event;
    if (!PyArg_ParseTuple(args, "O!iiiiiii", &PaxImageType, &image,
			  &srcx, &srcy, &destx, &desty, &width, &height,
			  &send_event))
	return NULL;
    XShmPutImage(self->display, self->drawable, self->gc,
		 PaxImage_AsImage(image), srcx, srcy, destx, desty,
		 width, height, send_event);
    Py_INCREF(Py_None);
    return Py_None;
}
#else
static PyObject *
PaxGC_ShmPutImage(PaxGCObject *self, PyObject *args)
{
    PyErr_SetString(PyExc_RuntimeError,
		    "gcobject compiled without XShm support");
    return NULL;
}
#endif /* PAX_NO_XSHM */


// #include "gcmethods.c"
// ====================================================
/* automatically generated by Generate/mkgc.py */
/* Methods for PaxGC objects */

#define checkshortlist pax_checkshortlist
#define checkdoublelist pax_checkdoublelist


static PyObject *
PaxGC_DrawArc(PaxGCObject * self, PyObject *args)
{
	int arg1;
	int arg2;
	unsigned int arg3;
	unsigned int arg4;
	int arg5;
	int arg6;
	if (!PyArg_ParseTuple(args, "iiiiii",
			&arg1,
			&arg2,
			&arg3,
			&arg4,
			&arg5,
			&arg6))
		return NULL;
XDrawArc(self->display, self->drawable, self->gc,
			arg1,
			arg2,
			arg3,
			arg4,
			arg5,
			arg6);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_DrawArcs(PaxGCObject * self, PyObject *args)
{
	PyObject *arg1; XArc *arcs_arg1; int narcs_arg1;
	if (!PyArg_ParseTuple(args, "O",
			&arg1))
		return NULL;
	if (!checkshortlist(6, arg1, (short**)&arcs_arg1, &narcs_arg1)) {
		if (!PyErr_Occurred())
			PyErr_SetString(PyExc_TypeError, "arg1 should be XArc[]");
		return NULL;
	}
XDrawArcs(self->display, self->drawable, self->gc,
			arcs_arg1, narcs_arg1);
	PyMem_Free(arcs_arg1);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_DrawImageString(PaxGCObject * self, PyObject *args)
{
	int arg1;
	int arg2;
	PyObject *arg3; int nchars;
	if (!PyArg_ParseTuple(args, "iiS",
			&arg1,
			&arg2,
			&arg3))
		return NULL;
	if (!(nchars = PyString_Size(arg3), 1)) {
		if (!PyErr_Occurred())
			PyErr_SetString(PyExc_TypeError, "arg3 should be char[]");
		return NULL;
	}
XDrawImageString(self->display, self->drawable, self->gc,
			arg1,
			arg2,
			PyString_AsString(arg3), nchars);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_DrawLine(PaxGCObject * self, PyObject *args)
{
	int arg1;
	int arg2;
	int arg3;
	int arg4;
	if (!PyArg_ParseTuple(args, "iiii",
			&arg1,
			&arg2,
			&arg3,
			&arg4))
		return NULL;
XDrawLine(self->display, self->drawable, self->gc,
			arg1,
			arg2,
			arg3,
			arg4);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_DrawLines(PaxGCObject * self, PyObject *args)
{
	PyObject *arg1; XPoint *pts_arg1; int npts_arg1;
	int arg2;
	if (!PyArg_ParseTuple(args, "Oi",
			&arg1,
			&arg2))
		return NULL;
	if (!checkshortlist(2, arg1, (short**)&pts_arg1, &npts_arg1)) {
		if (!PyErr_Occurred())
			PyErr_SetString(PyExc_TypeError, "arg1 should be XPoint[]");
		return NULL;
	}
XDrawLines(self->display, self->drawable, self->gc,
			pts_arg1, npts_arg1,
			arg2);
	PyMem_Free(pts_arg1);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_DrawPoint(PaxGCObject * self, PyObject *args)
{
	int arg1;
	int arg2;
	if (!PyArg_ParseTuple(args, "ii",
			&arg1,
			&arg2))
		return NULL;
XDrawPoint(self->display, self->drawable, self->gc,
			arg1,
			arg2);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_DrawPoints(PaxGCObject * self, PyObject *args)
{
	PyObject *arg1; XPoint *pts_arg1; int npts_arg1;
	int arg2;
	if (!PyArg_ParseTuple(args, "Oi",
			&arg1,
			&arg2))
		return NULL;
	if (!checkshortlist(2, arg1, (short**)&pts_arg1, &npts_arg1)) {
		if (!PyErr_Occurred())
			PyErr_SetString(PyExc_TypeError, "arg1 should be XPoint[]");
		return NULL;
	}
XDrawPoints(self->display, self->drawable, self->gc,
			pts_arg1, npts_arg1,
			arg2);
	PyMem_Free(pts_arg1);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_DrawRectangle(PaxGCObject * self, PyObject *args)
{
	int arg1;
	int arg2;
	unsigned int arg3;
	unsigned int arg4;
	if (!PyArg_ParseTuple(args, "iiii",
			&arg1,
			&arg2,
			&arg3,
			&arg4))
		return NULL;
XDrawRectangle(self->display, self->drawable, self->gc,
			arg1,
			arg2,
			arg3,
			arg4);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_DrawRectangles(PaxGCObject * self, PyObject *args)
{
	PyObject *arg1; XRectangle *rects_arg1; int nrects_arg1;
	if (!PyArg_ParseTuple(args, "O",
			&arg1))
		return NULL;
	if (!checkshortlist(4, arg1, (short**)&rects_arg1, &nrects_arg1)) {
		if (!PyErr_Occurred())
			PyErr_SetString(PyExc_TypeError, "arg1 should be XRectangle[]");
		return NULL;
	}
XDrawRectangles(self->display, self->drawable, self->gc,
			rects_arg1, nrects_arg1);
	PyMem_Free(rects_arg1);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_DrawSegments(PaxGCObject * self, PyObject *args)
{
	PyObject *arg1; XSegment *segs_arg1; int nsegs_arg1;
	if (!PyArg_ParseTuple(args, "O",
			&arg1))
		return NULL;
	if (!checkshortlist(4, arg1, (short**)&segs_arg1, &nsegs_arg1)) {
		if (!PyErr_Occurred())
			PyErr_SetString(PyExc_TypeError, "arg1 should be XSegment[]");
		return NULL;
	}
XDrawSegments(self->display, self->drawable, self->gc,
			segs_arg1, nsegs_arg1);
	PyMem_Free(segs_arg1);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_DrawString(PaxGCObject * self, PyObject *args)
{
	int arg1;
	int arg2;
	PyObject *arg3; int nchars;
	if (!PyArg_ParseTuple(args, "iiS",
			&arg1,
			&arg2,
			&arg3))
		return NULL;
	if (!(nchars = PyString_Size(arg3), 1)) {
		if (!PyErr_Occurred())
			PyErr_SetString(PyExc_TypeError, "arg3 should be char[]");
		return NULL;
	}
XDrawString(self->display, self->drawable, self->gc,
			arg1,
			arg2,
			PyString_AsString(arg3), nchars);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_FillArc(PaxGCObject * self, PyObject *args)
{
	int arg1;
	int arg2;
	unsigned int arg3;
	unsigned int arg4;
	int arg5;
	int arg6;
	if (!PyArg_ParseTuple(args, "iiiiii",
			&arg1,
			&arg2,
			&arg3,
			&arg4,
			&arg5,
			&arg6))
		return NULL;
XFillArc(self->display, self->drawable, self->gc,
			arg1,
			arg2,
			arg3,
			arg4,
			arg5,
			arg6);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_FillArcs(PaxGCObject * self, PyObject *args)
{
	PyObject *arg1; XArc *arcs_arg1; int narcs_arg1;
	if (!PyArg_ParseTuple(args, "O",
			&arg1))
		return NULL;
	if (!checkshortlist(6, arg1, (short**)&arcs_arg1, &narcs_arg1)) {
		if (!PyErr_Occurred())
			PyErr_SetString(PyExc_TypeError, "arg1 should be XArc[]");
		return NULL;
	}
XFillArcs(self->display, self->drawable, self->gc,
			arcs_arg1, narcs_arg1);
	PyMem_Free(arcs_arg1);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_FillPolygon(PaxGCObject * self, PyObject *args)
{
	PyObject *arg1; XPoint *pts_arg1; int npts_arg1;
	int arg2;
	int arg3;
	if (!PyArg_ParseTuple(args, "Oii",
			&arg1,
			&arg2,
			&arg3))
		return NULL;
	if (!checkshortlist(2, arg1, (short**)&pts_arg1, &npts_arg1)) {
		if (!PyErr_Occurred())
			PyErr_SetString(PyExc_TypeError, "arg1 should be XPoint[]");
		return NULL;
	}
XFillPolygon(self->display, self->drawable, self->gc,
			pts_arg1, npts_arg1,
			arg2,
			arg3);
	PyMem_Free(pts_arg1);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_FillRectangle(PaxGCObject * self, PyObject *args)
{
	int arg1;
	int arg2;
	unsigned int arg3;
	unsigned int arg4;
	if (!PyArg_ParseTuple(args, "iiii",
			&arg1,
			&arg2,
			&arg3,
			&arg4))
		return NULL;
XFillRectangle(self->display, self->drawable, self->gc,
			arg1,
			arg2,
			arg3,
			arg4);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_FillRectangles(PaxGCObject * self, PyObject *args)
{
	PyObject *arg1; XRectangle *rects_arg1; int nrects_arg1;
	if (!PyArg_ParseTuple(args, "O",
			&arg1))
		return NULL;
	if (!checkshortlist(4, arg1, (short**)&rects_arg1, &nrects_arg1)) {
		if (!PyErr_Occurred())
			PyErr_SetString(PyExc_TypeError, "arg1 should be XRectangle[]");
		return NULL;
	}
XFillRectangles(self->display, self->drawable, self->gc,
			rects_arg1, nrects_arg1);
	PyMem_Free(rects_arg1);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_PutImage(PaxGCObject * self, PyObject *args)
{
	PyObject *arg1;
	int arg2;
	int arg3;
	int arg4;
	int arg5;
	int arg6;
	int arg7;
	if (!PyArg_ParseTuple(args, "Oiiiiii",
			&arg1,
			&arg2,
			&arg3,
			&arg4,
			&arg5,
			&arg6,
			&arg7))
		return NULL;
	if (!PaxImage_Check(arg1)) {
		if (!PyErr_Occurred())
			PyErr_SetString(PyExc_TypeError, "arg1 should be XImage");
		return NULL;
	}
XPutImage(self->display, self->drawable, self->gc,
			PaxImage_AsImage(arg1),
			arg2,
			arg3,
			arg4,
			arg5,
			arg6,
			arg7);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_ChangeGC(PaxGCObject *self, PyObject*args)
{
	PyObject *arg1; unsigned long mask; XGCValues values;
	if (self->shared) {
		PyErr_SetString(PyExc_TypeError, "can't modify shared GC");
		return NULL;
	}
	if (!PyArg_ParseTuple(args, "O",
			&arg1))
		return NULL;
	if (!PaxGC_MakeValues(arg1, &mask, &values)) {
		if (!PyErr_Occurred())
			PyErr_SetString(PyExc_TypeError, "arg1 should be XGCValues#");
		return NULL;
	}
XChangeGC(self->display, self->gc,
			mask, &values);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_SetArcMode(PaxGCObject *self, PyObject*args)
{
	int arg1;
	if (self->shared) {
		PyErr_SetString(PyExc_TypeError, "can't modify shared GC");
		return NULL;
	}
	if (!PyArg_ParseTuple(args, "i",
			&arg1))
		return NULL;
XSetArcMode(self->display, self->gc,
			arg1);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_SetBackground(PaxGCObject *self, PyObject*args)
{
	unsigned long arg1;
	if (self->shared) {
		PyErr_SetString(PyExc_TypeError, "can't modify shared GC");
		return NULL;
	}
	if (!PyArg_ParseTuple(args, "l",
			&arg1))
		return NULL;
XSetBackground(self->display, self->gc,
			arg1);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_SetClipOrigin(PaxGCObject *self, PyObject*args)
{
	int arg1;
	int arg2;
	if (self->shared) {
		PyErr_SetString(PyExc_TypeError, "can't modify shared GC");
		return NULL;
	}
	if (!PyArg_ParseTuple(args, "ii",
			&arg1,
			&arg2))
		return NULL;
XSetClipOrigin(self->display, self->gc,
			arg1,
			arg2);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_SetClipRectangles(PaxGCObject *self, PyObject*args)
{
	int arg1;
	int arg2;
	PyObject *arg3; XRectangle *rects_arg3; int nrects_arg3;
	int arg4;
	if (self->shared) {
		PyErr_SetString(PyExc_TypeError, "can't modify shared GC");
		return NULL;
	}
	if (!PyArg_ParseTuple(args, "iiOi",
			&arg1,
			&arg2,
			&arg3,
			&arg4))
		return NULL;
	if (!checkshortlist(4, arg3, (short**)&rects_arg3, &nrects_arg3)) {
		if (!PyErr_Occurred())
			PyErr_SetString(PyExc_TypeError, "arg3 should be XRectangle[]");
		return NULL;
	}
XSetClipRectangles(self->display, self->gc,
			arg1,
			arg2,
			rects_arg3, nrects_arg3,
			arg4);
	PyMem_Free(rects_arg3);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_SetFillRule(PaxGCObject *self, PyObject*args)
{
	int arg1;
	if (self->shared) {
		PyErr_SetString(PyExc_TypeError, "can't modify shared GC");
		return NULL;
	}
	if (!PyArg_ParseTuple(args, "i",
			&arg1))
		return NULL;
XSetFillRule(self->display, self->gc,
			arg1);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_SetFillStyle(PaxGCObject *self, PyObject*args)
{
	int arg1;
	if (self->shared) {
		PyErr_SetString(PyExc_TypeError, "can't modify shared GC");
		return NULL;
	}
	if (!PyArg_ParseTuple(args, "i",
			&arg1))
		return NULL;
XSetFillStyle(self->display, self->gc,
			arg1);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_SetFont(PaxGCObject *self, PyObject*args)
{
	PyObject *arg1;
	if (self->shared) {
		PyErr_SetString(PyExc_TypeError, "can't modify shared GC");
		return NULL;
	}
	if (!PyArg_ParseTuple(args, "O",
			&arg1))
		return NULL;
	if (!PaxFont_Check(arg1)) {
		if (!PyErr_Occurred())
			PyErr_SetString(PyExc_TypeError, "arg1 should be Font");
		return NULL;
	}
XSetFont(self->display, self->gc,
			PaxFont_AsFont(arg1));
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_SetForeground(PaxGCObject *self, PyObject*args)
{
	unsigned long arg1;
	if (self->shared) {
		PyErr_SetString(PyExc_TypeError, "can't modify shared GC");
		return NULL;
	}
	if (!PyArg_ParseTuple(args, "l",
			&arg1))
		return NULL;
XSetForeground(self->display, self->gc,
			arg1);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_SetFunction(PaxGCObject *self, PyObject*args)
{
	int arg1;
	if (self->shared) {
		PyErr_SetString(PyExc_TypeError, "can't modify shared GC");
		return NULL;
	}
	if (!PyArg_ParseTuple(args, "i",
			&arg1))
		return NULL;
XSetFunction(self->display, self->gc,
			arg1);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_SetGraphicsExposures(PaxGCObject *self, PyObject*args)
{
	int arg1;
	if (self->shared) {
		PyErr_SetString(PyExc_TypeError, "can't modify shared GC");
		return NULL;
	}
	if (!PyArg_ParseTuple(args, "i",
			&arg1))
		return NULL;
XSetGraphicsExposures(self->display, self->gc,
			(Bool)arg1);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_SetLineAttributes(PaxGCObject *self, PyObject*args)
{
	unsigned int arg1;
	int arg2;
	int arg3;
	int arg4;
	if (self->shared) {
		PyErr_SetString(PyExc_TypeError, "can't modify shared GC");
		return NULL;
	}
	if (!PyArg_ParseTuple(args, "iiii",
			&arg1,
			&arg2,
			&arg3,
			&arg4))
		return NULL;
XSetLineAttributes(self->display, self->gc,
			arg1,
			arg2,
			arg3,
			arg4);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_SetPlaneMask(PaxGCObject *self, PyObject*args)
{
	unsigned long arg1;
	if (self->shared) {
		PyErr_SetString(PyExc_TypeError, "can't modify shared GC");
		return NULL;
	}
	if (!PyArg_ParseTuple(args, "l",
			&arg1))
		return NULL;
XSetPlaneMask(self->display, self->gc,
			arg1);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_SetRegion(PaxGCObject *self, PyObject*args)
{
	PyObject *arg1;
	if (self->shared) {
		PyErr_SetString(PyExc_TypeError, "can't modify shared GC");
		return NULL;
	}
	if (!PyArg_ParseTuple(args, "O",
			&arg1))
		return NULL;
	if (!PaxRegion_Check(arg1)) {
		if (!PyErr_Occurred())
			PyErr_SetString(PyExc_TypeError, "arg1 should be Region");
		return NULL;
	}
XSetRegion(self->display, self->gc,
			PaxRegion_AsRegion(arg1));
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_SetState(PaxGCObject *self, PyObject*args)
{
	unsigned long arg1;
	unsigned long arg2;
	int arg3;
	unsigned long arg4;
	if (self->shared) {
		PyErr_SetString(PyExc_TypeError, "can't modify shared GC");
		return NULL;
	}
	if (!PyArg_ParseTuple(args, "llil",
			&arg1,
			&arg2,
			&arg3,
			&arg4))
		return NULL;
XSetState(self->display, self->gc,
			arg1,
			arg2,
			arg3,
			arg4);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_SetStipple(PaxGCObject *self, PyObject*args)
{
	PyObject *arg1;
	if (self->shared) {
		PyErr_SetString(PyExc_TypeError, "can't modify shared GC");
		return NULL;
	}
	if (!PyArg_ParseTuple(args, "O",
			&arg1))
		return NULL;
	if (!PaxPixmap_Check(arg1)) {
		if (!PyErr_Occurred())
			PyErr_SetString(PyExc_TypeError, "arg1 should be Pixmap");
		return NULL;
	}
XSetStipple(self->display, self->gc,
			PaxPixmap_AsPixmap(arg1));
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_SetSubwindowMode(PaxGCObject *self, PyObject*args)
{
	int arg1;
	if (self->shared) {
		PyErr_SetString(PyExc_TypeError, "can't modify shared GC");
		return NULL;
	}
	if (!PyArg_ParseTuple(args, "i",
			&arg1))
		return NULL;
XSetSubwindowMode(self->display, self->gc,
			arg1);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_SetTSOrigin(PaxGCObject *self, PyObject*args)
{
	int arg1;
	int arg2;
	if (self->shared) {
		PyErr_SetString(PyExc_TypeError, "can't modify shared GC");
		return NULL;
	}
	if (!PyArg_ParseTuple(args, "ii",
			&arg1,
			&arg2))
		return NULL;
XSetTSOrigin(self->display, self->gc,
			arg1,
			arg2);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_SetTile(PaxGCObject *self, PyObject*args)
{
	PyObject *arg1;
	if (self->shared) {
		PyErr_SetString(PyExc_TypeError, "can't modify shared GC");
		return NULL;
	}
	if (!PyArg_ParseTuple(args, "O",
			&arg1))
		return NULL;
	if (!PaxPixmap_Check(arg1)) {
		if (!PyErr_Occurred())
			PyErr_SetString(PyExc_TypeError, "arg1 should be Pixmap");
		return NULL;
	}
XSetTile(self->display, self->gc,
			PaxPixmap_AsPixmap(arg1));
	Py_INCREF(Py_None);
	return Py_None;
}

// ---------------------- Cairo functionality-------------------------------
static PyObject *
PaxGC_CairoInit(PaxGCObject * self, PyObject *args)
{
	int width, height;
	int x_off=0, y_off=0;
	cairo_surface_t *surface;
	if (!PyArg_ParseTuple(args, "ii",
			&width,
			&height))
		return NULL;

	Visual *visual = DefaultVisual(self->display, DefaultScreen(self->display));
	surface = cairo_xlib_surface_create(self->display, self->drawable, visual, width, height);
	cairo_surface_set_device_offset(surface, -x_off, -y_off);
	self->cairo = cairo_create(surface);
// 	cairo_surface_destroy(surface);
	printf("Cairo initialized!\n");
	cairo_set_fill_rule(self->cairo, 1);
	cairo_move_to(self->cairo, 0, 0);

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_CairoSetSourceRGB(PaxGCObject * self, PyObject *args)
{
    double red, green, blue;

    if (!PyArg_ParseTuple (args, "ddd",
			   &red, &green, &blue))
	return NULL;

    cairo_set_source_rgb (self->cairo, red, green, blue);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_CairoSetSourceRGBA(PaxGCObject * self, PyObject *args)
{
    double red, green, blue;
    double alpha = 1.0;

    if (!PyArg_ParseTuple (args, "ddd|d",
			   &red, &green, &blue, &alpha))
	return NULL;

    cairo_set_source_rgba (self->cairo, red, green, blue, alpha);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_CairoSetOutlineAttr(PaxGCObject * self, PyObject *args)
{
    double width;
    int cap, join;

    if (!PyArg_ParseTuple (args, "dii",
			   &width, &cap, &join))
	return NULL;

cairo_set_line_width (self->cairo, width);
cairo_set_line_cap (self->cairo, cap);
cairo_set_line_join (self->cairo, join);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_CairoFillRectangle(PaxGCObject * self, PyObject *args)
{
	double arg1;
	double arg2;
	double arg3;
	double arg4;
	if (!PyArg_ParseTuple(args, "dddd",
			&arg1,
			&arg2,
			&arg3,
			&arg4))
		return NULL;

cairo_new_path(self->cairo);
cairo_move_to(self->cairo, arg1, arg2);
cairo_rel_line_to(self->cairo, arg3, 0);
cairo_rel_line_to(self->cairo, 0, arg4);
cairo_rel_line_to(self->cairo, -1*arg3, 0);
cairo_rel_line_to(self->cairo, 0, -1*arg4);
cairo_close_path(self->cairo);

if(self->cairo_pattern!=NULL){
	cairo_set_source(self->cairo, self->cairo_pattern);
}
cairo_fill(self->cairo);

if(self->cairo_pattern!=NULL){
	cairo_pattern_destroy(self->cairo_pattern);
	self->cairo_pattern = NULL;
}
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_CairoDrawRectangle(PaxGCObject * self, PyObject *args)
{
	double arg1;
	double arg2;
	double arg3;
	double arg4;
	if (!PyArg_ParseTuple(args, "dddd",
			&arg1,
			&arg2,
			&arg3,
			&arg4))
		return NULL;

cairo_new_path(self->cairo);
cairo_move_to(self->cairo, arg1, arg2);
cairo_rel_line_to(self->cairo, arg3, 0);
cairo_rel_line_to(self->cairo, 0, arg4);
cairo_rel_line_to(self->cairo, -1*arg3, 0);
cairo_rel_line_to(self->cairo, 0, -1*arg4);
cairo_close_path(self->cairo);
cairo_stroke(self->cairo);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_CairoSetDash(PaxGCObject * self, PyObject *args)
{
    double *dashes, offset = 0;
    int ndash, i;
    PyObject *py_dashes;

    if (!PyArg_ParseTuple (args, "O|d", &py_dashes, &offset))
	return NULL;

    py_dashes = PySequence_Fast (py_dashes,
				 "first argument must be a sequence");
    if (!py_dashes)
	return NULL;

    ndash = PySequence_Fast_GET_SIZE(py_dashes);
    dashes = malloc (ndash * sizeof(double));
    for (i = 0; i < ndash; i++) {
	PyObject *item = PySequence_Fast_GET_ITEM(py_dashes, i);

	dashes[i] = PyFloat_AsDouble(item);
	if (PyErr_Occurred()) {
	    free (dashes);
	    Py_DECREF(py_dashes);
	    return NULL;
	}
    }
    Py_DECREF(py_dashes);

cairo_set_dash(self->cairo, dashes, ndash, offset);
free(dashes);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_CairoDrawArc(PaxGCObject * self, PyObject *args)
{
    double x, y, width, height, radius;

    if (!PyArg_ParseTuple (args, "dddd",
			   &x, &y, &width, &height))
	return NULL;

cairo_save (self->cairo);

cairo_new_path(self->cairo);
cairo_translate (self->cairo, x, y);
if(width>height)
{
	cairo_scale (self->cairo, width/height, 1.0);
	radius=height/2;
}
else
{
	cairo_scale (self->cairo, 1.0, height/width);
	radius=width/2;
}
cairo_arc (self->cairo, 0., 0., radius, 0., 2 * 3.14159265359); //2 * M_PI);
cairo_close_path(self->cairo);

cairo_restore (self->cairo);
cairo_stroke(self->cairo);

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_CairoFillArc(PaxGCObject * self, PyObject *args)
{
    double x, y, width, height, radius;

    if (!PyArg_ParseTuple (args, "dddd",
			   &x, &y, &width, &height))
	return NULL;

cairo_save (self->cairo);

cairo_new_path(self->cairo);
cairo_translate (self->cairo, x, y);
if(width>height)
{
	cairo_scale (self->cairo, width/height, 1.0);
	radius=height/2;
}
else
{
	cairo_scale (self->cairo, 1.0, height/width);
	radius=width/2;
}
cairo_arc (self->cairo, 0., 0., radius, 0., 2 * 3.14159265359); //2 * M_PI);
cairo_close_path(self->cairo);

if(self->cairo_pattern!=NULL){
	cairo_set_source(self->cairo, self->cairo_pattern);
}
cairo_fill(self->cairo);

if(self->cairo_pattern!=NULL){
	cairo_pattern_destroy(self->cairo_pattern);
	self->cairo_pattern = NULL;
}
cairo_restore (self->cairo);

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_CairoFillPolygon(PaxGCObject * self, PyObject *args)
{
	PyObject *arg1;
	double *pts_arg1;
	int npts_arg1;
	int i;

	if (!PyArg_ParseTuple(args, "O",
			&arg1))
		return NULL;
	if (!checkdoublelist(2, arg1, (double**)&pts_arg1, &npts_arg1)) {
		if (!PyErr_Occurred())
			PyErr_SetString(PyExc_TypeError, "arg1 should be CairoPoint[]");
		return NULL;
	}

cairo_new_path(self->cairo);
cairo_move_to(self->cairo, pts_arg1[0], pts_arg1[1]);

for (i = 2; i < 2*npts_arg1; i++)
{
cairo_line_to(self->cairo, pts_arg1[i], pts_arg1[i+1]);
i++;
}
cairo_line_to(self->cairo, pts_arg1[0], pts_arg1[1]);
cairo_close_path(self->cairo);

if(self->cairo_pattern!=NULL){
	cairo_set_source(self->cairo, self->cairo_pattern);
}
cairo_fill(self->cairo);

if(self->cairo_pattern!=NULL){
	cairo_pattern_destroy(self->cairo_pattern);
	self->cairo_pattern = NULL;
}

	PyMem_DEL(pts_arg1);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_CairoDrawPolygon(PaxGCObject * self, PyObject *args)
{
	PyObject *arg1;
	double *pts_arg1;
	int npts_arg1;
	int i;

	if (!PyArg_ParseTuple(args, "O",
			&arg1))
		return NULL;
	if (!checkdoublelist(2, arg1, (double**)&pts_arg1, &npts_arg1)) {
		if (!PyErr_Occurred())
			PyErr_SetString(PyExc_TypeError, "arg1 should be CairoPoint[]");
		return NULL;
	}

cairo_new_path(self->cairo);
cairo_move_to(self->cairo, pts_arg1[0], pts_arg1[1]);

for (i = 2; i < 2*npts_arg1; i++)
{
cairo_line_to(self->cairo, pts_arg1[i], pts_arg1[i+1]);
i++;
}
cairo_line_to(self->cairo, pts_arg1[0], pts_arg1[1]);
cairo_close_path(self->cairo);
cairo_stroke(self->cairo);

	PyMem_DEL(pts_arg1);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_CairoPatternCreateLinear(PaxGCObject * self, PyObject *args)
{
    double x0, y0, x1, y1;

    if (!PyArg_ParseTuple (args, "dddd",
			   &x0, &y0, &x1, &y1))
	return NULL;

    if(self->cairo_pattern!=NULL){
	cairo_pattern_destroy(self->cairo_pattern);
    }

    self->cairo_pattern = cairo_pattern_create_linear(x0, y0, x1, y1);

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_CairoPatternCreateRadial(PaxGCObject * self, PyObject *args)
{
    double x0, y0, r0, x1, y1, r1;

    if (!PyArg_ParseTuple (args, "dddddd",
			   &x0, &y0, &r0, &x1, &y1, &r1))
	return NULL;

    if(self->cairo_pattern!=NULL){
	cairo_pattern_destroy(self->cairo_pattern);
    }

    self->cairo_pattern = cairo_pattern_create_radial(x0, y0, r0, x1, y1, r1);

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_CairoPatternAddColorStopRGB(PaxGCObject * self, PyObject *args)
{
    double offset, red, green, blue;

    if (!PyArg_ParseTuple (args, "dddd",
			   &offset, &red, &green, &blue))
	return NULL;

    cairo_pattern_add_color_stop_rgb(self->cairo_pattern, offset, red, green, blue);

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *
PaxGC_CairoPatternAddColorStopRGBA(PaxGCObject * self, PyObject *args)
{
    double offset, red, green, blue, alpha;

    if (!PyArg_ParseTuple (args, "ddddd",
			   &offset, &red, &green, &blue, &alpha))
	return NULL;

    cairo_pattern_add_color_stop_rgba(self->cairo_pattern, offset, red, green, blue, alpha);

	Py_INCREF(Py_None);
	return Py_None;
}

static PyMethodDef PaxGC_methods[] = {
	{"CairoInit", (PyCFunction)PaxGC_CairoInit, 1},
	{"CairoSetSourceRGB", (PyCFunction)PaxGC_CairoSetSourceRGB, 1},
	{"CairoSetSourceRGBA", (PyCFunction)PaxGC_CairoSetSourceRGBA, 1},
	{"CairoSetOutlineAttr", (PyCFunction)PaxGC_CairoSetOutlineAttr, 1},
	{"CairoSetDash", (PyCFunction)PaxGC_CairoSetDash, 1},
	{"CairoFillRectangle", (PyCFunction)PaxGC_CairoFillRectangle, 1},
	{"CairoDrawRectangle", (PyCFunction)PaxGC_CairoDrawRectangle, 1},
	{"CairoFillArc", (PyCFunction)PaxGC_CairoFillArc, 1},
	{"CairoDrawArc", (PyCFunction)PaxGC_CairoDrawArc, 1},
	{"CairoFillPolygon", (PyCFunction)PaxGC_CairoFillPolygon, 1},
	{"CairoDrawPolygon", (PyCFunction)PaxGC_CairoDrawPolygon, 1},
	{"CairoPatternCreateLinear", (PyCFunction)PaxGC_CairoPatternCreateLinear, 1},
	{"CairoPatternCreateRadial", (PyCFunction)PaxGC_CairoPatternCreateRadial, 1},
	{"CairoPatternAddColorStopRGB", (PyCFunction)PaxGC_CairoPatternAddColorStopRGB, 1},
	{"CairoPatternAddColorStopRGBA", (PyCFunction)PaxGC_CairoPatternAddColorStopRGBA, 1},

	{"ChangeGC", (PyCFunction)PaxGC_ChangeGC, 1},
	{"DrawArc", (PyCFunction)PaxGC_DrawArc, 1},
	{"DrawArcs", (PyCFunction)PaxGC_DrawArcs, 1},
	{"DrawImageString", (PyCFunction)PaxGC_DrawImageString, 1},
	{"DrawLine", (PyCFunction)PaxGC_DrawLine, 1},
	{"DrawLines", (PyCFunction)PaxGC_DrawLines, 1},
	{"DrawPoint", (PyCFunction)PaxGC_DrawPoint, 1},
	{"DrawPoints", (PyCFunction)PaxGC_DrawPoints, 1},
	{"DrawRectangle", (PyCFunction)PaxGC_DrawRectangle, 1},
	{"DrawRectangles", (PyCFunction)PaxGC_DrawRectangles, 1},
	{"DrawSegments", (PyCFunction)PaxGC_DrawSegments, 1},
	{"DrawString", (PyCFunction)PaxGC_DrawString, 1},
	{"FillArc", (PyCFunction)PaxGC_FillArc, 1},
	{"FillArcs", (PyCFunction)PaxGC_FillArcs, 1},
	{"FillPolygon", (PyCFunction)PaxGC_FillPolygon, 1},
	{"FillRectangle", (PyCFunction)PaxGC_FillRectangle, 1},
	{"FillRectangles", (PyCFunction)PaxGC_FillRectangles, 1},
	{"PutImage", (PyCFunction)PaxGC_PutImage, 1},
	{"SetArcMode", (PyCFunction)PaxGC_SetArcMode, 1},
	{"SetBackground", (PyCFunction)PaxGC_SetBackground, 1},
	{"SetClipMask", (PyCFunction)PaxGC_SetClipMask, 1},
	{"SetClipOrigin", (PyCFunction)PaxGC_SetClipOrigin, 1},
	{"SetClipRectangles", (PyCFunction)PaxGC_SetClipRectangles, 1},
	{"SetDashes", (PyCFunction)PaxGC_SetDashes, 1},
	{"SetDrawable", (PyCFunction)PaxGC_SetDrawable, 1},
	{"SetFillRule", (PyCFunction)PaxGC_SetFillRule, 1},
	{"SetFillStyle", (PyCFunction)PaxGC_SetFillStyle, 1},
	{"SetFont", (PyCFunction)PaxGC_SetFont, 1},
	{"SetForeground", (PyCFunction)PaxGC_SetForeground, 1},
	{"SetForegroundAndFill", (PyCFunction)PaxGC_SetForegroundAndFill, 1},
	{"SetFunction", (PyCFunction)PaxGC_SetFunction, 1},
	{"SetGraphicsExposures", (PyCFunction)PaxGC_SetGraphicsExposures, 1},
	{"SetLineAttributes", (PyCFunction)PaxGC_SetLineAttributes, 1},
	{"SetPlaneMask", (PyCFunction)PaxGC_SetPlaneMask, 1},
	{"SetRegion", (PyCFunction)PaxGC_SetRegion, 1},
	{"SetState", (PyCFunction)PaxGC_SetState, 1},
	{"SetStipple", (PyCFunction)PaxGC_SetStipple, 1},
	{"SetSubwindowMode", (PyCFunction)PaxGC_SetSubwindowMode, 1},
	{"SetTSOrigin", (PyCFunction)PaxGC_SetTSOrigin, 1},
	{"SetTile", (PyCFunction)PaxGC_SetTile, 1},
	{"ShmPutImage", (PyCFunction)PaxGC_ShmPutImage, 1},
	{0, 0} /* Sentinel */
};

// ======================================================

static PyObject *
MemberList(void)
{
    int i, n;
    PyObject *v;
    for (n = 0; GCattrdefs[n].name != NULL; n++)
	;
    v = PyList_New(n);
    if (v != NULL)
    {
	for (i = 0; i < n; i++)
	    PyList_SetItem(v, i, PyString_FromString(GCattrdefs[i].name));
	if (PyErr_Occurred())
	{
	    Py_DECREF(v);
	    v = NULL;
	}
	else
	{
	    PyList_Sort(v);
	}
    }
    return v;
}

static PyObject *
GetAttr(PaxGCObject *self, char *name)
{
    struct GCattr *p;
    XGCValues values;
    PyObject *result;

    if (name[0] == '_' && strcmp(name, "__members__") == 0)
	return MemberList();

    result = Py_FindMethod(PaxGC_methods, (PyObject *)self, name);
    if (result != NULL)
	return result;
    PyErr_Clear();

    if (name[0] == 'd' && strcmp(name, "drawable") == 0)
    {
	if (self->drawable_object)
	{
	    Py_INCREF(self->drawable_object);
	    return self->drawable_object;
	}
	PyErr_SetString(PyExc_AttributeError, "drawable object is not set");
	return NULL;
    }

    for (p = GCattrdefs; ; p++)
    {
	if (p->name == NULL)
	{
	    PyErr_SetString(PyExc_AttributeError, name);
	    return NULL;
	}
	if (strcmp(name, p->name) == 0)
	    break;
    }
    if (!XGetGCValues(self->display, self->gc, p->mask, &values))
    {
	PyErr_SetString(PyExc_TypeError, "write-only (!) GC attribute");
	return NULL;
    }
    if (strcmp(p->type, "Pixmap") == 0)
    {
	return PaxPixmap_FromPixmap(self->display,
				   *(Pixmap*)((char*)(&values) + p->offset),
				   0);
    }
    else if (strcmp(p->type, "Font") == 0)
    {
	if (* (Font *) ((char *)(&values) + p->offset) == (Font) -1)
	{
	    Py_INCREF(Py_None);
	    return Py_None;
	}
	return PaxFont_FromFont(self->display,
			       * (Font *) ((char *)(&values) + p->offset));
    }
    else
    {
	/* XXX Assume sizeof(int) == sizeof(long) */
	return PyInt_FromLong(* (long *)((char *)(&values) + p->offset));
    }
}

static int
SetAttr(PaxGCObject *self, char *name, PyObject *value)
{
    struct GCattr *p;
    XGCValues values;

    if (self->shared != PAXGC_OWNED)
    {
	PyErr_SetString(PyExc_TypeError, "can't modify shared GC");
	return -1;
    }
    if (value == NULL)
    {
	PyErr_SetString(PyExc_TypeError, "can't delete GC attribute");
	return -1;
    }
    if (!PyInt_Check(value))
    {
	PyErr_SetString(PyExc_TypeError, "GC attribute value must be integer");
	return -1;
    }
    for (p = GCattrdefs; ; p++)
    {
	if (p->name == NULL)
	{
	    PyErr_SetString(PyExc_AttributeError, name);
	    return -1;
	}
	if (strcmp(name, p->name) == 0)
	    break;
    }
    if (p->type[0] == 'c')
	*((char*)(&values) + p->offset) = PyInt_AsLong(value);
    else
        /* XXX Assume sizeof(int) == sizeof(long) */
	*(long*)((char *)(&values) + p->offset) = PyInt_AsLong(value);
    XChangeGC(self->display, self->gc, p->mask, &values);
    return 0;
}

static void
Dealloc(PaxGCObject *self)
{
    if (self->shared == PAXGC_SHARED)
	Tk_FreeGC(self->display, self->gc);
    else if (self->shared == PAXGC_OWNED)
	XFreeGC(self->display, self->gc);
    Py_XDECREF(self->drawable_object);
    PyObject_Del(self);
}

PyTypeObject PaxGCType =
{
	PyObject_HEAD_INIT(&PyType_Type)
	0,			/*ob_size*/
	"PaxGC",		/*tp_name*/
	sizeof(PaxGCObject),	/*tp_size*/
	0,			/*tp_itemsize*/
	(destructor)Dealloc,	/*tp_dealloc*/
	0,			/*tp_print*/
	(getattrfunc)GetAttr,	/*tp_getattr*/
	(setattrfunc)SetAttr,	/*tp_setattr*/
	0,			/*tp_compare*/
	0,			/*tp_repr*/
	0,			/*tp_as_number*/
	0,			/*tp_as_sequence*/
	0,			/*tp_as_mapping*/
	0,			/*tp_hash*/
};


