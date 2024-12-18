"""Module to convolve input hyperspectral data to target satellite sensors bands"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This script contains the class Convolution that allows to convolve input hyperspectral
#  data to target satellite sensor bands
#
# Author: Davide Lomeo,
# Email: davide.lomeo@kcl.ac.uk
# GitHub: https://github.com/davidelomeo/satellite_sensors_convolutions
# Date: 20 Nov 2024
# Version: 0.2.0

import json
import numpy as np
import pandas as pd
from pkg_resources import resource_filename
from convolution.apply_convolutions import convolve_bands_01nm, convolve_bands_1nm

__all__ = ['Convolution']


class Convolution:
    "Class to convolve input ground reflectance to target satelite bands"

    def __init__(self, in_situ_rrs, sensor_name, savefile=None):
        """
        Function that constructs the Convolution datatype using the input parameters.

        Parameters
        ----------
        in_situ_rrs : pd.DataFrame
            The input dataframe containing ground reflectance data.
        
        sensor_name : str
            The name of the sensor for which to convolve the input reflectance data.
            Available sensors include:
            - 'TM_L5'           # Landsat 5 Thematic Mapper
            - 'ETM+_L7'         # Landsat 7 Enhanced Thematic Mapper +
            - 'OLI_L8'          # Landsat 8 Operational Land Imager
            - 'OLI_L9'          # Landsat 9 Operational Land Imager
            - 'MERIS'           # Medium Resolution Imaging Spectrometer
            - 'MSI_S2A'         # Sentinel 2A MultiSpectral Instrument
            - 'MSI_S2B'         # Sentinel 2B MultiSpectral Instrument
            - 'OLCI_S3A'        # Sentinel 3A Ocean and Land Colour Instrument
            - 'OLCI_S3B'        # Sentinel 3B Ocean and Land Colour Instrument
            - 'MODIS_AQUA'      # Moderate Resolution Imaging Spectroradiometer on Aqua
            - 'MODIS_TERRA'     # Moderate Resolution Imaging Spectroradiometer on Terra
            - 'Superdove'       # Superdove satellite
            - 'VIIRS_SNPP'      # Visible Infrared Imaging Radiometer Suite on Suomi NPP
            - 'VIIRS_NOAA20'    # Visible Infrared Imaging Radiometer Suite on NOAA 20
            - 'VIIRS_NOAA21'    # Visible Infrared Imaging Radiometer Suite on NOAA 21
            - 'GOCI'            # Geostationary Ocean Color Imager
            - 'GOCI_II'         # Geostationary Ocean Color Imager II

        savefile : str, optional
            Path to save the output dataframe containing the convolved bands, if provided.
            NOTE: Do not include the file name and extension, just the target folder.

        Functions
        ---------
        get_srf_and_bandpass()
            Function to get the spectral response function and the bandpass information of the user-defined sensor.
        
        do_convolutions()
            Function to initiate band convolution according to the user-defined sensor name.
        """

        # --- Public variables ---
        # These variables are defined by the user
        self.in_situ_rrs = in_situ_rrs
        self.sensor_name = sensor_name
        self.savefile = savefile

        # --- Private variables ---
        # These variables are not defined by the user but are needed to compute convolutions
        self._available_sensors = [
            'MSI_S2A', 'MSI_S2B', 'OLCI_S3A', 'OLCI_S3B',
            'Superdove', 'TM_L5', 'ETM+_L7', 'OLI_L8',
            'OLI_L9', 'MERIS', 'MODIS_AQUA', 'MODIS_TERRA',
            'VIIRS_SNPP', 'VIIRS_NOAA20', 'VIIRS_NOAA21',
            'GOCI', 'GOCI_II'
        ]

        # Raising a Value Error if the input sensor name doesn't match the names defined in the doc.
        if self.sensor_name not in self._available_sensors:
            raise ValueError('''
            Invalid Sensor Name! Please look at the documentation by running 'help(Convolution)'
            to see which sensors are available!''')

        # ensuring that the input reflectance data indices are integers and columns are string
        self.in_situ_rrs.index = self.in_situ_rrs.index.astype(int)
        self.in_situ_rrs.columns = self.in_situ_rrs.columns.astype(str)

        # Public variable not defined by the user but initiated by the user-defined sensor_name
        self.srf, self.bandpass = self.get_srf_and_bandpass()
        self.bandpass['Width (FWHM)'] = self.bandpass['Width (FWHM)'].apply(
            lambda x: int(round(float(x))) | 1)  # Ensure widths are odd

        # Initialize the output DataFrame
        self.convolved_bands = pd.DataFrame(
            index=in_situ_rrs.columns, columns=self.bandpass['Nominal Center Wavelength'])

        if self.savefile:
            self._save_to_file()

    def _save_to_file(self):
        """Private function to save the produced convolution to the user-defined path"""

        self.convolved_bands.to_csv(
           self.savefile + f'/{self.sensor_name}_conv.csv')

    def get_srf_and_bandpass(self):
        """Function that returns the spectral response function and the bandpass of the user-defined sensor

        Returns
        --------
        pd.DataFrame()
        The function returns a dataframe containing the band-wise spectral response function and bandpass of
        the user-defined sensor
        """

        path_to_srf = resource_filename(
            'convolution', f'SRFs_and_bandpasses/{self.sensor_name}_SRF.csv')
        path_to_bandpass = resource_filename(
            'convolution', f'SRFs_and_bandpasses/{self.sensor_name}_bandpass.csv')

        return pd.read_csv(path_to_srf, index_col='wl'), pd.read_csv(path_to_bandpass)

    def do_convolutions(self):
        """Function to perform band convolution based on the user-defined sensor name.

        Returns
        -------
        pd.DataFrame
            The function returns a dataframe containing the convolved bands. If the 'savefile' 
            parameter was provided, the dataframe will also be saved to the specified path.
        """

        self.warnings = []
    
        # Iterate over each col in the in situ data
        for col in self.in_situ_rrs.columns:
            in_situ_wl = self.in_situ_rrs.index.values
            in_situ_rrs_col = self.in_situ_rrs[col].values

            # Iterate over each band in the bandpass file
            for _, band in self.bandpass.iterrows():
                center_wl = band['Nominal Center Wavelength']
                width = band['Width (FWHM)']

                if self.sensor_name in ['OLCI_S3A', 'OLCI_S3B', 'MERIS']:
                    convolved_value = convolve_bands_01nm(self, center_wl, width, in_situ_wl, in_situ_rrs_col)
                else:
                    convolved_value = convolve_bands_1nm(self, center_wl, width, in_situ_wl, in_situ_rrs_col)
    
                # Store the result
                self.convolved_bands.at[col, center_wl] = convolved_value
        
        self.convolved_bands.columns.name = None
        self.convolved_bands.index.name = 'in_situ_obs'
        
        for warning in np.unique(self.warnings):
            print(warning)
        return self.convolved_bands
