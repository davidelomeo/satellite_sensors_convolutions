"""Satellite-sensor specific functions to convolve input data to spectral response functions"""

import numpy as np
import pandas as pd

__all__ = ['convolve_bands_01nm', 'convolve_bands_1nm']


def convolve_bands_01nm(self, center_wl, width, in_situ_wl, in_situ_rrs):
    """
    Convolve in situ reflectance values to a specific sensor band at 0.1nm intervals.

    Parameters:
    - center_wl: float
        Center wavelength of the band.
    - width: float
        Full width at half maximum (FWHM) of the band.
    - in_situ_wl: array-like
        In situ wavelengths (0.1nm intervals).
    - in_situ_rrs: array-like
        In situ reflectance values.

    Returns:
    - convolved_value: float
        Convolved reflectance value for the band.
    """

    # Calculate exact half-widths and adjust for decimal precision
    half_width = width / 2.0
    if half_width % 0.1 == 0.05:
        half_width_left = round(half_width - 0.05, 1)
        half_width_right = round(half_width + 0.05, 1)
    else:
        half_width_left = round(half_width, 1)
        half_width_right = round(half_width, 1)

    start_wl = center_wl - half_width_left
    end_wl = center_wl + half_width_right

    # Find in situ points within the current band range
    in_situ_mask = (in_situ_wl >= start_wl) & (in_situ_wl <= end_wl)
    in_situ_band_wl = in_situ_wl[in_situ_mask]
    in_situ_band_rrs = in_situ_rrs[in_situ_mask]

    # Check if in_situ_band_wl is empty
    if in_situ_band_wl.size == 0:
        self.warnings.append(f"WARNING: Band {center_wl} nm was not convolved due to missing input data")
        return 0

    # Find SRF points within the current band range
    srf_mask = (self.srf.index.values >= start_wl) & (self.srf.index.values <= end_wl)
    srf_band_wl = self.srf.index.values[srf_mask]
    srf_band = self.srf.loc[srf_band_wl, str(int(center_wl))]

    # Interpolate in situ reflectance to match the SRF wavelengths
    interp_rrs = np.interp(srf_band_wl, in_situ_band_wl, in_situ_band_rrs)

    # Perform convolution using numerical integration (trapezoidal rule)
    numerator = np.trapz(interp_rrs * srf_band, srf_band_wl)
    denominator = np.trapz(srf_band, srf_band_wl)

    if denominator != 0:
        convolved_value = numerator / denominator
    else:
        convolved_value = 0

    return convolved_value


def convolve_bands_1nm(self, center_wl, width, in_situ_wl, in_situ_rrs):
    """
    Convolve in situ reflectance values to a specific sensor band at 1nm intervals.

    Parameters:
    - center_wl: float
        Center wavelength of the band.
    - width: float
        Full width at half maximum (FWHM) of the band.
    - in_situ_wl: array-like
        In situ wavelengths (1nm intervals).
    - in_situ_rrs: array-like
        In situ reflectance values.

    Returns:
    - convolved_value: float
        Convolved reflectance value for the band.
    """
    # Define the range of wavelengths for the band
    half_width = (width // 2)
    start_wl = center_wl - half_width
    end_wl = center_wl + half_width

    # Find in situ points within the current band range
    in_situ_mask = (in_situ_wl >= start_wl) & (in_situ_wl <= end_wl)
    in_situ_band_wl = in_situ_wl[in_situ_mask]
    in_situ_band_rrs = in_situ_rrs[in_situ_mask]

        # Check if in_situ_band_wl is empty
    if in_situ_band_wl.size == 0:
        self.warnings.append(f"WARNING: Band {center_wl} nm was not convolved due to missing input data")
        return 0

    # Directly use in situ reflectance and SRF values for sensors with 1nm intervals
    srf_band = self.srf.loc[in_situ_band_wl, str(int(center_wl))]
    numerator = np.trapz(in_situ_band_rrs * srf_band, in_situ_band_wl)
    denominator = np.trapz(srf_band, in_situ_band_wl)

    if denominator != 0:
        convolved_value = numerator / denominator
    else:
        convolved_value = 0

    return convolved_value
