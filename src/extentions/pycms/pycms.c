#define COPYRIGHTINFO "\
pyCMS\n\
a Python / PIL interface to the littleCMS ICC Color Management System\n\
Copyright (C) 2002-2003 Kevin Cazabon\n\
kevin@cazabon.com\n\
http://www.cazabon.com\n\
\n\
pyCMS home page:  http://www.cazabon.com/pyCMS\n\
littleCMS home page:  http://www.littlecms.com\n\
(littleCMS is Copyright (C) 1998-2001 Marti Maria)\n\
\n\
This library is free software; you can redistribute it and/or\n\
modify it under the terms of the GNU Lesser General Public\n\
License as published by the Free Software Foundation; either\n\
version 2.1 of the License, or (at your option) any later version.\n\
\n\
This library is distributed in the hope that it will be useful,\n\
but WITHOUT ANY WARRANTY; without even the implied warranty of\n\
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU\n\
Lesser General Public License for more details.\n\
\n\
You should have received a copy of the GNU Lesser General Public\n\
License along with this library; if not, write to the Free Software\n\
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA\n\
"

/////////////////////////////////////////////////////////////////////////////
// includes
/////////////////////////////////////////////////////////////////////////////
#include "Python.h"
#include "lcms.h"
#include "Imaging.h"


/////////////////////////////////////////////////////////////////////////////
// version information: update this before compiling for the versions you're using
/////////////////////////////////////////////////////////////////////////////
#define PYCMSVERSION        "0.0.2 alpha"
#define LITTLECMSVERSION    "1.09b"
#define PILVERSION          "1.1.3"

//#ifndef PY_MAJOR_VERSION
  // before 1.5.2b2, these were not supported
//  #define PY_MAJOR_VERSION 0
//  #define PY_MINOR_VERSION 0
//  #define PY_MICRO_VERSION 0
//#endif
#define PYTHONVERSION       "2.2.0"

/////////////////////////////////////////////////////////////////////////////
// version history
/////////////////////////////////////////////////////////////////////////////
/*
0.0.2 alpha:  Minor updates, added interfaces to littleCMS features, Jan 6, 2003
    - fixed some memory holes in how transforms/profiles were created and passed back to Python
       due to improper destructor setup for PyCObjects
    - added buildProofTransformFromOpenProfiles() function
    - eliminated some code redundancy, centralizing several common tasks with internal functions

0.0.1 alpha:  First public release Dec 26, 2002

*/

/////////////////////////////////////////////////////////////////////////////
// known to-do list with current version
/////////////////////////////////////////////////////////////////////////////
/*
getDefaultIntent doesn't seem to work properly... whassup??? I'm getting very large int return values instead of 0-3
getProfileName and getProfileInfo are a bit shaky... work on these to solidify them!

Add comments to code to make it clearer for others to read/understand!!!
Verify that PILmode->littleCMStype conversion in findLCMStype is correct for all PIL modes (it probably isn't for the more obscure ones)

Add support for reading and writing embedded profiles in JPEG and TIFF files
Add support for creating custom RGB profiles on the fly
Add support for checking presence of a specific tag in a profile
Add support for other littleCMS features as required

*/


/////////////////////////////////////////////////////////////////////////////
// options / configuration
/////////////////////////////////////////////////////////////////////////////
// Set the action to take upon error within the CMS module
// LCMS_ERROR_SHOW      pop-up window showing error, do not close application
// LCMS_ERROR_ABORT     pop-up window showing error, close the application
// LCMS_ERROR_IGNORE    ignore the error and continue
#define cmsERROR_HANDLER LCMS_ERROR_SHOW


/////////////////////////////////////////////////////////////////////////////
// reference
/////////////////////////////////////////////////////////////////////////////
/*
INTENT_PERCEPTUAL                 0
INTENT_RELATIVE_COLORIMETRIC      1
INTENT_SATURATION                 2
INTENT_ABSOLUTE_COLORIMETRIC      3
*/


/////////////////////////////////////////////////////////////////////////////
// structs
/////////////////////////////////////////////////////////////////////////////
typedef struct {
    PyObject_HEAD
    Imaging image;
} ImagingObject;


