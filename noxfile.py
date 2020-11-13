# Copyright (c) 2018 The Pooch Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Configuration for setting up virtual environments to check code style, run
tests, build documentation, and create package distributions for PyPI.

Instructions
------------

* List all available sessions: 'nox -l'
* Run all sessions: 'nox' (without arguments)
* Run only a particular session: 'nox -s SESSION' (e.g., 'nox -s test-3.8')
* Only create virtual environments and install packages: 'nox --install-only'
  (use this to prepare for working offline)
* Run a session but skip the install step: 'nox -s SESSION -- skip-install'
* Run a session and list installed packages:
  'nox -s SESSION -- list-packages'
* Run only selected code style checkers: 'nox -s check -- CHECKER' (could be
  'black', 'flake8', or 'pylint')
* Open the documentation in a browser after building: 'nox -s docs -- show'
* Create a sandbox conda environment with all dependencies and the package
  installed: 'nox -s sandbox-PROJECT' (substitute for the project name). You
  can then activate it with 'conda activate .nox/sandbox-PROJECT' (from the
  project folder) and run things like 'python', 'ipython', and 'jupyter'.
  Useful for experimentation.

"""
from pathlib import Path
import shutil
import webbrowser

import nox


# CONFIGURE NOX
# Always reuse environments. Use --no-reuse-existing-virtualenvs to disable.
nox.options.reuse_existing_virtualenvs = True

# Custom command-line arguments that we're implementing
NOX_ARGS = ["skip-install", "list-packages", "show"]


PACKAGE = "pooch"
PYTHON_VERSIONS = ["3.9", "3.8", "3.7", "3.6"]
DOCS = Path("doc")
REQUIREMENTS = {
    "run": "requirements.txt",
    "test": str(Path("env") / "requirements-test.txt"),
    "optional": str(Path("env") / "requirements-optional.txt"),
    "docs": str(Path("env") / "requirements-docs.txt"),
    "style": str(Path("env") / "requirements-style.txt"),
    "build": str(Path("env") / "requirements-build.txt"),
    "sandbox": str(Path("env") / "requirements-sandbox.txt"),
}

STYLE_ARGS = {
    "pylint": [PACKAGE, "setup.py"],
    "flake8": [PACKAGE, "setup.py", str(DOCS / "conf.py")],
    "black": [
        "--check",
        PACKAGE,
        "setup.py",
        str(DOCS / "conf.py"),
        "noxfile.py",
    ],
}

# Use absolute paths for pytest otherwise it struggles to pick up coverage info
PYTEST_ARGS = [
    f"--cov-config={Path('.coveragerc').resolve()}",
    "--cov-report=term-missing",
    f"--cov={PACKAGE}",
    "--doctest-modules",
    '--doctest-glob="*.rst"',
    "-v",
    "--pyargs",
]
RST_FILES = [str(p.resolve()) for p in Path("doc").glob("**/*.rst")]


@nox.session()
def format(session):
    "Run 'black' to format the code"
    install_requirements(session, ["style"])
    session.run("black", *STYLE_ARGS["black"][1:])


@nox.session()
def check(session):
    "Check code style"
    install_requirements(session, ["style"])
    list_packages(session)
    args = list(set(session.posargs).difference(NOX_ARGS))
    if args:
        checks = args
    else:
        checks = ["black", "flake8", "pylint"]
    for check in checks:
        session.run(check, *STYLE_ARGS[check])


@nox.session()
def build(session):
    "Build source and wheel distributions"
    install_requirements(session, ["build"])
    packages = build_project(session, install=False)
    for package in packages:
        session.run("twine", "check", str(package))
    list_packages(session)


@nox.session()
def test(session):
    "Run tests and measure coverage (using pip)"
    _run_tests(session, optional=False, package_manager="pip")


@nox.session()
def test_optional(session):
    "Run tests with optional dependencies and measure coverage (using pip)"
    _run_tests(session, optional=True, package_manager="pip")


@nox.session(venv_backend="conda", python=PYTHON_VERSIONS)
def test_conda(session):
    "Run tests and measure coverage (using conda)"
    _run_tests(session, optional=False, package_manager="conda")


@nox.session(venv_backend="conda", python=PYTHON_VERSIONS)
def test_conda_optional(session):
    "Run tests with optional dependencies and measure coverage (using conda)"
    _run_tests(session, optional=True, package_manager="conda")


def _run_tests(session, optional, package_manager):
    "Run the tests given the desired configuration"
    requirements = ["build", "run", "test"]
    if optional:
        requirements.append("optional")
    install_requirements(session, requirements, package_manager=package_manager)
    build_project(session, install=True)
    list_packages(session, package_manager=package_manager)
    run_pytest(session)


@nox.session()
def docs(session):
    "Build the documentation web pages"
    install_requirements(session, ["build", "run", "docs", "optional"])
    build_project(session, install=True)
    list_packages(session, package_manager="pip")
    # Generate the API reference
    session.run(
        "sphinx-autogen",
        "-i",
        "-t",
        str(DOCS / "_templates"),
        "-o",
        str(DOCS / "api" / "generated"),
        str(DOCS / "api" / "index.rst"),
    )
    # Build the HTML pages
    html = DOCS / "_build" / "html"
    session.run(
        "sphinx-build",
        "-d",
        str(DOCS / "_build" / "doctrees"),
        "doc",
        str(html),
    )
    if session.posargs and "show" in session.posargs:
        session.log("Opening built docs in the default web browser.")
        webbrowser.open(f"file://{(html / 'index.html').resolve()}")


@nox.session(venv_backend="conda", python="3.8", name=f"sandbox-{PACKAGE}")
def sandbox(session):
    "Create a sandbox conda environment to use outside of nox"
    install_requirements(
        session, ["build", "style", "run", "docs", "sandbox"], package_manager="conda"
    )
    build_project(session, install=True)
    list_packages(session, package_manager="conda")


@nox.session(venv_backend="none")
def clean(session):
    """
    Remove all files generated by the build process
    """
    files = [
        Path("build"),
        Path("dist"),
        Path("MANIFEST"),
        Path(".coverage"),
        Path(".pytest_cache"),
        Path("__pycache__"),
        DOCS / "_build",
        DOCS / "api" / "generated",
        DOCS / "gallery",
        DOCS / "tutorials",
    ]
    files.extend(Path(PACKAGE).glob("**/*.pyc"))
    files.extend(Path(".").glob(".coverage.*"))
    files.extend(Path(PACKAGE).glob("**/__pycache__"))
    files.extend(Path(".").glob("*.egg-info"))
    files.extend(Path(".").glob("**/.ipynb_checkpoints"))
    for f in files:
        if f.exists():
            session.log(f"removing: {f}")
            if f.is_dir():
                shutil.rmtree(f)
            else:
                f.unlink()


# UTILITY FUNCTIONS
###############################################################################


def install_requirements(session, requirements, package_manager="pip"):
    """
    Install dependencies from the requirements files specified in REQUIREMENTS.

    *requirements* should be a list of keywords defined in the REQUIREMENTS
    dictionary. Set *package_manager* to "conda" if using the conda backend for
    virtual environments.
    """
    if package_manager not in {"pip", "conda"}:
        raise ValueError(f"Invalid package manager '{package_manager}'")
    if session.posargs and "skip-install" in session.posargs:
        session.log("Skipping install steps.")
        return
    arg_name = {"pip": "-r", "conda": "--file"}
    args = []
    for requirement in requirements:
        args.extend([arg_name[package_manager], REQUIREMENTS[requirement]])
    if package_manager == "pip":
        session.install(*args)
    elif package_manager == "conda":
        session.conda_install(
            "--channel=conda-forge",
            "--channel=defaults",
            *args,
        )


def list_packages(session, package_manager="pip"):
    """
    List installed packages in the virtual environment.

    If the argument 'list-packages' is passed to the nox session, will list the
    installed packages in the virtual environment (using the package manager
    specified).

    Example: 'nox -s test-3.7 -- list-packages'
    """
    if package_manager not in {"pip", "conda"}:
        raise ValueError(f"Invalid package manager '{package_manager}'")
    if session.posargs and "list-packages" in session.posargs:
        session.log(f"Packages installed ({package_manager}):")
        if package_manager == "pip":
            session.run("pip", "freeze")
        elif package_manager == "conda":
            session.run("conda", "list")


def run_pytest(session):
    """
    Run tests with pytest in a separate folder.
    """
    tmpdir = session.create_tmp()
    session.cd(tmpdir)
    session.run("pytest", *PYTEST_ARGS, PACKAGE, *RST_FILES)
    session.run("coverage", "xml", "-o", ".coverage.xml")
    # Copy the coverage information back so it can be reported
    for f in Path(".").glob(".coverage*"):
        shutil.copy(f, Path(__file__).parent)


def build_project(session, install=False):
    """
    Build source and wheel packages for the project and returns their path.
    If 'install==True', will also install the package.
    """
    session.log("Build source and wheel distributions:")
    if Path("dist").exists():
        shutil.rmtree("dist")
    session.run("python", "setup.py", "sdist", "bdist_wheel", silent=True)
    packages = list(Path("dist").glob("*"))
    if install and packages:
        session.install("--force-reinstall", "--no-deps", str(packages[0]))
    return packages
