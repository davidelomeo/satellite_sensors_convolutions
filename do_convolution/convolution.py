import numpy as np
import pandas as pd
from do_convolution.sensors import sentinel2, sentinel3, superdove

__all__ = ['convolution']


def convolution(reflectance_data, spectral_response_function,
                sensor_name, water_bands_removed=False,
                s2_band_9_flag=False, savefile=None):

    '''Function that convolves the input hyperspectral bands to the input
    sensor bands

    Parameters
    ----------
    reflectance_data : pd.DataFrame
        DataFrame that contains the hyperspectral bands to convolve

    spectral_response_function: pd.DataFrame
        Dataframe that contains the spectral response functions of the sensor
        of choice

    sensor_name: str
        Name of the sensor to choose from the list below:
          - 'Sentinel2'
          - 'Superdove'

    water_bands_removed: Bool | Optional. Default: False
        Flag to determine wether water bands have been previously removed.
        If so, numpy will not through errors for division by 0

    s2_band_9_flag: Bool | Optional. Default: False
        Flag to include band 9 in Sentinel-2. Default is False

    savefile: str | Optional. Default: None
        Path where to save the output file when provided

    Returns
    -------
    pd.DataFrame
        The function only returns a dataframe is the flag return_conv_bands is
        set to True. Otherwise, it will not return anythng
        chosen directory.
    '''

    # if water bands have been removed, numpy will not try to divide by 0 any
    # non-floating null points
    if water_bands_removed:
        np.seterr(divide="ignore")

    # multiply each column in the input spectral measurements to the input
    # spectral response functions
    band_muls = {}
    for column in reflectance_data:
        f = spectral_response_function.mul(reflectance_data[column], axis=0)
        band_muls[reflectance_data[column].name] = f

    # checking what sensor to convolve bands for
    if sensor_name == 'Sentinel2':
        convolved_data = sentinel2(spectral_response_function,
                                   band_muls, s2_band_9_flag)

    if sensor_name == 'Sentinel3':
        convolved_data = sentinel3(spectral_response_function, band_muls)

    if sensor_name == 'Superdove':
        convolved_data = superdove(spectral_response_function, band_muls)

    # creating a single dataframe for all the input columns
    if len(convolved_data) <= 1:
        collated_conv = convolved_data[0]
    else:
        collated_conv = pd.concat(convolved_data, axis=1)

    if savefile:
        collated_conv.to_csv(savefile)

    return collated_conv
