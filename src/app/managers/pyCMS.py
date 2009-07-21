"""
pyCMS

    a Python / PIL interface to the littleCMS ICC Color Management System
    Copyright (C) 2002-2003 Kevin Cazabon
    kevin@cazabon.com
    http://www.cazabon.com

    pyCMS home page:  http://www.cazabon.com/pyCMS
    littleCMS home page:  http://www.littlecms.com
    (littleCMS is Copyright (C) 1998-2001 Marti Maria)

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public
    License along with this library; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


    The pyCMS.py module provides a "clean" interface between Python/PIL and
    pyCMSdll, taking care of some of the more complex handling of the direct
    pyCMSdll functions, as well as error-checking and making sure that all
    relevant data is kept together.

    While it is possible to call pyCMSdll functions directly, it's not highly
    recommended.


    Version History:
        0.0.2 alpha     Jan 6, 2002
        
                        Added try/except statements arount type() checks of
                        potential CObjects... Python won't let you use type()
                        on them, and raises a TypeError (stupid, if you ask me!)

                        Added buildProofTransformFromOpenProfiles() function.                        
                        Additional fixes in DLL, see DLL code for details.
                        
        0.0.1 alpha     first public release, Dec. 26, 2002

    Known to-do list with current version (of Python interface, not pyCMSdll):

        none
      
"""

#######################################################################
# version
#######################################################################
VERSION = "0.0.2 alpha"


#######################################################################
# imports
#######################################################################
import pycms
pyCMSdll=pycms
import os
import Image

#######################################################################
# constants
#######################################################################
TRUE =                          1
FALSE =                         None

INTENT_PERCEPTUAL =             0
INTENT_RELATIVE_COLORIMETRIC =  1
INTENT_SATURATION =             2
INTENT_ABSOLUTE_COLORIMETRIC =  3

DIRECTION_INPUT =               0
DIRECTION_OUTPUT =              1
DIRECTION_PROOF =               2

#######################################################################
# classes
#######################################################################
# classes are used for PyCMSTransform and PyCMSProfile so that data
# such as input and output mode can follow the object after creation,
# and be easily retrieved when needed.

class PyCMSError(Exception):
    pass

class PyCMSTransform:
    def __init__(self, transform = None, inputMode = None, outputMode = None):
        self.transform = transform
        self.inputMode = inputMode
        self.outputMode = outputMode

class PyCMSProfile:
    def __init__(self, profile = None):
        self.profile = profile


#######################################################################
# functions
#######################################################################
def versions ():
    """
    pyCMS.versions()
    
    Returns a tuple of (pyCMSVersion, littleCMSVersion, pythonVersion,
        PILVersion).
        
    However, don't trust these values 100%, because they're currently
    configured manually in pyCMSdll.c before building the DLL.
    """
    
    return pyCMSdll.versions()

def about ():
    """
    pyCMS.about()
    
    Returns a string containing information about pyCMSdll.dll, including
    copyright and license information.
    """
    
    return pyCMSdll.about()

def copyright ():
    """
    pyCMS.copyright()
    
    Returns a string containing information about pyCMSdll.dll, including
    copyright and license information.
    """
    
    return pyCMSdll.copyright()

