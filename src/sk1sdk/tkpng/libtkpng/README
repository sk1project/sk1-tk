TkPNG - PNG Photo Image extension for Tcl/Tk

Copyright (c) 2007 Igor E.Novikov (patched for tk8.5 compatibility)
Copyright (c) 2005 Michael Kirkham <mikek@muonics.com> & Muonics

See the file "license.terms" for information on usage and redistribution
of this file, and for a DISCLAIMER OF ALL WARRANTIES.

This package implements support for loading and using PNG images with
Tcl/Tk.  Although other extensions such as Img also add support for PNG
images, I wanted something that was lightweight, did not depend on libpng,
and which would be suitable for inclusion in the Tk core, as Tk does not
currently support any image formats natively that take advantage of its
internal support for alpha blending, and alpha antialiasing and drop shadows
really go a long way toward beautifying Tk applications.

At this time, the package supports reading images from files or binary
data.  Base64 decoding is supported as of version 0.6.  Exporting images
to PNG format is not supported yet.

The package supports the full range of color types, channels and bit
depths from 1 bit black & white to 16 bit per channel full color
with alpha (64 bit RGBA) and interlacing.  Ancillary "chunks" such
as gamma, color profile, and text fields are ignored, although they
are checked at a minimum for correct CRC.

This extension is provided under the Tcl license (see the file
"license.terms" for details), though acknowledgements and/or
donations are of course accepted and appreciated. :)

Special thanks to Willem van Schaik's suite for his suite of PNG test
images, which are available from:

http://www.schaik.com/pngsuite/pngsuite.html

