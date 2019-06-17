from setuptools import setup

setup(
    name='wrf_management',
    version='0.01',
    packages=['wrf_management', 'wrf_management.download'],
    url='',
    license='',
    author='diego aliaga',
    author_email='diego.aliaga@helsinki.fi',
    description='package to run wrf at taito', install_requires=['xarray', 'pandas', 'netCDF4']
)