def profileToProfile (im, inputProfile, outputProfile, renderingIntent = INTENT_PERCEPTUAL, outputMode = None, inPlace = FALSE):
    """
    pyCMS.profileToProfile(im, inputProfile, outputProfile,
        [renderingIntent], [outputMode], [inPlace])
        
    Returns either None or a new PIL image object, depending on value of
    inPlace (see below).  

    im = an open PIL image object (i.e. Image.new(...) or
        Image.open(...), etc.)
    inputProfile = string, as a valid filename path to the ICC input
        profile you wish to use for this image
    outputProfile = string, as a valid filename path to the ICC output
        profile you wish to use for this image
    renderingIntent = integer (0-3) specifying the rendering intent you
        wish to use for the transform
        INTENT_PERCEPTUAL =           0 (DEFAULT) (pyCMS.INTENT_PERCEPTUAL)
        INTENT_RELATIVE_COLORIMETRIC =1 (pyCMS.INTENT_RELATIVE_COLORIMETRIC)
        INTENT_SATURATION =           2 (pyCMS.INTENT_SATURATION)
        INTENT_ABSOLUTE_COLORIMETRIC =3 (pyCMS.INTENT_ABSOLUTE_COLORIMETRIC)

        see the pyCMS documentation for details on rendering intents and
        what they do.
    outputMode = a valid PIL mode for the output image (i.e. "RGB", "CMYK",
        etc.).  Note: if rendering the image "inPlace", outputMode MUST be
        the same mode as the input, or omitted completely.  If omitted, the
        outputMode will be the same as the mode of the input image (im.mode)
    inPlace = BOOL (1 = TRUE, None or 0 = FALSE).  If TRUE, the original
        image is modified in-place, and None is returned.  If FALSE
        (default), a new Image object is returned with the transform
        applied.

    If the input or output profiles specified are not valid filenames, a
    PyCMSError will be raised.  If inPlace == TRUE and outputMode != im.mode,
    a PyCMSError will be raised.  If an error occurs during application of
    the profiles, a PyCMSError will be raised.  If outputMode is not a mode
    supported by the outputProfile (or by pyCMS), a PyCMSError will be
    raised.

    This function applies an ICC transformation to im from inputProfile's
    color space to outputProfile's color space using the specified rendering
    intent to decide how to handle out-of-gamut colors.

    OutputMode can be used to specify that a color mode conversion is to
    be done using these profiles, but the specified profiles must be able
    to handle that mode.  I.e., if converting im from RGB to CMYK using
    profiles, the input profile must handle RGB data, and the output
    profile must handle CMYK data.

    """    
    if not os.path.isfile(inputProfile):
        raise PyCMSError, "Invalid input profile path provided: %s" %inputProfile
    if not os.path.isfile(outputProfile):
        raise PyCMSError, "Invalid output profile path provided: %s" %outputProfile
    
    if outputMode == None:
        outputMode = im.mode

    if type(renderingIntent) != type(1) or not (0 <= renderingIntent <=3):
        raise PyCMSError, "renderingIntent must be an integer between 0 and 3"

    if inPlace == TRUE and im.mode != outputMode:
        raise PyCMSError, "Cannot transform image in place, im.mode and output mode are different (%s vs. %s)" %(im.mode, outputMode)

    if inPlace == TRUE:
        imOut = im
    else:
        imOut = Image.new(outputMode, im.size)

    im.load() #make sure it's loaded, or it may not have a .im attribute!

    result = pyCMSdll.profileToProfile(im.im.id, imOut.im.id, inputProfile, outputProfile, renderingIntent)

    if result == 0:
        if inPlace == TRUE:
            return None
        else:
            return imOut

    elif result == -1:
        raise PyCMSError, "Error occurred in pyCMSdll.profileToProfile()"

    else:
        raise PyCMSError, result

def getOpenProfile (profileFilename):
    """
    pyCMS.getOpenProfile(profileFilename)
    
    Returns a PyCMSProfile class object.  

    profileFilename = string, as a valid filename path to the ICC profile
        you wish to open

    The PyCMSProfile object can be passed back into pyCMS for use in creating
    transforms and such (as in pyCMS.buildTransformFromOpenProfiles()).

    If profileFilename is not a vaild filename for an ICC profile, a
    PyCMSError will be raised.    

    """    
    if not os.path.isfile(profileFilename):
        raise PyCMSError, "Invalid profile path provided: %s" %profileFilename
    
    result = pyCMSdll.getOpenProfile (profileFilename)

    try:
        if type(result) == type("string"):
            raise PyCMSError, result
    except TypeError:
        pass

    return PyCMSProfile(result)

