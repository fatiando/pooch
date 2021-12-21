# Copyright (c) 2018 The Pooch Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Convert the requirements in the given file to their oldest version by
replacing >= with == in place.
"""
import sys


requirements_file = sys.argv[1]


def to_oldest(package):
    "Convert the specification to pin to the oldest version"
    oldest = package.split(",")[0].replace(">=", "==")
    return f"{oldest.strip()}\n"


with open(requirements_file) as input_file:
    requirements = [to_oldest(line) for line in input_file]

with open(requirements_file, "wt") as output_file:
    output_file.writelines(requirements)
