sK1 is an open source vector graphics editor similar to CorelDRAW, 
Adobe Illustrator, or Freehand. PrintDesign is oriented for prepress industry, 
so it works with CMYK colorspace and produces CMYK-based PDF and PS output. 

sK1 Project (http://sk1project.org),
Copyright (C) 2003-2015 by Igor E. Novikov

How to install: 
--------------------------------------------------------------------------
 to build package:       python setup.py build
 to install package:     python setup.py install
 to remove installation: python setup.py uninstall
--------------------------------------------------------------------------
 to create source distribution:   python setup.py sdist
--------------------------------------------------------------------------
 to create binary RPM distribution:  python setup.py bdist_rpm
--------------------------------------------------------------------------
 to create binary DEB distribution:  python setup.py bdist_deb
--------------------------------------------------------------------------

help on available distribution formats: python setup.py bdist --help-formats

DETAILS

If you wish testing sK1 you have two installation ways. 
First option is a distutils install with commands:

python setup.py build
python setup.py install

But this way is not recommended. The most preferred option is a package 
installation (deb or rpm). You can create package using command:

python setup.py bdist_deb (for Ubuntu|Mint|Debian etc.)
python setup.py bdist_rpm (for Fedora|OpenSuse|Mageia etc.)

By installing the package you have full control over all the installed files 
and can easily remove them from the system (it's important for application
preview).

For successful build either distutils or deb|rpm package you need installing
some development packages. We describe dev-packages for Ubuntu|Debian, but for
other distros they have similar names. So, you need:

libx11-dev
libxcursor-dev 
libcairo2-dev
liblcms2-dev
libxext-dev 
tk8.6-dev (or tk8.5-dev)
python-dev
python-cairo-dev


To run application you need installing also:

python-tk
python-gtk2
python-imaging 
python-reportlab
python-cairo

-------------------------------------------
Build dependencies for Fedora:

libX11-devel
libXcursor-devel
cairo-devel
lcms2-devel
libXext-devel
tk-devel
python-devel
pycairo-devel

tkinter
pygtk2
python-pillow
python-reportlab
pycairo
-------------------------------------------
Build dependencies for OpenSUSE:

libX11-devel
libXcursor-devel
libXext-devel
cairo-devel
liblcms2-devel
tk-devel
python-devel
python-cairo-devel

python-tk
python-gtk
python-Pillow
python-reportlab
python-cairo
-------------------------------------------
Build dependencies for Mageia 64bit:

lib64x11-devel
lib64xcursor-devel (lib64xcursor1)
lib64xext-devel (lib64xext6)
lib64cairo-devel
lib64lcms2-devel (lib64lcms2_2)
lib64tk-devel
lib64python-devel
python-cairo-devel

tkinter
pygtk2.0
python-pillow
python-reportlab
python-cairo
-------------------------------------------
Build dependencies for Mageia 32bit:

libx11-devel
libxcursor-devel (libxcursor1)
libxext-devel (libxext6)
libcairo-devel
liblcms2-devel
libtk-devel
libpython-devel
python-cairo-devel

tkinter
pygtk2.0
python-pillow
python-reportlab
python-cairo