def buildTransform (inputProfile, outputProfile, inMode, outMode, renderingIntent = INTENT_PERCEPTUAL):
    """
    pyCMS.buildTransform(inputProfile, outputProfile, inMode, outMode,
        [renderingIntent])
        
    Returns a PyCMSTransform class object.
    
    inputProfile = string, as a valid filename path to the ICC input
        profile you wish to use for this transform
    outputProfile = string, as a valid filename path to the ICC output
        profile you wish to use for this transform
    inMode = string, as a valid PIL mode that the appropriate profile also
        supports (i.e. "RGB", "RGBA", "CMYK", etc.)
    outMode = string, as a valid PIL mode that the appropriate profile also
        supports (i.e. "RGB", "RGBA", "CMYK", etc.)
    renderingIntent = integer (0-3) specifying the rendering intent you
        wish to use for the transform
        INTENT_PERCEPTUAL =           0 (DEFAULT) (pyCMS.INTENT_PERCEPTUAL)
        INTENT_RELATIVE_COLORIMETRIC =1 (pyCMS.INTENT_RELATIVE_COLORIMETRIC)
        INTENT_SATURATION =           2 (pyCMS.INTENT_SATURATION)
        INTENT_ABSOLUTE_COLORIMETRIC =3 (pyCMS.INTENT_ABSOLUTE_COLORIMETRIC)
        see the pyCMS documentation for details on rendering intents and
        what they do.

    If the input or output profiles specified are not valid filenames, a
    PyCMSError will be raised.  If an error occurs during creation of the
    transform, a PyCMSError will be raised.
    
    If inMode or outMode are not a mode supported by the outputProfile (or
    by pyCMS), a PyCMSError will be raised.

    This function builds and returns an ICC transform from the inputProfile
    to the outputProfile using the renderingIntent to determine what to do
    with out-of-gamut colors.  It will ONLY work for converting images that
    are in inMode to images that are in outMode color format (PIL mode,
    i.e. "RGB", "RGBA", "CMYK", etc.).

    Building the transform is a fair part of the overhead in
    pyCMS.profileToProfile(), so if you're planning on converting multiple
    images using the same input/output settings, this can save you time.
    Once you have a transform object, it can be used with
    pyCMS.applyProfile() to convert images without the need to re-compute
    the lookup table for the transform.

    The reason pyCMS returns a class object rather than a handle directly
    to the transform is that it needs to keep track of the PIL input/output
    modes that the transform is meant for.  These attributes are stored in
    the "inMode" and "outMode" attributes of the object (which can be
    manually overridden if you really want to, but I don't know of any
    time that would be of use, or would even work).

    """   
    if not os.path.isfile(inputProfile):
        raise PyCMSError, "Invalid input profile path provided: %s" %inputProfile
    if not os.path.isfile(outputProfile):
        raise PyCMSError, "Invalid output profile path provided: %s" %outputProfile

    if type(renderingIntent) != type(1) or not (0 <= renderingIntent <=3):
        raise PyCMSError, "renderingIntent must be an integer between 0 and 3"

    result = pyCMSdll.buildTransform (inputProfile, outputProfile, inMode, outMode, renderingIntent)

    try:
        if type(result) == type("string"):
            raise PyCMSError, result
    except TypeError:
        pass

    return PyCMSTransform(result, inMode, outMode)

