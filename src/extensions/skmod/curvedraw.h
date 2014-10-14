/* Sketch - A Python-based interactive drawing program
 * Copyright (C) 2006 by Igor E.Novikov
 * Copyright (C) 1997, 1998 by Bernhard Herzog
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

#ifndef CURVEDRAW_H
#define CURVEDRAW_H

PyObject * SKCurve_PyDrawTransformed(SKCurveObject * self, PyObject * args);

PyObject * SKCurve_PyDrawMultipath(PyObject* self, PyObject * args);

PyObject * SKCurve_PyMultipathRegion(PyObject* self, PyObject * args);



#endif
