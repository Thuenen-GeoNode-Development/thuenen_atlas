from setuptools import find_packages, setup

import importer_datapackage


def read_file(path: str):
    with open(path, "r") as file:
        return file.read()


setup_requires = [
    "wheel",
]

setup(
    name="importer-datapackage",
    version="0.0.1",
    url="https://github.com/52north/geonode-contribs",
    description="Datapackage handler for the geonode-importer",
    long_description=read_file("README.md"),
    author="52north",
    author_email="info@52north.org",
    platforms="any",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django :: 3.0",
        "License :: OSI Approved :: GNU General Public License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "setuptools>=59",
        "frictionless==5.4.0",
        "geonode_importer>=1.0.3"
    ],
)
