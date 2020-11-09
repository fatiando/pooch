# Copyright (c) 2018 The Pooch Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
# pylint: disable=invalid-name
"""
Get the version number and git commit hash from versioneer.
"""
from ._version import get_versions


full_version = get_versions()["version"]
git_revision = get_versions()["full-revisionid"]
