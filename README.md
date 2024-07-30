# Satellite Sensors Convolutions

This repository contains the Convolution class that allows to convolve in-situ hyperspectral sprectral measurements to target satellite sensors bands.

## Satellites currently available

- TM_L5,
- ETM+_L7,
- OLI_L8,
- OLI_L9,
- MERIS,
- MSI_S2A,
- MSI_S2B,
- OLCI_S3A,
- OLCI_S3B,
- MODIS_AQUA,
- MODIS_TERRA
- Superdove,

*More sensors will be addedd over time*

## Usage Instructions

The class `Convolution` expects a pandas dataframe and a string that matches one of the satellites sensors listed above as input. The index column of the dataframe
needs to be the range of available wavelengths, and each column is a different observation.

The module will return a dataframe with convolved bands to the target sensor.

Example of usage if returning one dataframe (i.e., ***Sentinel2a-b***, ***Superdove***, ***Landsat5TM***, ***Landsat7ETM+***):

```
convolution_constructor = convolution.Convolution(*input_rrs*, *sensor_name*)
convolved_bands = convolution_constructor.do_convolutions()
print(convolved_bands)
```

The user may also use the following method to return the SRF abd related banpass information of the input sensor name:

```
convolution_constructor = convolution.Convolution(*input_rrs*, *sensor_name*)
srf, bandpass = convolution_constructor.get_srf_and_bandpass()
print(srf)
print(bandpass)
```
