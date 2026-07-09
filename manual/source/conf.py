# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Algodal Text Parser Generator"
copyright = "2026, Alrick Grandison"
author = "Alrick Grandison"
release = "August 2026"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["myst_parser", "sphinx_design", "sphinxcontrib.mermaid"]

myst_enable_extensions = [
    "colon_fence",  # ::: blocks (admonitions)
    "deflist",  # definition lists
    "tasklist",  # - [ ] checkboxes
    "html_admonition",  # <div class="admonition"> blocks
    "html_image",  # <img> tags
    "attrs_inline",  # inline attributes {.class}
    "attrs_block",  # block attributes
    "fieldlist",  # :field: value lists
    "substitution",  # {{ LANG }} replacements (defined in myst_substitutions)
]

source_suffix = {".rst": "restructuredtext", ".md": "markdown"}

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

html_theme_options = {
    "logo_only": False,
    "prev_next_buttons_location": "bottom",
    "style_external_links": False,
    # Toc options
    "collapse_navigation": True,
    "sticky_navigation": True,
    "navigation_depth": 4,
    "includehidden": True,
    "titles_only": False,
}
