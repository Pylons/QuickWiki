"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
from webhelpers.html import HTML, escape, literal, url_escape
from webhelpers.html.tags import *
from webhelpers.html.secure_form import secure_form
from webhelpers.pylonslib import Flash as _Flash

flash = _Flash()
