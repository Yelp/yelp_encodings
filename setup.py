from setuptools import find_packages
from setuptools import setup

setup(
    name="Encoding Utilities",
    version="0.1.0",
    packages=find_packages('.', exclude=('tests*')),
)
