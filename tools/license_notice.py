# Copyright (c) 2018 The Pooch Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Add license notice to every source file if not present
"""
import sys
from pathlib import Path
from argparse import ArgumentParser
from pathspec import PathSpec


PROJECT = "pooch"
YEAR = "2018"
NOTICE = f"""
# Copyright (c) {YEAR} The {PROJECT.title()} Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
""".strip()
CHECK_HELP = """
Don't write the files, just return the status. Return code 0 means
nothing would change. Return code 1 means some files lacks the license notice.
"""


def get_gitignore(root):
    """
    Return a PathSpec matching gitignore content if present.
    This function is a modified version of the one present in Black
    (https://github.com/psf/black) available under MIT License.
    """
    gitignore = root / ".gitignore"
    lines = []
    if gitignore.is_file():
        with gitignore.open() as gi_file:
            lines = gi_file.readlines()
    return PathSpec.from_lines("gitwildmatch", lines)


def main():
    """
    Add license notice to every source file if not present or just check
    """
    # Create option parser
    parser = ArgumentParser(
        description=" Add license notice to every source file if not present."
    )
    parser.add_argument(
        "--check", action="store_true", dest="check", default=False, help=CHECK_HELP
    )
    args = parser.parse_args()

    gitignore = get_gitignore(Path("."))

    python_files = [
        path
        for path in Path(".").glob("**/*.py")
        if not str(path).startswith(".")
        if not gitignore.match_file(path)
    ]

    missing_notice_files = []
    for pyfile in python_files:
        code = pyfile.read_text()
        if not code.startswith(NOTICE):
            missing_notice_files.append(pyfile)

    if args.check:
        if missing_notice_files:
            print("License notice is missing in some source files! 💔")
            for pyfile in missing_notice_files:
                print(f"  {pyfile}")
            sys.exit(1)
        else:
            print("All source files have the license notice! 🎉")
            sys.exit(0)
    else:
        print("Successfully added license notice to:")
        for pyfile in missing_notice_files:
            code = pyfile.read_text()
            pyfile.write_text("\n".join([NOTICE, code]))
            print(f"  {pyfile}")
        sys.exit(0)


if __name__ == "__main__":
    main()
