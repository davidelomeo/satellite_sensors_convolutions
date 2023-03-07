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
The means and standard deviations were obtained by averaging the spectral responses within 1nm ranges. It is worth convoluting bands for both 
means and standard deviations to assess the errors for each band.

*More sensors will be addedd over time*

## Usage Instructions
The class `Convolution` expects a pandas dataframe and a string that matches one of the satellites sensors listed above as input. The index column of the dataframe
is a range of wavelengths between 350 and 2500 at 1nm steps, and each column is a different observation (Site). If your reflectance data does not inlcude such range,
plesae add rows of zeros for any missing wavelenght and do not leave any cell with NaNs.
