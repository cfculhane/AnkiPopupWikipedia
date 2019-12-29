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
from .web import popup_integrator
from .wiki_connect import WikiConnect

html_reslist = """<div class="tt-reslist">{}</div>"""

html_field = """<div class="tt-fld">{}</div>"""

# RegExes for cloze marker removal

cloze_re_str = r"\{\{c(\d+)::(.*?)(::(.*?))?\}\}"
cloze_re = re.compile(cloze_re_str)


# Functions that compose tooltip content

def getContentFor(term) -> str:
    """Compose tooltip content for search term.
    Returns HTML string."""
    conf = config["local"]
    note_content = None
    wiki = WikiConnect()

    popup_type: str = config["local"]["popup_type"]
    if popup_type == "mobile":
        content = [wiki.get_mobile_html(term)]
    elif popup_type == "extract":
        content = [wiki.get_extract(term)]
    else:
        raise ValueError(f"popup_type {popup_type} not supported! Please check configuration file.")

    extract_thumbnail = None  # TODO Implement thumbnails
    if extract_thumbnail is not None:
        content.append(extract_thumbnail)  # TODO need to format thumbnail into HTML

    if content:
        return html_reslist.format("".join(content))
    elif note_content is False:
        return ""
    elif note_content is None:
        return "No other results found." if conf["show_notfound_msg"] else ""


def linkHandler(self, url, _old):
    """JS <-> Py bridge"""
    print(f"url = {url}")
    if url.startswith("wikiLookup"):
        (cmd, payload) = url.split(":", 1)
        term, ignore_nid = json.loads(payload)
        print(f"term = {term}, ignore_nid = {ignore_nid}")
        term = term.strip()
        return getContentFor(term)
    else:
        return _old(self, url)


def onRevHtml(self, _old):
    return _old(self) + popup_integrator


def onProfileLoaded():
    """Monkey-patch Reviewer delayed in order to counteract bad practices
    in other add-ons that overwrite revHtml and _linkHandler in their
    entirety"""
    Reviewer.revHtml = wrap(Reviewer.revHtml, onRevHtml, "around")
    Reviewer._linkHandler = wrap(Reviewer._linkHandler, linkHandler, "around")


def onReviewerHotkey():
    if mw.state != "review":
        return
    mw.reviewer.web.eval("invokeWikiTooltipAtSelectedElm();")


def setupShortcuts():
    QShortcut(QKeySequence(config["local"]["popup_hotkey"]),
              mw, activated=onReviewerHotkey)


def initializeReviewer():
    setupShortcuts()
    addHook("profileLoaded", onProfileLoaded)
