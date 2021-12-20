# Copyright (c) 2018 The Pooch Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Export the run-time requirements from setup.cfg to a requirement.txt format.
Prints to STDOUT. If the "minimal" argument is passed, will replace >= with ==
to force dependencies to the minimal supported version.

Modified from https://github.com/Unidata/MetPy
"""
import sys
import configparser

# Read the setup.cfg
config = configparser.ConfigParser()
config.read("setup.cfg")

minimal = "minimal" in sys.argv

print("# Run-time dependencies")
for package in config["options"]["install_requires"].strip().split("\n"):
    if minimal:
        package = package.replace(">=", "==")
    print(package)