/////////////////////////////////////////////////////////////////////////////
// internal functions
/////////////////////////////////////////////////////////////////////////////
DWORD
findLCMStype (char* PILmode) {

  if (strcmp(PILmode, "RGB") == 0) {
    return TYPE_RGBA_8;
  }
  else if (strcmp(PILmode, "RGBA") == 0) {
    return TYPE_RGBA_8;
  }
  else if (strcmp(PILmode, "RGBX") == 0) {
    return TYPE_RGBA_8;
  }
  else if (strcmp(PILmode, "RGBA;16B") == 0) {
    return TYPE_RGBA_16;
  }
  else if (strcmp(PILmode, "CMYK") == 0) {
    return TYPE_CMYK_8;
  }
  else if (strcmp(PILmode, "L") == 0) {
    return TYPE_GRAY_8;
  }
  else if (strcmp(PILmode, "L;16") == 0) {
    return TYPE_GRAY_16;
  }
  else if (strcmp(PILmode, "L;16B") == 0) {
    return TYPE_GRAY_16_SE;
  }
  else if (strcmp(PILmode, "YCCA") == 0) {
    return TYPE_YCbCr_8;
  }
  else if (strcmp(PILmode, "YCC") == 0) {
    return TYPE_YCbCr_8;
  }

  else {
    // take a wild guess... but you probably should fail instead.
    return TYPE_GRAY_8; // so there's no buffer overrun...
  }
}

int
pyCMSdoTransform (Imaging im, Imaging imOut, cmsHTRANSFORM hTransform) {
  int i;

  if (im->xsize > imOut->xsize) {
    return -1;
  }
  if (im->ysize > imOut->ysize) {
    return -1;
  }

  Py_BEGIN_ALLOW_THREADS

  if(im->block !=NULL) {
	cmsDoTransform(hTransform, im->block,
				imOut->block,
				im->xsize*im->ysize);
  }else{
	for (i=0; i < im->ysize; i++)
	{
	cmsDoTransform(hTransform, im->image[i],
				imOut->image[i],
				im->xsize);
	}
  }
  Py_END_ALLOW_THREADS

  return 0;
}

cmsHTRANSFORM
_buildTransform (cmsHPROFILE hInputProfile, cmsHPROFILE hOutputProfile, char *sInMode, char *sOutMode, int iRenderingIntent) {
  cmsHTRANSFORM hTransform;

  cmsErrorAction(cmsERROR_HANDLER);

  Py_BEGIN_ALLOW_THREADS

  // create the transform
  hTransform = cmsCreateTransform(hInputProfile,
                                 findLCMStype(sInMode),
                                 hOutputProfile,
                                 findLCMStype(sOutMode),
                                 iRenderingIntent, 0);

  Py_END_ALLOW_THREADS

  return hTransform;
}

cmsHTRANSFORM
_buildProofTransform(cmsHPROFILE hInputProfile, cmsHPROFILE hOutputProfile, cmsHPROFILE hDisplayProfile, char *sInMode, char *sOutMode, int iRenderingIntent, int iDisplayIntent) {
  cmsHTRANSFORM hTransform;

  cmsErrorAction(cmsERROR_HANDLER);

  Py_BEGIN_ALLOW_THREADS

  // create the transform
  hTransform =  cmsCreateProofingTransform(hInputProfile,
                          findLCMStype(sInMode),
                          hOutputProfile,
                          findLCMStype(sOutMode),
                          hDisplayProfile,
                          iRenderingIntent,
                          iDisplayIntent,
                          0);

  Py_END_ALLOW_THREADS

  return hTransform;
}

/////////////////////////////////////////////////////////////////////////////
// Python callable functions
/////////////////////////////////////////////////////////////////////////////
static PyObject *
versions (PyObject *self, PyObject *args) {
  return Py_BuildValue ("ssss", PYCMSVERSION, LITTLECMSVERSION, PYTHONVERSION, PILVERSION);
}

static PyObject *
about (PyObject *self, PyObject *args) {
  return Py_BuildValue("s", COPYRIGHTINFO);
}

static PyObject *
copyright (PyObject *self, PyObject *args) {
  return about(self, args);
}

static PyObject *
getOpenProfile(PyObject *self, PyObject *args) {
  char *sProfile = NULL;

  cmsHPROFILE hProfile;

  if (!PyArg_ParseTuple(args, "s", &sProfile)) {
   return Py_BuildValue("s", "ERROR: Could not parse argument tuple passed to pycms.getOpenProfile()");
  }

  cmsErrorAction(cmsERROR_HANDLER);

  hProfile = cmsOpenProfileFromFile(sProfile, "r");

  return Py_BuildValue("O", PyCObject_FromVoidPtr(hProfile, cmsCloseProfile));
}

