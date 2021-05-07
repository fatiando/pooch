# Copyright (c) 2018 The Pooch Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Build and install the project.

Uses setuptools_scm to manage version numbers using git tags.
"""
import os
from setuptools import setup, find_packages


NAME = "pooch"
FULLNAME = "Pooch"
AUTHOR = "Leonardo Uieda"
AUTHOR_EMAIL = "leouieda@gmail.com"
MAINTAINER = AUTHOR
MAINTAINER_EMAIL = AUTHOR_EMAIL
LICENSE = "BSD License"
URL = "https://github.com/fatiando/pooch"
DESCRIPTION = (
    "Pooch manages your Python library's sample data files: "
    "it automatically downloads and stores them in a local directory, "
    "with support for versioning and corruption checks."
)
KEYWORDS = ""
with open("README.rst") as f:
    LONG_DESCRIPTION = "".join(f.readlines())

CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Science/Research",
    "Intended Audience :: Developers",
    "Intended Audience :: Education",
    "Topic :: Scientific/Engineering",
    "Topic :: Software Development :: Libraries",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3 :: Only",
    f"License :: OSI Approved :: {LICENSE}",
]
PLATFORMS = "Any"
PACKAGES = find_packages(exclude=["doc"])
SCRIPTS = []
PACKAGE_DATA = {
    "pooch.tests": [
        os.path.join("data", "*"),
        os.path.join("data", "store", "*"),
        os.path.join("data", "store", "subdir", "*"),
    ]
}
INSTALL_REQUIRES = ["requests", "packaging", "appdirs"]
PYTHON_REQUIRES = ">=3.6"
SETUP_REQUIRES = ["setuptools_scm"]
# Configuration for setuptools-scm
USE_SCM_VERSION = {
    "relative_to": __file__,
    "version_scheme": "post-release",
    "local_scheme": "node-and-date",
    "write_to": f"{NAME}/_version.py",
}

if __name__ == "__main__":
    setup(
        name=NAME,
        fullname=FULLNAME,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        use_scm_version=USE_SCM_VERSION,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        license=LICENSE,
        url=URL,
        platforms=PLATFORMS,
        scripts=SCRIPTS,
        packages=PACKAGES,
        package_data=PACKAGE_DATA,
        classifiers=CLASSIFIERS,
        keywords=KEYWORDS,
        install_requires=INSTALL_REQUIRES,
        python_requires=PYTHON_REQUIRES,
        setup_requires=SETUP_REQUIRES,
    )