def buildProofTransform (inputProfile, outputProfile, displayProfile, inMode, outMode, renderingIntent = INTENT_PERCEPTUAL, displayRenderingIntent = INTENT_PERCEPTUAL):
    """
    pyCMS.buildProofTransform(inputProfile, outputProfile, displayProfile,
        inMode, outMode, [renderingIntent], [displayRenderingIntent])
        
    Returns a PyCMSTransform class object.
    
    inputProfile = string, as a valid filename path to the ICC input
        profile you wish to use for this transform
    outputProfile = string, as a valid filename path to the ICC output
        profile you wish to use for this transform
    displayProfile = string, as a valid filename path to the ICC display
        (monitor, usually) profile you wish to use for this transform
    inMode = string, as a valid PIL mode that the appropriate profile also
        supports (i.e. "RGB", "RGBA", "CMYK", etc.)
    outMode = string, as a valid PIL mode that the appropriate profile also
        supports (i.e. "RGB", "RGBA", "CMYK", etc.)
    renderingIntent = integer (0-3) specifying the rendering intent you
        wish to use for the input->output (simulated) transform
        INTENT_PERCEPTUAL =           0 (DEFAULT) (pyCMS.INTENT_PERCEPTUAL)
        INTENT_RELATIVE_COLORIMETRIC =1 (pyCMS.INTENT_RELATIVE_COLORIMETRIC)
        INTENT_SATURATION =           2 (pyCMS.INTENT_SATURATION)
        INTENT_ABSOLUTE_COLORIMETRIC =3 (pyCMS.INTENT_ABSOLUTE_COLORIMETRIC)
        see the pyCMS documentation for details on rendering intents and
        what they do.
    displayRenderingIntent = integer (0-3) specifying the rendering intent
        you wish to use for (input/output simulation)->display transform
        INTENT_PERCEPTUAL =           0 (DEFAULT) (pyCMS.INTENT_PERCEPTUAL)
        INTENT_RELATIVE_COLORIMETRIC =1 (pyCMS.INTENT_RELATIVE_COLORIMETRIC)
        INTENT_SATURATION =           2 (pyCMS.INTENT_SATURATION)
        INTENT_ABSOLUTE_COLORIMETRIC =3 (pyCMS.INTENT_ABSOLUTE_COLORIMETRIC)
        see the pyCMS documentation for details on rendering intents and
        what they do.
        
    If the input, output, or display profiles specified are not valid
    filenames, a PyCMSError will be raised.
    
    If an error occurs during creation of the transform, a PyCMSError will
    be raised.
    
    If inMode or outMode are not a mode supported by the outputProfile
    (or by pyCMS), a PyCMSError will be raised.

    This function builds and returns an ICC transform from the inputProfile
    to the displayProfile, but tries to simulate the result that would be
    obtained on the outputProfile device using renderingIntent and
    displayRenderingIntent to determine what to do with out-of-gamut
    colors.  This is known as "soft-proofing".  It will ONLY work for
    converting images that are in inMode to images that are in outMode
    color format (PIL mode, i.e. "RGB", "RGBA", "CMYK", etc.).

    Usage of the resulting transform object is exactly the same as with
    pyCMS.buildTransform().

    Proof profiling is generally used when using a "proof" device to get a
    good idea of what the final printed/displayed image would look like on
    the outputProfile device when it's quicker and easier to use the
    display device for judging color.  Generally, this means that
    displayDevice is a monitor, or a dye-sub printer (etc.), and the output
    device is something more expensive, complicated, or time consuming
    (making it difficult to make a real print for color judgement purposes).

    Soft-proofing basically functions by limiting the color gamut on the
    display device to the gamut availabile on the output device.  However,
    when the final output device has a much wider gamut than the display
    device, you may obtain marginal results.
    
    """ 
    if not os.path.isfile(inputProfile):
        raise PyCMSError, "Invalid input profile path provided: %s" %inputProfile
    if not os.path.isfile(outputProfile):
        raise PyCMSError, "Invalid output profile path provided: %s" %outputProfile
    if not os.path.isfile(displayProfile):
        raise PyCMSError, "Invalid display profile path provided: %s" %displayProfile

    if type(renderingIntent) != type(1) or not (0 <= renderingIntent <=3):
        raise PyCMSError, "renderingIntent must be an integer between 0 and 3"
    
    result = pyCMSdll.buildProofTransform (inputProfile, outputProfile, displayProfile, inMode, outMode, renderingIntent, displayRenderingIntent)

    try:
        if type(result) == type("string"):
            raise PyCMSError, result
    except TypeError:
        pass

    return PyCMSTransform(result, inMode, outMode)