static PyObject *
buildTransform(PyObject *self, PyObject *args) {
  char *sInputProfile;
  char *sOutputProfile;
  char *sInMode;
  char *sOutMode;
  int iRenderingIntent = 0;
  cmsHPROFILE hInputProfile, hOutputProfile;
  cmsHTRANSFORM transform;

  if (!PyArg_ParseTuple(args, "ssss|i", &sInputProfile, &sOutputProfile, &sInMode, &sOutMode, &iRenderingIntent)) {
   return Py_BuildValue("s", "ERROR: Could not parse argument tuple passed to pycms.buildTransform()");
  }

  cmsErrorAction(cmsERROR_HANDLER);

  hInputProfile  = cmsOpenProfileFromFile(sInputProfile, "r");
  hOutputProfile = cmsOpenProfileFromFile(sOutputProfile, "r");

  transform = _buildTransform(hInputProfile, hOutputProfile, sInMode, sOutMode, iRenderingIntent);

  cmsCloseProfile(hInputProfile);
  cmsCloseProfile(hOutputProfile);

  return PyCObject_FromVoidPtr(transform, cmsDeleteTransform); // this may not be right way to call the destructor...?
}

static PyObject *
buildTransformFromOpenProfiles (PyObject *self, PyObject *args) {
  char *sInMode;
  char *sOutMode;
  int iRenderingIntent = 0;
  void *pInputProfile;
  void *pOutputProfile;
  cmsHPROFILE hInputProfile, hOutputProfile;
  cmsHTRANSFORM transform;

  if (!PyArg_ParseTuple(args, "OOss|i", &pInputProfile, &pOutputProfile, &sInMode, &sOutMode, &iRenderingIntent)) {
   return Py_BuildValue("s", "ERROR: Could not parse argument tuple passed to pycms.buildTransformFromOpenProfiles()");
  }

  cmsErrorAction(cmsERROR_HANDLER);

  hInputProfile = (cmsHPROFILE) PyCObject_AsVoidPtr(pInputProfile);
  hOutputProfile = (cmsHPROFILE) PyCObject_AsVoidPtr(pOutputProfile);

  transform = _buildTransform(hInputProfile, hOutputProfile, sInMode, sOutMode, iRenderingIntent);

  // we don't have to close these profiles... but do we have to decref them?

  return PyCObject_FromVoidPtr(transform, cmsDeleteTransform); // this may not be right way to call the destructor...?
}

static PyObject *
buildProofTransform(PyObject *self, PyObject *args) {
  char *sInputProfile;
  char *sOutputProfile;
  char *sDisplayProfile;
  char *sInMode;
  char *sOutMode;
  int iRenderingIntent = 0;
  int iDisplayIntent = 0;
  cmsHTRANSFORM transform;

  cmsHPROFILE hInputProfile, hOutputProfile, hDisplayProfile;

  if (!PyArg_ParseTuple(args, "sssss|ii", &sInputProfile, &sOutputProfile, &sDisplayProfile, &sInMode, &sOutMode, &iRenderingIntent, &iDisplayIntent)) {
   return Py_BuildValue("s", "ERROR: Could not parse argument tuple passed to pycms.buildProofTransform()");
  }

  cmsErrorAction(cmsERROR_HANDLER);

  // open the input and output profiles
  hInputProfile  = cmsOpenProfileFromFile(sInputProfile, "r");
  hOutputProfile = cmsOpenProfileFromFile(sOutputProfile, "r");
  hDisplayProfile = cmsOpenProfileFromFile(sDisplayProfile, "r");

  transform = _buildProofTransform(hInputProfile, hOutputProfile, hDisplayProfile, sInMode, sOutMode, iRenderingIntent, iDisplayIntent);

  cmsCloseProfile(hInputProfile);
  cmsCloseProfile(hOutputProfile);
  cmsCloseProfile(hDisplayProfile);

  return PyCObject_FromVoidPtr(transform, cmsDeleteTransform); // this may not be right way to call the destructor...?

}

