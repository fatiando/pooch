# Copyright (c) 2018 The Pooch Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Export the run-time requirements from setup.cfg to a requirement.txt format.
Modified from https://github.com/Unidata/MetPy
"""
import configparser

# Read the setup.cfg
config = configparser.ConfigParser()
config.read("setup.cfg")

print("# Run-time dependencies")
for package in config["options"]["install_requires"].strip().split("\n"):
    print(package.strip())