def buildTransformFromOpenProfiles (inputProfile, outputProfile, inMode, outMode, renderingIntent = INTENT_PERCEPTUAL):
    """
    pyCMS.buildTransformFromOpenProfiles(inputProfile, outputProfile,
        inMode, outMode, [renderingIntent])
        
    Returns a PyCMSTransform class object

    inputProfile = a valid PyCMSProfile class object
    outputProfile = a valid PyCMSProfile class object
    inMode = string, as a valid PIL mode that the appropriate profile also
        supports (i.e. "RGB", "RGBA", "CMYK", etc.)
    outMode = string, as a valid PIL mode that the appropriate profile also
        supports (i.e. "RGB", "RGBA", "CMYK", etc.)
    renderingIntent = integer (0-3) specifying the rendering intent you
        wish to use for the transform
        INTENT_PERCEPTUAL =           0 (DEFAULT) (pyCMS.INTENT_PERCEPTUAL)
        INTENT_RELATIVE_COLORIMETRIC =1 (pyCMS.INTENT_RELATIVE_COLORIMETRIC)
        INTENT_SATURATION =           2 (pyCMS.INTENT_SATURATION)
        INTENT_ABSOLUTE_COLORIMETRIC =3 (pyCMS.INTENT_ABSOLUTE_COLORIMETRIC)
        see the pyCMS documentation for details on rendering intents and
        what they do.

    This function operates exactly the same as pyCMS.buildTransform()
    except that the inputProfile and outputProfile arguments must be valid
    PyCMSProfile objects rather than filenames.  Use this function to
    create pre-calculated transforms from open PyCMSProfiles (such as
    profiles created on-the-fly using pyCMS.createProfile(), or [in the
    future] profiles extracted from image files.

    """

    if type(renderingIntent) != type(1) or not (0 <= renderingIntent <=3):
        raise PyCMSError, "renderingIntent must be an integer between 0 and 3"
    
    result = pyCMSdll.buildTransformFromOpenProfiles (inputProfile.profile, outputProfile.profile, inMode, outMode, renderingIntent)

    try:
        if type(result) == type("string"):
            raise PyCMSError, result
    except TypeError:
        pass

    return PyCMSTransform(result, inMode, outMode)
    
def buildProofTransformFromOpenProfiles (inputProfile, outputProfile, displayProfile, inMode, outMode, renderingIntent = INTENT_PERCEPTUAL, displayRenderingIntent = INTENT_PERCEPTUAL):
    """
    pyCMS.buildProofTransformFromOpenProfiles(inputProfile, outputProfile,
        displayProfile, inMode, outMode, [renderingIntent],
        [displayRenderingIntent])
        
    Returns a PyCMSTransform class object

    inputProfile = a valid PyCMSProfile class object
    outputProfile = a valid PyCMSProfile class object
    displayProfile = a valid PyCMSProfile class object
    inMode = string, as a valid PIL mode that the appropriate profile also
        supports (i.e. "RGB", "RGBA", "CMYK", etc.)
    outMode = string, as a valid PIL mode that the appropriate profile also
        supports (i.e. "RGB", "RGBA", "CMYK", etc.)
    renderingIntent = integer (0-3) specifying the rendering intent you
        wish to use for the transform
        INTENT_PERCEPTUAL =           0 (DEFAULT) (pyCMS.INTENT_PERCEPTUAL)
        INTENT_RELATIVE_COLORIMETRIC =1 (pyCMS.INTENT_RELATIVE_COLORIMETRIC)
        INTENT_SATURATION =           2 (pyCMS.INTENT_SATURATION)
        INTENT_ABSOLUTE_COLORIMETRIC =3 (pyCMS.INTENT_ABSOLUTE_COLORIMETRIC)
        see the pyCMS documentation for details on rendering intents and
        what they do.
    displayRenderingIntent = integer (0-3) specifying the rendering intent you
        wish to use for the transform
        INTENT_PERCEPTUAL =           0 (DEFAULT) (pyCMS.INTENT_PERCEPTUAL)
        INTENT_RELATIVE_COLORIMETRIC =1 (pyCMS.INTENT_RELATIVE_COLORIMETRIC)
        INTENT_SATURATION =           2 (pyCMS.INTENT_SATURATION)
        INTENT_ABSOLUTE_COLORIMETRIC =3 (pyCMS.INTENT_ABSOLUTE_COLORIMETRIC)
        see the pyCMS documentation for details on rendering intents and
        what they do.
    This function operates exactly the same as pyCMS.buildProofTransform()
    except that the profile arguments must be valid
    PyCMSProfile objects rather than filenames.  Use this function to
    create pre-calculated proof transforms from open PyCMSProfiles (such as
    profiles created on-the-fly using pyCMS.createProfile(), or [in the
    future] profiles extracted from image files.

    """

    if type(renderingIntent) != type(1) or not (0 <= renderingIntent <=3) or type(displayRenderingIntent) != type(1) or not (0 <= displayRenderingIntent <=3):
        raise PyCMSError, "renderingIntent must be an integer between 0 and 3"
    
    result = pyCMSdll.buildProofTransformFromOpenProfiles (inputProfile.profile, outputProfile.profile, displayProfile.profile, inMode, outMode, renderingIntent, displayRenderingIntent)

    try:
        if type(result) == type("string"):
            raise PyCMSError, result

    except TypeError:
        pass

    return PyCMSTransform(result, inMode, outMode)    

