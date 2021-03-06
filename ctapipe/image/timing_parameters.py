"""
Image timing-based shower image parametrization.
"""

import numpy as np
from ctapipe.io.containers import TimingParametersContainer

__all__ = [
    'timing_parameters'
]


def timing_parameters(geom, image, peakpos, hillas_parameters):
    """
    Function to extract timing parameters from a cleaned image

    Parameters
    ----------
    geom: ctapipe.instrument.CameraGeometry
        Camera geometry
    image : array_like
        Pixel values
    peakpos : array_like
        Pixel peak positions array
    hillas_parameters: ctapipe.io.containers.HillasParametersContainer
        Result of hillas_parameters

    Returns
    -------
    timing_parameters: TimingParametersContainer
    """

    unit = geom.pix_x.unit
    pix_x = geom.pix_x.value
    pix_y = geom.pix_y.value

    # select only the pixels in the cleaned image that are greater than zero.
    # we need to exclude possible pixels with zero signal after cleaning.
    mask = image > 0
    pix_x = pix_x[mask]
    pix_y = pix_y[mask]
    image = image[mask]
    peakpos = peakpos[mask]

    assert pix_x.shape == image.shape, 'image shape must match geometry'
    assert pix_x.shape == peakpos.shape, 'peakpos shape must match geometry'

    longi, trans = geom.get_shower_coordinates(
        hillas_parameters.x,
        hillas_parameters.y,
        hillas_parameters.psi
    )
    slope, intercept = np.polyfit(longi[mask], peakpos, deg=1, w=np.sqrt(image))

    return TimingParametersContainer(
        slope=slope / unit,
        intercept=intercept,
    )
