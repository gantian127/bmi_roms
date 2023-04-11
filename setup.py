from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="bmi_roms",
    version='0.1.0',
    author="Tian Gan",
    author_email="jamy127@foxmail.com",
    description="BMI implementation for ROMS model data https://www.myroms.org/",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="http://csdms.colorado.edu",
    packages=find_packages(exclude=("tests*",)),
    install_requires=open("requirements.txt", "r").read().splitlines(),
)