def applyTransform (im, transform, inPlace = FALSE):
    """
    pyCMS.applyTransform(im, transform, [inPlace])
    
    Returns either None, or a new PIL Image object, depending on the value
        of inPlace (see below)

    im = a PIL Image object, and im.mode must be the same as the inMode
        supported by the transform.
    transform = a valid PyCMSTransform class object
    inPlace = BOOL (1 == TRUE, 0 or None == FALSE).  If TRUE, im is
        modified in place and None is returned, if FALSE, a new Image
        object with the transform applied is returned (and im is not
        changed).  The default is FALSE.

    If im.mode != transform.inMode, a PyCMSError is raised.
    
    If inPlace == TRUE and transform.inMode != transform.outMode, a
    PyCMSError is raised.
    
    If im.mode, transfer.inMode, or transfer.outMode is not supported by
    pyCMSdll or the profiles you used for the transform, a PyCMSError is
    raised.
    
    If an error occurs while the transform is being applied, a PyCMSError
    is raised.

    This function applies a pre-calculated transform (from
    pyCMS.buildTransform() or pyCMS.buildTransformFromOpenProfiles()) to an
    image.  The transform can be used for multiple images, saving
    considerable calcuation time if doing the same conversion multiple times.

    If you want to modify im in-place instead of receiving a new image as
    the return value, set inPlace to TRUE.  This can only be done if
    transform.inMode and transform.outMode are the same, because we can't
    change the mode in-place (the buffer sizes for some modes are
    different).  The  default behavior is to return a new Image object of
    the same dimensions in mode transform.outMode.

    """  
    if im.mode != transform.inputMode:
        raise PyCMSError, "Image mode does not match profile input mode (%s vs %s)" %(im.mode, transform.inMode)
    
    if inPlace == TRUE:
        if transform.inputMode != transform.outputMode:
            raise PyCMSError, "Cannot transform image in place, input mode and output mode are different (%s vs. %s)" %(transform.inMode, transform.outMode)
        imOut = im
    else:
    	if transform.outputMode=='CMYK':
    		color=(100,0,0,0)
    	else:
    		color=(0,0,0)
        imOut = Image.new(transform.outputMode, im.size, color)

    im.load() #make sure it's loaded, or it may not have an .im attribute!
    
    result = pyCMSdll.applyTransform (im.im.id, imOut.im.id, transform.transform)

    if result == 0:
        if inPlace == TRUE:
            return None
        else:
            return imOut

    elif result == -1:
        raise PyCMSError, "Error occurred in pyCMSdll.applyTransform()"

    else:
        raise PyCMSError, result

