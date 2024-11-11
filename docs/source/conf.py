import os
import sys
sys.path.insert(0, os.path.abspath('../../'))  # Adjust this if your structure is different




# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'EarthPicture'
copyright = '2024, Louis Pauchet (UNIS - INSA Rouen)'
author = 'Louis Pauchet (UNIS - INSA Rouen)'
release = '0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',       # Generates documentation from docstrings
    'sphinx.ext.napoleon',      # Supports Google-style and NumPy-style docstrings
    'sphinx.ext.viewcode',      # Adds links to source code in the documentation
]


templates_path = ['_templates']
exclude_patterns = []

autodoc_mock_imports = ["sentinelsat", "shapely"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