static PyObject *
buildProofTransformFromOpenProfiles(PyObject *self, PyObject *args) {
  char *sInMode;
  char *sOutMode;
  int iRenderingIntent = 0;
  int iDisplayIntent = 0;
  void *pInputProfile;
  void *pOutputProfile;
  void *pDisplayProfile;
  cmsHTRANSFORM transform;

  cmsHPROFILE hInputProfile, hOutputProfile, hDisplayProfile;

  if (!PyArg_ParseTuple(args, "OOOss|ii", &pInputProfile, &pOutputProfile, &pDisplayProfile, &sInMode, &sOutMode, &iRenderingIntent, &iDisplayIntent)) {
   return Py_BuildValue("s", "ERROR: Could not parse argument tuple passed to pycms.buildProofTransform()");
  }

  cmsErrorAction(cmsERROR_HANDLER);

  hInputProfile = (cmsHPROFILE) PyCObject_AsVoidPtr(pInputProfile);
  hOutputProfile = (cmsHPROFILE) PyCObject_AsVoidPtr(pOutputProfile);
  hDisplayProfile = (cmsHPROFILE) PyCObject_AsVoidPtr(pDisplayProfile);

  transform = _buildProofTransform(hInputProfile, hOutputProfile, hDisplayProfile, sInMode, sOutMode, iRenderingIntent, iDisplayIntent);

  // we don't have to close these profiles, but do we have to decref them?

  return PyCObject_FromVoidPtr(transform, cmsDeleteTransform); // this may not be right way to call the destructor...?
}

static PyObject *
applyTransform(PyObject *self, PyObject *args) {
  long idIn;
  long idOut;
  void *hTransformPointer;
  cmsHTRANSFORM hTransform;
  Imaging im;
  Imaging imOut;

  int result;

  if (!PyArg_ParseTuple(args, "llO", &idIn, &idOut, &hTransformPointer)) {
    return Py_BuildValue("s", "ERROR: Could not parse the data passed to pycms.applyTransform()");
  }

  im = (Imaging) idIn;
  imOut = (Imaging) idOut;

  cmsErrorAction(cmsERROR_HANDLER);

  hTransform = (cmsHTRANSFORM) PyCObject_AsVoidPtr(hTransformPointer);

  result = pyCMSdoTransform(im, imOut, hTransform);

  return Py_BuildValue("i", result);
}

static PyObject *
profileToProfile(PyObject *self, PyObject *args)
{
  Imaging im;
  Imaging imOut;
  long idIn;
  long idOut = 0L;
  char *sInputProfile = NULL;
  char *sOutputProfile = NULL;
  int iRenderingIntent = 0;
  char *inMode;
  char *outMode;
  int result;
  cmsHPROFILE hInputProfile, hOutputProfile;
  cmsHTRANSFORM hTransform;

  // parse the PyObject arguments, assign to variables accordingly
  if (!PyArg_ParseTuple(args, "llss|i", &idIn, &idOut, &sInputProfile, &sOutputProfile, &iRenderingIntent)) {
      return Py_BuildValue("s", "ERROR: Could not parse the argument tuple passed to pycms.profileToProfile()");
  }

  im = (Imaging) idIn;

  if (idOut != 0L) {
    imOut = (Imaging) idOut;
  }

  cmsErrorAction(cmsERROR_HANDLER);

  // Check the modes of imIn and imOut to set the color type for the transform
  // Note that the modes do NOT have to be the same, as long as they are each
  //    supported by the relevant profile specified

  inMode = im->mode;
  if (idOut == 0L) {
    outMode = inMode;
  }
  else {
    outMode = imOut->mode;
  }

  // open the input and output profiles
  hInputProfile  = cmsOpenProfileFromFile(sInputProfile, "r");
  hOutputProfile = cmsOpenProfileFromFile(sOutputProfile, "r");

  // create the transform
  hTransform = _buildTransform(hInputProfile, hOutputProfile, inMode, outMode, iRenderingIntent);

  // apply the transform to imOut (or directly to im in place if idOut is not supplied)
  if (idOut != 0L) {
    result = pyCMSdoTransform (im, imOut, hTransform);
  }
  else {
    result = pyCMSdoTransform (im, im, hTransform);
  }

  // free the transform and profiles
  cmsDeleteTransform(hTransform);
  cmsCloseProfile(hInputProfile);
  cmsCloseProfile(hOutputProfile);

  // return 0 on success, -1 on failure
  return Py_BuildValue("i", result);
}