def createProfile (colorSpace, colorTemp = -1):
    """
    pyCMS.createProfile(colorSpace, [colorTemp])
    
    Returns a PyCMSProfile class object

    colorSpace = string, the color space of the profile you wish to create.
        Currently only "LAB", "XYZ", and "sRGB" are supported.
    colorTemp = positive integer for the white point for the profile, in
        degrees Kelvin (i.e. 5000, 6500, 9600, etc.).  The default is for
        D50 illuminant if omitted (5000k).  colorTemp is ONLY applied to
        LAB profiles, and is ignored for XYZ and sRGB.

    If colorSpace not in ["LAB", "XYZ", "sRGB"], a PyCMSError is raised
    
    If using LAB and colorTemp != a positive integer, a PyCMSError is raised.
    
    If an error occurs while creating the profile, a PyCMSError is raised.

    Use this function to create common profiles on-the-fly instead of
    having to supply a profile on disk and knowing the path to it.  It
    returns a normal PyCMSProfile object that can be passed to
    pyCMS.buildTransformFromOpenProfiles() to create a transform to apply
    to images.

    """    
    if colorSpace not in ["LAB", "XYZ", "sRGB"]:
        raise PyCMSError, "Color space not supported for on-the-fly profile creation (%s)" %colorSpace

    if colorSpace == "LAB":
        if type(colorTemp) == type(5000.0):
            colorTemp = int(colorTemp + 0.5)
        if type (colorTemp) != type (5000):
            raise PyCMSError, "Color temperature must be a positive integer, \"%s\" not valid" %colorTemp
        
    result = pyCMSdll.createProfile (colorSpace, colorTemp)

    try:
        if type(result) == type("string"):
            raise PyCMSError, result

        else:
            return PyCMSProfile(result)
    except TypeError:
        # you can't use type() on a PyCObject... argh!
        return PyCMSProfile(result)
    
def getProfileName (profile):
    """
    pyCMS.getProfileName(profile)
    
    Returns a string containing the internal name of the profile as stored
        in an ICC tag.

    profile = EITHER a valid PyCMSProfile object, OR a string of the
        filename of an ICC profile.

    If profile isn't a valid PyCMSProfile object or filename to a profile,
    a PyCMSError is raised If an error occurs while trying to obtain the
    name tag, a PyCMSError is raised.

    Use this function to obtain the INTERNAL name of the profile (stored
    in an ICC tag in the profile itself), usually the one used when the
    profile was originally created.  Sometimes this tag also contains
    additional information supplied by the creator.
    
    """
    try:
        if type(profile) != type("string"):
            profile = profile.profile
        elif (not os.path.isfile(profile)):
            raise PyCMSError, "Invalid  profile path provided: %s" %profile
        
    except TypeError:
        # you can't use type() on a PyCObject... argh!
        profile = profile.profile

    result = pyCMSdll.getProfileName(profile)

    if len(result) > 7 and result[:7] == "ERROR: ":
        raise PyCMSError, result

    else:
        return result
      
def getProfileInfo (profile):
    """
    pyCMS.getProfileInfo(profile)
    
    Returns a string containing the internal profile information stored in
        an ICC tag.

    profile = EITHER a valid PyCMSProfile object, OR a string of the
        filename of an ICC profile.

    If profile isn't a valid PyCMSProfile object or filename to a profile,
    a PyCMSError is raised.

    If an error occurs while trying to obtain the info tag, a PyCMSError
    is raised

    Use this function to obtain the information stored in the profile's
    info tag.  This often contains details about the profile, and how it
    was created, as supplied by the creator.

    """
    try:
        if type(profile) != type("string"):
            profile = profile.profile
        elif (not os.path.isfile(profile)):
            raise PyCMSError, "Invalid  profile path provided: %s" %profile
        
    except TypeError:
        # you can't use type() on a PyCObject... argh!
        profile = profile.profile
        
    result = pyCMSdll.getProfileInfo(profile)

    if len(result) > 7 and result[:7] == "ERROR: ":
        raise PyCMSError, result

    else:
        return result
      
