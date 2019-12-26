"""
Parses collection for pertinent notes and generates result list
"""

import re

from aqt import mw
from aqt.utils import askUser
from .config import config
from .libaddon.debug import logger
from .wiki_connect import WikiConnect

# UI messages

WRN_RESCOUNT = ("<b>{}</b> relevant notes found.<br>"
                "The tooltip could take a lot of time to render and <br>"
                "temporarily slow down Anki.<br><br>"
                "<b>Are you sure you want to proceed?</b>")

# HTML format strings for results

html_reslist = """<div class="tt-reslist">{}</div>"""

html_field = """<div class="tt-fld">{}</div>"""

# RegExes for cloze marker removal

cloze_re_str = r"\{\{c(\d+)::(.*?)(::(.*?))?\}\}"
cloze_re = re.compile(cloze_re_str)


# Functions that compose tooltip content

def getContentFor(term, ignore_nid) -> str:
    """Compose tooltip content for search term.
    Returns HTML string."""
    conf = config["local"]

    note_content = None
    wiki = WikiConnect()

    # content = [wiki.format_extract(term)]
    content = [wiki.get_mobile_html(term)]


    extract_thumbnail = None  # TODO Implment thumbnails
    if extract_thumbnail is not None:
        content.append(extract_thumbnail)  # TODO need to format thumbnail into HTML

    if content:
        return html_reslist.format("".join(content))
    elif note_content is False:
        return ""
    elif note_content is None:
        return "No other results found." if conf["show_notfound_msg"] else ""



