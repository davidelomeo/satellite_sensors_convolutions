## Description
Package that convolves input hyperspectral reflectance data to user-defined sensor bands (Full List in the documentation of the Convolution class or in the README in the main page of the branch)

## Functions and Classes
The function marked as being bith function and method are functions that can be either called or used in a .map() method.
- `Convolution` : CLASS - create the Convolution data type and contruct the workflow according to input sensor name.
- `get_modified_reflectance_data()` : FUNCTION/ METHOD - returning the modified input reflectance data if originally not in range 350-2500nm
- `get_central_wavelengths()` : FUNCTION/ METHOD - returning a list of bands names and respective central wavelenghts according to input sensor name.
- `get_srf()` : FUNCTION/ METHOD - returning the spectral response function of the input sensor name.en objects. 
- `do_convolutions()` : FUNCTION/ METHOD - returning the convoluteed bands for the input sensor name
