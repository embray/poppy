############################################################################
#
#  Airy functions for comparison's sake
#
############################################################################
from __future__ import (absolute_import, division, print_function, unicode_literals)

import numpy as np
import matplotlib.pyplot as pl
import scipy


_RADtoARCSEC = 180.*60*60/np.pi # ~ 206265
_ARCSECtoRAD = np.pi/(180.*60*60)

def airy_1d( diameter=1.0, wavelength=1e-6, length = 512, pixelscale=0.010, 
        obscuration=0.0, center=None, plot=False):
    """ 1-dimensional Airy function PSF calculator 
    
    Parameters
    ----------
    diameter, wavelength : float
        aperture diameter and wavelength in meters
    size : tuple
        array size
    pixelscale : float
        arcseconds
    obscuration: float, optional
        ratio of secondary obscuration (between 0 and 1)

    Returns 
    --------
    r : array
        radius array in arcsec
    airy : array
        Array with the Airy function values, normalized to 1 at peak
    """

    center = (length-1)/2.
    r = np.arange(length)*pixelscale

    v = np.pi * (r*_ARCSECtoRAD) * diameter/wavelength
    e = obscuration

    # pedantically avoid divide by 0 by setting 0s to minimum nonzero number
    v[v==0] = np.finfo(v.dtype).eps

    
    airy =  1./(1-e**2)**2* ((2*scipy.special.jn(1,v) - e*2*scipy.special.jn(1,e*v))/v )**2
    # see e.g. Schroeder, Astronomical Optics, 2nd ed. page 248

    if plot:
        plt.semilogy(r, airy)
        plt.xlabel("radius [arcsec]")
        plt.ylabel("PSF intensity")
    return r, airy



def airy_2d( diameter=1.0, wavelength=1e-6, shape=(512,512), pixelscale=0.010, 
        obscuration=0.0, center=None):
    """ 2-dimensional Airy function PSF calculator 
    
    Parameters
    ----------
    diameter: float
        aperture diameter in meters
    wavelength : float
        Wavelenght in meters
    shape : tuple
        array shape
    pixelscale : 
        arcseconds
    obscuration: float, optional
        Diameter of secondary obscuration
    center: tuple, optional
        Offset coordinates for center of output array
    """

    if center is None:
        center = (np.asarray(shape)-1.)/2
    y, x = np.indices(shape, dtype=float)
    y -= center[0]
    x -= center[1]
    y *= pixelscale
    x *= pixelscale
    r = np.sqrt(x**2 + y**2)

    radius = float(diameter)/2.0

    k = 2*np.pi / wavelength # wavenumber
    v = k * radius * r * _ARCSECtoRAD
    e = obscuration

    # pedantically avoid divide by 0 by setting 0s to minimum nonzero number
    v[v==0] = np.finfo(v.dtype).eps

    airy =  1./(1-e**2)**2* ((2*scipy.special.jn(1,v) - e*2*scipy.special.jn(1,e*v))/v)**2
    # see e.g. Schroeder, Astronomical Optics, 2nd ed. page 248
    return airy


def sinc2_2d( width=1.0, height=None, wavelength=1e-6, shape=(512,512), pixelscale=0.010, 
        obscuration=0.0, center=None):
    """
    Parameters
    -----------
    width : float
        Width in meters of the aperture
    height : float, optional
        height in meters of the aperture. If not specified, the aperture is assumed 
        to be a square so height=width

    """

    if height== None:  height=width
    halfwidth  = float(width)/2
    halfheight = float(height)/2

    if center is None:
        center = (np.asarray(shape)-1.)/2
    y, x = np.indices(shape, float)
    y -= center[0]
    x -= center[1]
    y *= pixelscale
    x *= pixelscale

    k = 2*np.pi / wavelength # wavenumber
    alpha = k * x * halfwidth  * _ARCSECtoRAD
    beta  = k * y * halfheight * _ARCSECtoRAD

    psf = (np.sinc(alpha))**2 * (np.sinc(beta))**2

    return psf
################################################################################


