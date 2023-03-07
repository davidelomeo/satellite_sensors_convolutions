from setuptools import find_packages, setup, find_namespace_packages

setup(
    name = 'convolution',
    install_requires = ['numpy', 'pandas'],
    packages=find_namespace_packages(where="convolution"),
    version = '0.1.0',
    description = '''Python package that to convolve input hyperspectral
                     bands to satellite sensor bands.''',
    author='Davide Lomeo',
    author_email='davide.lomeo@kcl.ac.uk',
    # url='https://github.com/davidelomeo/satellite_sensors_convolutions,
    license='MIT',
    # include_package_data=True,
    package_data={'spectral_response_functions.Landsat': ['*.csv'],
                  'spectral_response_functions.Planet': ['*.csv'],
                  'spectral_response_functions.Sentinel2': ['*.csv'],
                  'spectral_response_functions.Sentinel3': ['*.csv']},
)
