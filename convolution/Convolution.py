"""Module to convolve input hyperspectral data to target satellite sensors bands"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This script contains the class Convolution that allows to convolve input hyperspectral
#  data to target satellite sensor bands
#
# Author: Davide Lomeo,
# Email: davide.lomeo@kcl.ac.uk
# GitHub: https://github.com/davidelomeo/satellite_sensors_convolutions
# Date: 07 Apr 2023
# Version: 0.1.0

import json
import numpy as np
import pandas as pd
from pkg_resources import resource_filename
from convolution.sensors import sentinel2, sentinel3, superdove, landsat5, landsat7, landsat8, landsat9, meris

__all__ = ['Convolution']


class Convolution:
    "Class to convolve input ground reflectance to target satelite bands"

    def __init__(self, reflectance_data, sensor_name, savefile=None):
        """ Function that constructs the Convolution datatype using the input parameters

        Parameters
        ----------
        reflectance_data: pd.DataFrame
           The input dataframe that contains ground reflectance data
    
        spectral_response_function: pd.DataFrame
           The input spectral response function

        sensor_name: str
           The name of the sensor for which to convolve the input reflectance data.

           The choices of sensors are:
               - 'Sentinel2a'
               - 'Sentinel2b'
               - 'Sentinel3a'
               - 'Sentinel3b'
               - 'Superdove'
               - 'Landsat5TM'
               - 'Landsat7ETM+'
               - 'Landsat8OLI'
               - 'Landsat9OLI'
               - 'MERIS'

            NOTE: Sentinel3a-b, Landsat8OLI-9OLI, MERIS return two dataframes in a list. The first
                  one are the convolved bands means and the second one their standard deviations

        savefile: str | Optional. Default: None
            Path where to save the output dataframe containing the convolved bands when provided.
            NOTE: do not inlcude file name and extension, just target folder

        Functions
        ---------
        get_central_wavelengths()
            Function to get the central band wavelengths of the user-defined sensor name
        get_srf()
            Function to get the spectral response function of the user-defined sensor name
        do_convolutions(self):
            Function to initiate band convolution according to the user-defined sensor name
        """

        # --- Public variables ---
        # These variables are defined by the user
        self.reflectance_data = reflectance_data
        self.sensor_name = sensor_name
        self.savefile = savefile

        # --- Private variables ---
        # These variables are not defined by the user but are needed to compute convolutions
        self._band_muls, self._band_muls_stds = {}, {}
        self._available_sensors = [
            'Sentinel2a', 'Sentinel2b', 'Sentinel3a', 'Sentinel3b',
            'Superdove', 'Landsat5TM', 'Landsat7ETM+', 'Landsat8OLI',
            'Landsat9OLI', 'MERIS'
        ]

        # Raising a Value Error if the input sensor name doesn't match the names defined in the doc.
        if self.sensor_name not in self._available_sensors:
            raise ValueError('''
            Invalid Sensor Name! Please look at the documentation by running 'help(Convolution)'
            to see which sensors are available!''')

        # Public variable not defined by the user but initiated by the user-defined sensor_name
        self.srf, self.srf_stds = self.get_srf()

        # ensuring that numpy doesn't throw an error when dividing by 0
        np.seterr(divide="ignore")

        # generating two empty dataframes - one for band means and one for stds - with the
        # band numbers and respective central wavelenghts as index
        index_col = pd.Index(self.get_central_wavelengths(), name='Band_name_and_centre_wavelength')
        self.convolved_bands = pd.DataFrame(index=index_col)
        self.convolved_bands_stds = pd.DataFrame(index=index_col)

        # multiply each column in the input spectral measurements to the input
        # spectral response functions
        for column in self.reflectance_data:
            product_df = self.srf.mul(self.reflectance_data[column], axis=0)
            self._band_muls[self.reflectance_data[column].name] = product_df
            # doing the same as above only if the sensor used has both means and stds
            if not self.srf_stds.empty:
                product_df_std = self.srf_stds.mul(self.reflectance_data[column], axis=0)
                self._band_muls_stds[self.reflectance_data[column].name] = product_df_std

        if self.savefile:
            self._save_to_file()

    def _save_to_file(self):
        """Private function to save the produced convolution to the user-defined path"""

        self.convolved_bands.to_csv(
           self.savefile + f'/{self.sensor_name}_convolved_bands.csv')
        if not self.srf_stds.empty:
            self.convolved_bands_stds.to_csv(
                self.savefile + f'/{self.sensor_name}_convolved_bands_stds.csv')

    def get_central_wavelengths(self):
        """Function that returns the central bands wavelengths od the user-defined sensor

        Returns
        --------
        list
        The function returns a list of band names and respective central wavelengths of the
        user-defined sensor name
        """

        json_file = resource_filename(
            'convolution', 'spectral_response_functions/central_wavelengths.json')
        with open(json_file) as file:
            central_wavelengths = json.load(file)
        return central_wavelengths[self.sensor_name]

    def get_srf(self):
        """Function that returns the spectral response function of the user-defined sensor

        Returns
        --------
        pd.DataFrame()
        The function returns a dataframe containing the band-wise spectral response function of
        the user-defined sensor
        """
        if self.sensor_name in ['Sentinel3a', 'Sentinel3b', 'Landsat8OLI', 'Landsat9OLI', 'MERIS']:
            path_to_srf_means = resource_filename(
                'convolution', f'spectral_response_functions/{self.sensor_name}_srf_means.csv')
            path_to_srf_stds = resource_filename(
                'convolution', f'spectral_response_functions/{self.sensor_name}_srf_stds.csv')
            return pd.read_csv(path_to_srf_means, index_col='SR_WL'
                               ), pd.read_csv(path_to_srf_stds, index_col='SR_WL')
        else:
            path_to_srf = resource_filename(
                'convolution',
                f'spectral_response_functions/{self.sensor_name}_srf.csv')
            return pd.read_csv(path_to_srf, index_col='SR_WL'), pd.DataFrame()

    def do_convolutions(self):
        """Function to initiate band convolution according to the sensor name defined by the user

        Returns
        -------
        pd.DataFrame()
            The function returns either one or two dataframes. The dataframe(s) will also be
            saved to the target path if the variable savefile was provided. The function returns
            two dataframes if the user convolves bands to Sentinel3a-b, Landsat8OLI-9OLI or MERIS.
        """

        if (self.sensor_name == 'Sentinel2a') | (self.sensor_name == 'Sentinel2b'):
            sentinel2(self)

        if (self.sensor_name == 'Sentinel3a') | (self.sensor_name == 'Sentinel3b'):
            self.convolved_bands = sentinel3(
                self, self.srf, self._band_muls, self.convolved_bands)
            self.convolved_bands_stds = sentinel3(
                self, self.srf_stds, self._band_muls_stds, self.convolved_bands_stds)

        if self.sensor_name == 'Superdove':
            superdove(self)

        if self.sensor_name == 'Landsat5TM':
            landsat5(self)

        if self.sensor_name == 'Landsat7ETM+':
            landsat7(self)

        if self.sensor_name == 'Landsat8OLI':
            self.convolved_bands = landsat8(
                self, self.srf, self._band_muls, self.convolved_bands)
            self.convolved_bands_stds = landsat8(
                self, self.srf_stds, self._band_muls_stds, self.convolved_bands_stds)

        if self.sensor_name == 'Landsat9OLI':
            self.convolved_bands = landsat9(
                self, self.srf, self._band_muls, self.convolved_bands)
            self.convolved_bands_stds = landsat9(
                self, self.srf_stds, self._band_muls_stds, self.convolved_bands_stds)

        if (self.sensor_name == 'MERIS') | (self.sensor_name == 'MERIS'):
            self.convolved_bands = meris(
                self, self.srf, self._band_muls, self.convolved_bands)
            self.convolved_bands_stds = meris(
                self, self.srf_stds, self._band_muls_stds, self.convolved_bands_stds)

        if not self.srf_stds.empty:
            return self.convolved_bands, self.convolved_bands_stds
        else:
            return self.convolved_bands
