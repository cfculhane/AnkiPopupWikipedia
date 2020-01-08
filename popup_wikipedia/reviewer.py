# -*- coding: utf-8 -*-

# Popup Dictionary Add-on for Anki
#
# Copyright (C)  2018-2019 Aristotelis P. <https://glutanimate.com/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version, with the additions
# listed at the end of the license file that accompanied this program.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# NOTE: This program is subject to certain additional terms pursuant to
# Section 7 of the GNU Affero General Public License.  You should have
# received a copy of these additional terms immediately following the
# terms and conditions of the GNU Affero General Public License that
# accompanied this program.
#
# If not, please request a copy through one of the means of contact
# listed here: <https://glutanimate.com/contact/>.
#
# Any modifications to this file must keep this entire header intact.

"""
Modifications to Anki's Reviewer
"""

import json
import re

from anki.hooks import wrap, addHook
from aqt import mw
from aqt.qt import *
from aqt.reviewer import Reviewer
from .config import config
from .web import EXTENSION_HTML
from .wiki_connect import WikiConnect

# RegExes for cloze marker removal

cloze_re_str = r"\{\{c(\d+)::(.*?)(::(.*?))?\}\}"
cloze_re = re.compile(cloze_re_str)


# Functions that compose tooltip content
# Note that some of these functions are monkey-patched into the Anki codebase, so function names are
# not PEP-8 compliant

def get_wikicontent(term) -> str:
    """ Compose tooltip content for search term.
    Returns HTML string. """
    conf = config["local"]
    note_content = None
    wiki = WikiConnect(cache_expiry_hrs=conf["cache_expire_after"])

    popup_type: str = conf["popup_type"]
    if popup_type == "mobile":
        content = wiki.get_mobile_html(term)
    elif popup_type == "extract":
        content = wiki.get_extract(term)
    else:
        raise ValueError(f"popup_type {popup_type} not supported! Please check configuration file.")

    return content

# noinspection PyPep8Naming
def linkHandler(self, url, _old):
    """JS <-> Py bridge"""
    print(f"popup-wikipedia linkHandler url = {url}")
    print("---")
    if url.startswith("wikiLookup"):
        (cmd, payload) = url.split(":", 1)
        term = json.loads(payload)
        print(f"term = {term}")
        term = term.strip()
        return get_wikicontent(term)
    else:
        return _old(self, url)


# noinspection PyPep8Naming
def onRevHtml(self, _old):
    return _old(self) + EXTENSION_HTML


# noinspection PyPep8Naming
def patch_reviewer():
    """Monkey-patch Reviewer delayed in order to counteract bad practices
    in other add-ons that overwrite revHtml and _linkHandler in their
    entirety"""
    print("wiki patch_reviewer called")
    Reviewer.revHtml = wrap(Reviewer.revHtml, onRevHtml, "around")
    Reviewer._linkHandler = wrap(Reviewer._linkHandler, linkHandler, "around")


def wiki_hotkey() -> bool:
    if mw.state != "review":
        return False
    else:
        mw.reviewer.web.eval("invokeWikiTooltipAtSelectedElm();")
        return True


# noinspection PyPep8Naming
def setupShortcuts():
    QShortcut(QKeySequence(config["local"]["popup_hotkey"]),
              mw, activated=wiki_hotkey)


# noinspection PyPep8Naming
def initializeReviewer():
    setupShortcuts()
    addHook("profileLoaded", patch_reviewer)
