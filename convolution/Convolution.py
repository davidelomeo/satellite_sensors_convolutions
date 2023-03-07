
import json
import numpy as np
import pandas as pd
from pkg_resources import resource_filename
from convolution.sensors import sentinel2, sentinel3, superdove, landsat5, landsat7, landsat8, landsat9

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

            NOTE: Sentinel3a-b, Landsat8OLI-9OLI return two dataframes in a list. The first one
                  are the convolved bands means and the second one their standard deviations
    
        savefile: str | Optional. Default: None
            Path where to save the output dataframe containing the convolved bands when provided.
            NOTE: do not inlcude file name and extension, just target folder

        Functions
        ---------
        get_central_wavelengths()
            Function to get the central band wavelengths for the input user-defined satellite name
        get_files(records_path, file_prefix)
            Loads the TFrecords and mixer using the input/ list and file prefix


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
            'Landsat9OLI'
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

    def get_central_wavelengths(self):
        """Function that returns the central bands wavelengths od the user-defined sensor"""
        json_file = resource_filename('convolution', 'central_wavelengths.json')
        with open(json_file) as js:
            mixer = json.load(js)
        return mixer[self.sensor_name]

    # def central_wavelenghts(self):
    #     """Function that contains the name of the available satellite sensors,
    #        their bands, and the respective central wavelenghts

    #     Returns
    #     -------
    #     list
    #         The function returns a list with the names of the bands and their respective central
    #         wavelenghts for the input sensor name
    #     """

    #     central_bands = {

    #         'Sentinel2a': [
    #             'Band1_443', 'Band2_490', 'Band3_560', 'Band4_665',
    #             'Band5_705', 'Band6_740', 'Band7_783', 'Band8_842',
    #             'Band8A_865', 'Band9_940', 'Band10_1375', 'Band11_1610',
    #             'Band12_2190'
    #         ],
    #         'Sentinel2b': [
    #             'Band1_443', 'Band2_490', 'Band3_560', 'Band4_665',
    #             'Band5_705', 'Band6_740', 'Band7_783', 'Band8_842',
    #             'Band8A_865', 'Band9_940', 'Band10_1375', 'Band11_1610',
    #             'Band12_2190'
    #         ],
    #         'Sentinel3a': [
    #             'Band1_400', 'Band2_412.5', 'Band3_442.5', 'Band4_490',
    #             'Band5_510', 'Band6_560', 'Band7_620', 'Band8_665', 
    #             'Band9_673.75', 'Band10_681.25', 'Band11_708.75', 
    #             'Band12_753.75', 'Band13_761.25', 'Band14_764.375', 
    #             'Band15_767.5', 'Band16_778.75', 'Band17_865', 
    #             'Band18_885', 'Band19_900', 'Band20_940', 'Band21_1020'
    #         ],
    #         'Sentinel3b': [
    #             'Band1_400', 'Band2_412.5', 'Band3_442.5', 'Band4_490',
    #             'Band5_510', 'Band6_560', 'Band7_620', 'Band8_665', 
    #             'Band9_673.75', 'Band10_681.25', 'Band11_708.75', 
    #             'Band12_753.75', 'Band13_761.25', 'Band14_764.375', 
    #             'Band15_767.5', 'Band16_778.75', 'Band17_865', 
    #             'Band18_885', 'Band19_900', 'Band20_940', 'Band21_1020'
    #         ],
    #         'Superdove': [
    #             'Band1_443', 'Band2_490', 'Band3_531', 'Band4_565',
    #             'Band5_610', 'Band6_665', 'Band7_705', 'Band8_865'
    #         ],
    #         'Landsat5TM': [
    #             'Band1_485', 'Band2_569', 'Band3_660', 'Band4_840',
    #             'Band5_1676', 'Band7_2223'
    #         ],
    #         'Landsat7ETM+': [
    #             'Band1_483', 'Band2_560', 'Band3_662', 'Band4_835',
    #             'Band5_1648', 'Band7_2206', 'Band8_706'
    #         ],
    #         'Landsat8OLI': [
    #             'Band1_443', 'Band2_482', 'Band3_561', 'Band4_655',
    #             'Band5_865', 'Band6_1609', 'Band7_2201', 'Band8_590',
    #             'Band9_1373'
    #         ],
    #         'Landsat9OLI': [
    #             'Band1_443', 'Band2_482', 'Band3_562', 'Band4_655',
    #             'Band5_865', 'Band6_1610', 'Band7_2200', 'Band8_590',
    #             'Band9_1375'
    #         ]
    #     }

    #     return central_bands[self.sensor_name]

    def get_srf(self):
        """Function that returns the spectral response function of the user-defined sensor

        Returns
        --------
        pd.DataFrame()
        The function returns a dataframe containing the band-wise spectral response function of
        the user-defined sensor
        """
        # Using pkg_resources.resource_filename to access srf dataframes from the
        # spectral_response_functions folder
        if (self.sensor_name == 'Sentinel2a') | (self.sensor_name == 'Sentinel2b'):
            path_to_file = resource_filename(
                'convolution',
                f'spectral_response_functions/s2{self.sensor_name[-1]}_srf.csv')
            return pd.read_csv(path_to_file, index_col='SR_WL'), pd.DataFrame()

        if (self.sensor_name == 'Sentinel3a') | (self.sensor_name == 'Sentinel3b'):
            path_to_means = resource_filename(
                'convolution',
                f'spectral_response_functions/s3{self.sensor_name[-1]}_srf_means.csv')
            path_to_stds = resource_filename(
                'convolution',
                f'spectral_response_functions/s3{self.sensor_name[-1]}_srf_stds.csv')
            return pd.read_csv(
                path_to_means, index_col='SR_WL'), pd.read_csv(path_to_stds, index_col='SR_WL')

        if self.sensor_name == 'Superdove':
            path_to_file = resource_filename(
                'convolution', 'spectral_response_functions/superdove_srf.csv')
            return pd.read_csv(path_to_file, index_col='SR_WL'), pd.DataFrame()

        if self.sensor_name == 'Landsat5TM':
            path_to_file = resource_filename(
                'convolution', 'spectral_response_functions/l5_srf.csv')
            return pd.read_csv(path_to_file, index_col='SR_WL'), pd.DataFrame()

        if self.sensor_name == 'Landsat7ETM+':
            path_to_file = resource_filename(
                'convolution', 'spectral_response_functions/l7_srf.csv')
            return pd.read_csv(path_to_file, index_col='SR_WL'), pd.DataFrame()

        if (self.sensor_name == 'Landsat8OLI') | (self.sensor_name == 'Landsat9OLI'):
            landsat_n = self.sensor_name.partition('OLI')[0][-1]
            path_to_means = resource_filename(
                'convolution',
                f'spectral_response_functions/l{landsat_n}_srf_means.csv')
            path_to_stds = resource_filename(
                'convolution',
                f'spectral_response_functions/l{landsat_n}_srf_stds.csv')
            return pd.read_csv(
                path_to_means, index_col='SR_WL'), pd.read_csv(path_to_stds, index_col='SR_WL')

    def do_convolutions(self):
        """Function to initiate band convolution according to the sensor name defined by the user

        Returns
        -------
        pd.DataFrame()
            The function returns either one or two dataframes. The dataframe(s) will also be
            saved to the target path if the variable savefile was provided. The function returns
            two dataframes if the user convolves bands to Sentinel3a-b or Landsat8OLI-9OLI.
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

        if self.savefile:
            self.convolved_bands.to_csv(
                self.savefile + f'/{self.sensor_name}_convolved_bands.csv')
            if not self.convolved_bands.empty:
                self.convolved_bands_stds.to_csv(
                    self.savefile + f'/{self.sensor_name}_convolved_bands_stds.csv')

        if not self.srf_stds.empty:
            return self.convolved_bands, self.convolved_bands_stds
        else:
            return self.convolved_bands
