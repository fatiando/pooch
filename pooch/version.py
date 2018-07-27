# pylint: disable=invalid-name
"""
Get the version number and git commit hash from versioneer.
"""
from ._version import get_versions


full_version = get_versions()["version"]
git_revision = get_versions()["full-revisionid"]
