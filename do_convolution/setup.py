from setuptools import find_packages, setup

setup(
    name='sensor_convolution',
    packages=find_packages(include=['convolution', 'sensors']),
    version='0.1.0',
    description='''Python package that allow to convolve input hyperspectral
                   bands to satellite sensor bands.''',
    author='Davide Lomeo',
    author_email='davide.lomeo@kcl.ac.uk',
    # url='https://github.com/davidelomeo/satellite_sensors_convolutions,
    license='MIT',
)
