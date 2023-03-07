from setuptools import find_packages, setup
reqs = ['numpy', 'pandas', 'pkg_resources']

setup(
    name = 'convolution',
    packages = find_packages(),
    install_requires = reqs,
    version = '0.1.0',
    description = '''Python package that to convolve input hyperspectral
                     bands to satellite sensor bands.''',
    author='Davide Lomeo',
    author_email='davide.lomeo@kcl.ac.uk',
    # url='https://github.com/davidelomeo/satellite_sensors_convolutions,
    license='MIT',
    # include_package_data=True,
    package_data={'Landsat': ['spectral_response_functions/Landsat/*.csv'],
                  'Planet': ['spectral_response_functions/Planet/*.csv'],
                  'Sentinel2': ['spectral_response_functions/Sentinel2/*.csv'],
                  'Sentinel3': ['spectral_response_functions/Sentinel3/*.csv']},
)