//////////////////////////////////////////////////////////////////////////////
// Python-Callable On-The-Fly profile creation functions
//////////////////////////////////////////////////////////////////////////////
static PyObject *
createProfile(PyObject *self, PyObject *args)
{
  char *sColorSpace;
  cmsHPROFILE hProfile;
  int iColorTemp = 0;
  LPcmsCIExyY whitePoint = NULL;
  int result;

  if (!PyArg_ParseTuple(args, "s|i", &sColorSpace, &iColorTemp)) {
      return Py_BuildValue("s", "ERROR: Could not parse the argument tuple passed to pycms.createProfile()");
  }

  cmsErrorAction(cmsERROR_HANDLER);

  if (strcmp(sColorSpace, "LAB") == 0) {
    if (iColorTemp > 0) {
      result = cmsWhitePointFromTemp(iColorTemp, whitePoint);
      if (result == FALSE) {
        return Py_BuildValue("s", "ERROR: Could not calculate white point from color temperature provided, must be integer in degrees Kelvin");
      }
      hProfile = cmsCreateLabProfile(whitePoint);
    }
    else {
      hProfile = cmsCreateLabProfile(NULL);
    }
  }
  else if (strcmp(sColorSpace, "XYZ") == 0) {
    hProfile = cmsCreateXYZProfile();
  }
  else if (strcmp(sColorSpace, "sRGB") == 0) {
    hProfile = cmsCreate_sRGBProfile();
  }
  else {
    return Py_BuildValue("s", "ERROR: Color space requested is not valid for built-in profiles");
  }

  return Py_BuildValue("O", PyCObject_FromVoidPtr(hProfile, cmsCloseProfile));
}

//////////////////////////////////////////////////////////////////////////////
// Python callable profile information functions
//////////////////////////////////////////////////////////////////////////////
static PyObject *
getProfileName(PyObject *self, PyObject *args)
{
  // I've had some intermittant problems with this function and getProfileInfo... look at them closer
  char *sProfile;
  char name[1024];

  int closeProfile = FALSE;

  cmsHPROFILE hProfile;

  if (!PyArg_ParseTuple(args, "s", &sProfile)) {
    if (!PyArg_ParseTuple(args, "O", &hProfile)) {
      return Py_BuildValue("s", "ERROR: Could not parse the argument tuple passed to pycms.getProfileName()");
    }
  }
  else {
    hProfile = cmsOpenProfileFromFile(sProfile, "r");
    closeProfile = TRUE;
  }

  // is there a better way to do this?  I can't seem to work with the const char* return value otherwise
  sprintf(name, "%s\n", cmsTakeProductName(hProfile));

  if (closeProfile == TRUE) {
    cmsCloseProfile(hProfile);
  }

  return Py_BuildValue("s", name);
}

static PyObject *
getProfileInfo(PyObject *self, PyObject *args)
{
  char *sProfile;
  char info[4096];
  int closeProfile = FALSE;

  cmsHPROFILE hProfile;

  if (!PyArg_ParseTuple(args, "s", &sProfile)) {
    if (!PyArg_ParseTuple(args, "O", &hProfile)) {
      return Py_BuildValue("s", "ERROR: Could not parse the argument tuple passed to pycms.getProfileInfo()");
    }
  }
  else {
    hProfile = cmsOpenProfileFromFile(sProfile, "r");
    closeProfile = TRUE;
  }

  // is there a better way to do this?  I can't seem to work with the const char* return value otherwise
  sprintf(info, "%s\n", cmsTakeProductInfo(hProfile));

  if (closeProfile == TRUE) {
    cmsCloseProfile(hProfile);
  }

  return Py_BuildValue("s", info);
}

static PyObject *
getDefaultIntent(PyObject *self, PyObject *args)
{
  char *sProfile;
  int intent = 0;
  int closeProfile = FALSE;

  cmsHPROFILE hProfile;

  if (!PyArg_ParseTuple(args, "s", &sProfile)) {
    if (!PyArg_ParseTuple(args, "O", &hProfile)) {
      return Py_BuildValue("s", "ERROR: Could not parse the argument tuple passed to pycms.getDefaultIntent()");
    }
  }
  else {
    hProfile = cmsOpenProfileFromFile(sProfile, "r");
    closeProfile = TRUE;
  }

  intent =  cmsTakeRenderingIntent(hProfile);

  if (closeProfile == TRUE) {
    cmsCloseProfile(hProfile);
  }

  return Py_BuildValue("i", intent);
}

