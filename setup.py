from setuptools import find_packages, setup

setup(
    name = 'convolution',
    install_requires = ['numpy', 'pandas'],
    packages = find_packages(),
    version = '0.1.0',
    description = '''Python package that to convolve input hyperspectral
                     bands to satellite sensor bands.''',
    author='Davide Lomeo',
    author_email='davide.lomeo@kcl.ac.uk',
    # url='https://github.com/davidelomeo/satellite_sensors_convolutions,
    license='MIT',
    package_data={'': ['spectral_response_functions/*']}
)
