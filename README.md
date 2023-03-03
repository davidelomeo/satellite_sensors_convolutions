# Satellite Sensors Convolutions
This repository contains functions to convolve in-situ sprectral measurements to target satellite sensors.

## Satellites currently available
- Sentinel2
- Sentinel3
- Planet Superdove
- Landsat5TM
- Landsat7ETM+
- Landsat8OLI
- Landsat9OLI

**NOTE:** To use the package properly, please use the spectral response functions files inside the folder `spectral_response_functions`
**NONE 2:** Sentinel3, Landsat8 and Landsat9 all have both mean srfs and relative standard deviations in the folder `spectral_response_functions`.It
is worth convoluting bands for both to assess the error for each band.

*More sensors will be addedd over time*

## Usage
The function `convolution` expects a pandas dataframe as input, where the index is a range of wavelengths between 350 and 2500, and each site is a column of observations for each wavelenght. If your reflectance data does not inlcude such range, plesae add rows of zeros for any missing wavelenght and do not leave any cell with NaNs.
