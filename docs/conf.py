# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import datetime
import os
import pathlib
import sys

import coordinate_canvas

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

CURRENT_PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))
COORDINATE_CANVAS_PATH = CURRENT_PATH.parent.parent

sys.path.insert(0, str(COORDINATE_CANVAS_PATH))

project = "coordinate-canvas"
copyright = f"{datetime.date.today().year}, Paulo Sanchez and Contrbutors"
author = "Paulo Sanchez"
release = coordinate_canvas.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosummary",
    # "sphinx_tabs.tabs",
    "sphinx.ext.ifconfig",
    "sphinx_rtd_theme"
]
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

html_theme_options = {
    "github_user": "erlete",
    "github_repo": "coordinate-canvas",
    "github_banner": True,
    "github_button": True,
    "github_type": "star",
    "fixed_sidebar": True,
}

autodoc_default_options = {
    "member-order": "bysource",
}

add_module_names = False
