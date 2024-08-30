from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("drone_delivery_cython.pyx")
)
