"""
Addon-wide constants
"""

from ._version import __version__

__all__ = ["ADDON"]


class ADDON(object):
    """Class storing general add-on properties
    Property names need to be all-uppercase with no leading underscores
    """
    NAME = "Popup Wikipedia"
    MODULE = "popup_wikipedia"
    ID = "395343016"
    VERSION = __version__
    LICENSE = "GNU AGPLv3"
    AUTHORS = (
        {"name": "Chris Culhane", "years": "2019",
         "contact": "https://github.com/cfculhane"},
    )
    AUTHOR_MAIL = "cfculhane@gmail.com"
    LIBRARIES = (
        {"name": "qTip2", "version": "3.0.3",
         "author": "Craig Michael Thompson", "license": "MIT license",
         "url": "http://qtip2.com/"},
    )
    CONTRIBUTORS = ()
    SPONSORS = ()
    LINKS = {
        "description": f"https://ankiweb.net/shared/info/{ID}",
        "rate": f"https://ankiweb.net/shared/review/{ID}",
        "help": ""
    }