def getDefaultIntent (profile):
    """
    pyCMS.getDefaultIntent(profile)
    
    Returns integer 0-3 specifying the default rendering intent for this
        profile.
        INTENT_PERCEPTUAL =           0 (DEFAULT) (pyCMS.INTENT_PERCEPTUAL)
        INTENT_RELATIVE_COLORIMETRIC =1 (pyCMS.INTENT_RELATIVE_COLORIMETRIC)
        INTENT_SATURATION =           2 (pyCMS.INTENT_SATURATION)
        INTENT_ABSOLUTE_COLORIMETRIC =3 (pyCMS.INTENT_ABSOLUTE_COLORIMETRIC)
        see the pyCMS documentation for details on rendering intents and
        what they do.

    profile = EITHER a valid PyCMSProfile object, OR a string of the
        filename of an ICC profile.
    
    If profile isn't a valid PyCMSProfile object or filename to a profile,
    a PyCMSError is raised.
    
    If an error occurs while trying to obtain the default intent, a
    PyCMSError is raised.

    Use this function to determine the default (and usually best optomized)
    rendering intent for this profile.  Most profiles support multiple
    rendering intents, but are intended mostly for one type of conversion.
    If you wish to use a different intent than returned, use
    pyCMS.isIntentSupported() to verify it will work first.
    """    
    try:
        if type(profile) != type("string"):
            profile = profile.profile
        elif (not os.path.isfile(profile)):
            raise PyCMSError, "Invalid  profile path provided: %s" %profile
        
    except TypeError:
        # you can't use type() on a PyCObject... argh!
        profile = profile.profile
        
    result = pyCMSdll.getDefaultIntent(profile)

    try:
        if type(result) == type("string"):
            raise PyCMSError, result
        else:
            return result

    except TypeError:
        # you can't use type() on a PyCObject... argh!
        return result
      
def isIntentSupported (profile, intent, direction):
    """
    pyCMS.isIntentSupported(profile, intent, direction)
    
    Returns 1 if the intent/direction are supported, -1 if they are not.

    profile = EITHER a valid PyCMSProfile object, OR a string of the
        filename of an ICC profile.
    intent = integer (0-3) specifying the rendering intent you wish to use
        with this profile
        INTENT_PERCEPTUAL =           0 (DEFAULT) (pyCMS.INTENT_PERCEPTUAL)
        INTENT_RELATIVE_COLORIMETRIC =1 (pyCMS.INTENT_RELATIVE_COLORIMETRIC)
        INTENT_SATURATION =           2 (pyCMS.INTENT_SATURATION)
        INTENT_ABSOLUTE_COLORIMETRIC =3 (pyCMS.INTENT_ABSOLUTE_COLORIMETRIC)
        see the pyCMS documentation for details on rendering intents and
        what they do.
    direction = integer specifing if the profile is to be used for input,
        output, or display/proof
        INPUT =               0 (or use pyCMS.DIRECTION_INPUT)
        OUTPUT =              1 (or use pyCMS.DIRECTION_OUTPUT)
        PROOF (or display) =  2 (or use pyCMS.DIRECTION_PROOF)

    Use this function to verify that you can use your desired
    renderingIntent with profile, and that profile can be used for the
    input/output/display profile as you desire.

    Some profiles are created specifically for one "direction", can cannot
    be used for others.  Some profiles can only be used for certain
    rendering intents... so it's best to either verify this before trying
    to create a transform with them (using this function), or catch the
    potential PyCMSError that will occur if they don't support the modes
    you select.

    """
    try:
        if type(profile) != type("string"):
            profile = profile.profile
        elif (not os.path.isfile(profile)):
            raise PyCMSError, "Invalid  profile path provided: %s" %profile
        
    except TypeError:
        # you can't use type() on a PyCObject... argh!
        profile = profile.profile
        
    result = pyCMSdll.isIntentSupported(profile, intent, direction)

    try:
        if type(result) == type("string"):
            raise PyCMSError, result

        else:
            return result
        
    except TypeError:
        # you can't use type() on a PyCObject... argh!
        return result

if __name__ == "__main__":
    # create a cheap manual from the __doc__ strings for the functions above
    
    import pyCMS
    import string
    print __doc__

    for f in dir(pyCMS):
        print "="*80
        print "%s" %f

        try:
            exec ("doc = pyCMS.%s.__doc__" %(f))
            if string.find(doc, "pyCMS") >= 0:
                # so we don't get the __doc__ string for imported modules
                print doc
        except AttributeError:
            pass
   