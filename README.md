# Satellite Sensors Convolutions
This repository contains the Convolution class that allows to convolve in-situ hyperspectral sprectral measurements to target satellite sensors bands.

## Satellites currently available
- Sentinel2a
- Sentinel2b
- Sentinel3a
- Sentinel3b
- Superdove
- Landsat5TM
- Landsat7ETM+
- Landsat8OLI
- Landsat9OLI

**NOTE:** Sentinel3, Landsat8 and Landsat9 have both mean srfs and relative standard deviations in the folder `spectral_response_functions`. 
The means and standard deviations were obtained by averaging the spectral responses within 1nm ranges.

*More sensors will be addedd over time*

## Usage Instructions
The class `Convolution` expects a pandas dataframe and a string that matches one of the satellites sensors listed above as input. The index column of the dataframe
is a range of wavelengths between 350 and 2500 at 1nm steps, and each column is a different observation (Site). If your reflectance data does not inlcude such range,
plesae add rows of zeros for any missing wavelenght and do not leave any cell with NaNs.

The module will return a dataframe with convolved bands to the target sensor. If the desired satellite is either ***Sentinel3a-b*** or ***Landsat8OLI-9OLI*** the
module will return two dafarames. The user can either assign the two dataframes using two variables or one.

Example of usage if returning one dataframe (i.e., ***Sentinel2a-b***, ***Superdove***, ***Landsat5TM***, ***Landsat7ETM+***):
```
convolution_constructor = convolution.Convolution(*input_data*, *sensor_name*)
convolved_bands = convolution_constructor.do_convolutions()
print(convolved_bands)
```

Example of usage if returning two dataframes (i.e., ***Sentinel3a-b*** or ***Landsat8OLI-9OLI***):
```
convolution_constructor = convolution.Convolution(*input_data*, *sensor_name*)
convolved_bands_1, convolved_bands_2 = convolution_constructor.do_convolutions()
print(convolved_bands_1, convolved_bands_2)
```
or
```
convolution_constructor = convolution.Convolution(*input_data*, *sensor_name*)
convolved_bands = convolution_constructor.do_convolutions()
print(convolved_bands[0], convolved_bands[1])
```
**NOTE:** convolved_bands[0] will always return the means and convolved_bands[1] will always return the stds


The user may also use the following method to return a list of bands names and relative central wavelengths according to the input sensor name:
```
convolution_constructor = convolution.Convolution(*input_data*, *sensor_name*)
central_wavelengths = convolution_constructor.get_central_wavelengths()
```

The user may also use the following method to return a tuple containg the spectral response function for both mean and stds bands (the latter only available if the input sensor name is either ***Sentinel3a-b*** or ***Landsat8OLI-9OLI*** available):
```
convolution_constructor = convolution.Convolution(*input_data*, *sensor_name*)
spectral_response_functions = convolution_constructor.get_srf()
print(spectral_response_functions[0]) # returning the means srf -> available for all sensors
print(spectral_response_functions[0]) # returning the stds srf -> on;y available for ***Sentinel3a-b*** and ***Landsat8OLI-9OLI***
```