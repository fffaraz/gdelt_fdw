import subprocess
from setuptools import setup, find_packages, Extension

setup(
  name='gdelt_fdw',
  version='1.0.0',
  author='Faraz Fallahi',
  license='Postgresql',
  packages=['gdelt_fdw']
)
