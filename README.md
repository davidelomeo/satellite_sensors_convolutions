# Satellite Sensors Convolutions
This repository contains the Convolution class that allows to convolve in-situ sprectral measurements to target satellite sensors bands.

## Satellites currently available
- Sentinel2
- Sentinel3
- PlanetScope Superdove
- Landsat5TM
- Landsat7ETM+
- Landsat8OLI
- Landsat9OLI

**NOTE:** It is advised to use the spectral response functions files inside the folder `spectral_response_functions` to avoid errors. The ranges used for 
the convolutions are indeed based on these files. Spectral response functions were taken from USGS, PlanetLab and ESA's websites.
**NONE 2:** Sentinel3, Landsat8 and Landsat9 have both mean srfs and relative standard deviations in the folder `spectral_response_functions`. 
The means and standard deviations were obtained by averaging the spectral responses within 1nm ranges. It is worth convoluting bands for both 
means and standard deviations to assess the errors for each band.

*More sensors will be addedd over time*

## Usage
The class `Convolution` expects a pandas dataframe as input, where the index is a range of wavelengths between 350 and 2500 at 1nm steps, and each column 
is a different observation (Site). If your reflectance data does not inlcude such range, plesae add rows of zeros for any missing wavelenght and do not leave
any cell with NaNs.
