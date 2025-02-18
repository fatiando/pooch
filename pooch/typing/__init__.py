# Copyright (c) 2018 The Pooch Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
=============================
Typing (:mod:`pooch.typing`)
=============================

This module provides additional `PEP 484 <https://peps.python.org/pep-0484/>`_
type aliases used in ``pooch``'s codebase.

API
---

.. autosummary::
   :toctree: generated/

    Action
    Downloader
    FilePath
    FilePathInput
    ParsedURL
    Processor

"""

import os
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Literal,
    Optional,
    Protocol,
    TypedDict,
    Union,
)

# Import Pooch only if TYPE_CHECKING is true to avoid circular loops at runtime
if TYPE_CHECKING:
    from .. import Pooch


__all__ = [
    "Action",
    "Downloader",
    "FilePath",
    "FilePathInput",
    "ParsedURL",
    "Processor",
]


Action = Literal["download", "fetch", "update"]
FilePath = Union[str, os.PathLike]
FilePathInput = Union[FilePath, list[FilePath], tuple[FilePath]]
Processor = Callable[[str, Action, Optional["Pooch"]], Any]


class Downloader(Protocol):
    """
    A class used to define the type definition for the downloader function.
    """

    # pylint: disable=too-few-public-methods
    def __call__(  # noqa: E704
        self,
        fname: str,
        action: Optional[FilePath],
        pooch: Optional["Pooch"],
        *,
        check_only: Optional[bool] = None,
    ) -> Any: ...


class ParsedURL(TypedDict):
    protocol: str
    netloc: str
    path: str