static PyObject *
isIntentSupported(PyObject *self, PyObject *args)
{
  char *sProfile;
  int iIntent;
  int iDirection;
  int closeProfile = FALSE;

  int result;

  cmsHPROFILE hProfile;

  if (!PyArg_ParseTuple(args, "sii", &sProfile, &iIntent, &iDirection)) {
    if (!PyArg_ParseTuple(args, "Oii", &hProfile, &iIntent, &iDirection)) {
      return Py_BuildValue("s", "ERROR: Could not parse the argument tuple passed to pycms.isIntentSupported()");
    }
  }
  else {
    hProfile = cmsOpenProfileFromFile(sProfile, "r");
    closeProfile = TRUE;
  }

  result =  cmsIsIntentSupported(hProfile, iIntent, iDirection);

  if (closeProfile == TRUE) {
    cmsCloseProfile(hProfile);
  }

  if (result == TRUE) {
    return Py_BuildValue("i", 1);
  }
  else {
    return Py_BuildValue("i", -1);
  }
}

/////////////////////////////////////////////////////////////////////////////
// Python interface setup
/////////////////////////////////////////////////////////////////////////////
static PyMethodDef pycms_methods[] = {
  // pyCMS info
  {"versions", versions, 1, "pycms.versions() returs tuple of pyCMSversion, littleCMSversion, pythonVersion that it was compiled with (don't trust this 100%, they must be set manually in the source code for now)"},
  {"about", about, 1, "pycms.about() returns info about pycms"},
  {"copyright", copyright, 1, "pycms.copyright() returns info about pycms"},

  // profile and transform functions
  {"profileToProfile", profileToProfile, 1, "pycms.profileToProfile (idIn, idOut, InputProfile, OutputProfile, [RenderingIntent]) returns 0 on success, -1 on failure.  If idOut is the same as idIn, idIn is modified in place, otherwise the results are applied to idOut"},
  {"getOpenProfile", getOpenProfile, 1, "pycms.getOpenProfile (profileName) returns a handle to an open pyCMS profile that can be used to build a transform"},
  {"buildTransform", buildTransform, 1, "pycms.buildTransform (InputProfile, OutputProfile, InMode, OutMode, [RenderingIntent]) returns a handle to a pre-computed ICC transform that can be used for processing multiple images, saving calculation time"},
  {"buildProofTransform", buildProofTransform, 1, "pycms.buildProofTransform (InputProfile, OutputProfile, DisplayProfile, InMode, OutMode, [RenderingIntent], [DisplayRenderingIntent]) returns a handle to a pre-computed soft-proofing (simulating the output device capabilities on the display device) ICC transform that can be used for processing multiple images, saving calculation time"},
  {"buildProofTransformFromOpenProfiles", buildProofTransformFromOpenProfiles, 1, "pycms.buildProofTransformFromOpenProfiles(InputProfile, OutputProfile, DisplayProfile, InMode, OutMode, [RenderingIntent], [DisplayRenderingIntent]) returns a handle to a pre-computed soft-proofing transform.  Profiles should be HANDLES, not pathnames."},
  {"applyTransform", applyTransform, 1, "pycms.applyTransform (idIn, idOut, hTransform) applys a pre-calcuated transform (from pycms.buildTransform) to an image.  If idIn and idOut are the same, it modifies the image in place, otherwise the new image is built in idOut.  Returns 0 on success, -1 on failure"},
  {"buildTransformFromOpenProfiles", buildTransformFromOpenProfiles, 1, "pycms.buildTransformFromOpenProfiles (InputProfile, OutputProfile, InMode, OutMode, RenderingIntent) returns a handle to a pre-computed ICC transform that can be used for processing multiple images, saving calculation time"},

  // on-the-fly profile creation functions
  {"createProfile", createProfile, 1, "pycms.createProfile (colorSpace, [colorTemp]) returns a handle to an open profile created on the fly.  colorSpace can be 'LAB', 'XYZ', or 'xRGB'.  If using LAB, you can specify a white point color temperature, or let it default to D50 (5000K)"},

  // profile info functions
  {"getProfileName", getProfileName, 1, "pycms.getProfileName (profile) returns the internal name of the profile"},
  {"getProfileInfo", getProfileInfo, 1, "pycms.getProfileInfo (profile) returns additional information about the profile"},
  {"getDefaultIntent", getDefaultIntent, 1, "pycms.getDefaultIntent (profile) returns the default rendering intent of the profile (as an integer)"},
  {"isIntentSupported", isIntentSupported, 1, "pycms.isIntentSupported (profile, intent, direction) returns 1 if profile supports that intent, -1 if it doesnt.  Direction is what the profile is being used for: INPUT = 0, OUTPUT = 1, PROOF = 2"},

  {NULL, NULL}
};

void initpycms(void)
{
  Py_InitModule("pycms", pycms_methods);
}
