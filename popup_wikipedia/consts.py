"""
Addon-wide constants
"""

from ._version import __version__

__all__ = ["ADDON"]


class ADDON(object):
    """Class storing general add-on properties
    Property names need to be all-uppercase with no leading underscores
    """
    NAME = "Anki Wiki Popup"
    MODULE = "anki_wiki_popup"
    ID = "0000000000"
    VERSION = __version__
    LICENSE = "GNU AGPLv3"
    AUTHORS = (
        {"name": "Chris Culhane", "years": "2019",
         "contact": "https://github.com/cfculhane"},
    )
    AUTHOR_MAIL = "cfculhane@gmail.com"
    LIBRARIES = (
        {"name": "qTip2", "version": "v2.1.1",
         "author": "Craig Michael Thompson", "license": "MIT license",
         "url": "http://qtip2.com/"},
        {"name": "jQuery.highlight", "version": "5",
         "author": "Johann Burkard", "license": "MIT license",
         "url": "https://johannburkard.de/blog/programming/javascript/highlight-javascript-text-higlighting-jquery-plugin.html"},
    )
    CONTRIBUTORS = ()
    SPONSORS = ()
    LINKS = {
        "description": f"https://ankiweb.net/shared/info/{ID}",
        "rate": f"https://ankiweb.net/shared/review/{ID}",
        "help": ""
    }
