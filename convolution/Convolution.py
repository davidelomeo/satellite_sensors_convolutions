import numpy as np
import pandas as pd
from convolution.sensors import sentinel2, sentinel3, superdove, landsat5, landsat7, landsat8, landsat9

__all__ = ['Convolution']


class Convolution:
    "Class to convolve input ground reflectance to target satelite bands"

    def __init__(self, reflectance_data, spectral_response_function,
                 sensor_name, savefile=None):
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
               - 'Sentinel2'
               - 'Sentinel3'
               - 'Superdove'
               - 'Landsat5TM'
               - 'Landsat7ETM+'
               - 'Landsat8OLI'
               - 'Landsat9OLI'
        
        savefile: str | Optional. Default: None
            Path where to save the output dataframe containing the convolved bands when provided
        """

        # --- Public variables ---
        # These variables are defined by the user
        self.reflectance_data = reflectance_data
        self.srf = spectral_response_function
        self.sensor_name = sensor_name
        self.savefile = savefile

        # --- Private variables ---
        # These variables are not defined by the user but are needed to compute convolutions
        self._band_muls = {}
        self._available_sensors = [
            'Sentinel2', 'Sentinel3', 'Superdove',
            'Landsat5TM', 'Landsat7ETM+', 'Landsat8OLI',
            'Landsat9OLI'
        ]
        self._sensor_flag = False

        # ensuring that numpy doesn't throw an error when dividing by 0
        np.seterr(divide="ignore")

        # multiply each column in the input spectral measurements to the input
        # spectral response functions
        for column in self.reflectance_data:
            product_df = self.srf.mul(self.reflectance_data[column], axis=0)
            self._band_muls[self.reflectance_data[column].name] = product_df

        if self.sensor_name not in self._available_sensors:
            print('ERROR: Sensor name not available or valid')
            self._sensor_flag = True
        else:
            # generating an empty dataframe with the band numbers and respective
            # central wavelenghts as index
            index_col = pd.Index(self.__central_wavelenghts(),
                         name='Band_name_and_centre_wavelength')
            self.convolved_bands = pd.DataFrame(index=index_col)

    def __central_wavelenghts(self):
        """Private function that contains the name of the available satellite sensors,
           their bands, and the respective central wavelenghts
           
        Returns
        -------
        list
            The function returns a list with the names of the bands and their respective central
            wavelenghts for input sensor name
        """

        central_bands = {

            'Sentinel2': [
                'Band1_443', 'Band2_490', 'Band3_560', 'Band4_665',
                'Band5_705', 'Band6_740', 'Band7_783', 'Band8_842',
                'Band8A_865', 'Band9_940', 'Band10_1375', 'Band11_1610',
                'Band12_2190'
            ],
            'Sentinel3': [
                'Band1_400', 'Band2_412.5', 'Band3_442.5', 'Band4_490',
                'Band5_510', 'Band6_560', 'Band7_620', 'Band8_665', 
                'Band9_673.75', 'Band10_681.25', 'Band11_708.75', 
                'Band12_753.75', 'Band13_761.25', 'Band14_764.375', 
                'Band15_767.5', 'Band16_778.75', 'Band17_865', 
                'Band18_885', 'Band19_900', 'Band20_940', 'Band21_1020'
            ],
            'Superdove': [
                'Band1_443', 'Band2_490', 'Band3_531', 'Band4_565',
                'Band5_610', 'Band6_665', 'Band7_705', 'Band8_865'
            ],
            'Landsat5TM': [
                'Band1_485', 'Band2_569', 'Band3_660', 'Band4_840',
                'Band5_1676', 'Band7_2223'
            ],
            'Landsat7ETM+': [
                'Band1_483', 'Band2_560', 'Band3_662', 'Band4_835',
                'Band5_1648', 'Band7_2206', 'Band8_706'
            ],
            'Landsat8OLI': [
                'Band1_443', 'Band2_482', 'Band3_561', 'Band4_655',
                'Band5_865', 'Band6_1609', 'Band7_2201', 'Band8_590',
                'Band9_1373'
            ],
            'Landsat9OLI': [
                'Band1_443', 'Band2_482', 'Band3_562', 'Band4_655',
                'Band5_865', 'Band6_1610', 'Band7_2200', 'Band8_590',
                'Band9_1375'
            ]
        }

        return central_bands[self.sensor_name]

    def do_convolutions(self):
        """Function to initiate band convolution according to the sensor name def

        Returns
        -------
        pd.DataFrame
            The function returns a dataframe containing the vonvolved bands. The dataframe will
            also be saved to the target path if the variable savefile was provided.
        """
        if self._sensor_flag:
            print('Nothing will be returned')
            return None
        if not self._sensor_flag:
            if self.sensor_name == 'Sentinel2':
                sentinel2(self)
            if self.sensor_name == 'Sentinel3':
                sentinel3(self)
            if self.sensor_name == 'Superdove':
                superdove(self)
            if self.sensor_name == 'Landsat5TM':
                landsat5(self)
            if self.sensor_name == 'Landsat7ETM+':
                landsat7(self)
            if self.sensor_name == 'Landsat8OLI':
                landsat8(self)
            if self.sensor_name == 'Landsat9OLI':
                landsat9(self)

            if self.savefile:
                self.convolved_bands.to_csv(self.savefile)

            return self.convolved_bands
