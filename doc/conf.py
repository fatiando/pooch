# -*- coding: utf-8 -*-
import sys
import os
import datetime
import sphinx_rtd_theme

from pooch.version import full_version

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.doctest",
    "sphinx.ext.viewcode",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "numpydoc",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "pandas": ("http://pandas.pydata.org/pandas-docs/stable/", None),
    "requests": ("https://2.python-requests.org/en/stable/", None),
}

# Autosummary pages will be generated by sphinx-autogen instead of sphinx-build
autosummary_generate = False

numpydoc_class_members_toctree = False

# Always show the source code that generates a plot
plot_include_source = True
plot_formats = ["png"]

# Sphinx project configuration
templates_path = ["_templates"]
exclude_patterns = ["_build", "**.ipynb_checkpoints"]
source_suffix = ".rst"
# The encoding of source files.
source_encoding = "utf-8-sig"
master_doc = "index"

# General information about the project
year = datetime.date.today().year
project = "Pooch"
copyright = "2018-{}, The Pooch Developers".format(year)
if len(full_version.split("+")) > 1 or full_version == "unknown":
    version = "dev"
else:
    version = full_version

# These enable substitutions using |variable| in the rst files
rst_epilog = """
.. |year| replace:: {year}
""".format(
    year=year
)

html_last_updated_fmt = "%b %d, %Y"
html_title = project
html_short_title = project
html_logo = "_static/pooch-logo.png"
html_favicon = "_static/favicon.png"
html_static_path = ["_static"]
html_extra_path = []
pygments_style = "default"
add_function_parentheses = False
html_show_sourcelink = False
html_show_sphinx = True
html_show_copyright = True

# Theme config
html_theme = "sphinx_rtd_theme"
html_theme_options = {"logo_only": True, "display_version": True}
html_context = {
    "menu_links_name": "Getting help and contributing",
    "menu_links": [
        (
            '<i class="fa fa-external-link-square fa-fw"></i> Fatiando a Terra',
            "https://www.fatiando.org",
        ),
        (
            '<i class="fa fa-users fa-fw"></i> Contributing',
            "https://github.com/fatiando/pooch/blob/master/CONTRIBUTING.md",
        ),
        (
            '<i class="fa fa-gavel fa-fw"></i> Code of Conduct',
            "https://github.com/fatiando/pooch/blob/master/CODE_OF_CONDUCT.md",
        ),
        ('<i class="fa fa-comment fa-fw"></i> Contact', "http://contact.fatiando.org"),
        (
            '<i class="fa fa-github fa-fw"></i> Source Code',
            "https://github.com/fatiando/pooch",
        ),
    ],
    # Custom variables to enable "Improve this page"" and "Download notebook"
    # links
    "doc_path": "doc",
    "galleries": "",
    "gallery_dir": "",
    "github_repo": "fatiando/pooch",
    "github_version": "master",
}


# Load the custom CSS files (needs sphinx >= 1.6 for this to work)
def setup(app):
    app.add_stylesheet("style.css")
