# -*- coding: utf-8 -*-
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
# -- General configuration ------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
]

templates_path = ["_templates"]
source_suffix = ".rst"
master_doc = "index"
project = "rmoq"
copyright = "2015, Rolf Erik Lekang"
version = "1.0"
release = "1.0.0"
exclude_patterns = ["_build"]
pygments_style = "sphinx"

# -- Options for HTML output ----------------------------------------------

html_theme = "default"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Output file base name for HTML help builder.
htmlhelp_basename = "rmoqdoc"


# -- Options for LaTeX output ---------------------------------------------

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    ("index", "rmoq.tex", "rmoq Documentation", "Rolf Erik Lekang", "manual"),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [("index", "rmoq", "rmoq Documentation", ["Rolf Erik Lekang"], 1)]

# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        "index",
        "rmoq",
        "rmoq Documentation",
        "Rolf Erik Lekang",
        "rmoq",
        "One line description of project.",
        "Miscellaneous",
    ),
]
