# -*- coding: utf-8 -*-

# Popup Wikipedia Add-on for Anki
#
# Copyright (C)  2019-2020 Chris Culhane <cfculhane@gmail.com>
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
# Any modifications to this file must keep this entire header intact.


import json
import re
from os import PathLike
from pathlib import Path

from .config import config
from .libaddon._vendor.common.requests_cache import CachedSession


class WikiConnect(object):
    """ Handle connections to wikipedia and gets HTML formatted text of articles in either extract
    or mobile formats. """
    LANGUAGE = config["local"]["wiki_language"]
    REST_API_BASEURL = f"https://{LANGUAGE}.wikipedia.org/api/rest_v1/"
    MEDIAWIKI_API_BASEURL = f"https://{LANGUAGE}.wikipedia.org/w/api.php"
    WIKI_BASEURL = f"https://{LANGUAGE}.wikipedia.org/"

    def __init__(self, cache_expiry_hrs: int):
        self.session = CachedSession(expire_after=cache_expiry_hrs * 3600)  # expire_after is in seconds

    def get_summary(self, title: str) -> {}:
        """ Gets the raw summary JSON API response for a title"""
        req_url = f"{self.REST_API_BASEURL}page/summary/{self._parse_title(title)}"
        resp = self.session.get(url=req_url)
        return json.loads(resp.text)

    def get_mobile_html(self, title: str) -> str:
        """ Gets page as mobile-formatted html-text """
        summary = self.get_summary(title)  # Get preview first to handle disambiguation
        try:
            parsed_summary = self.summary_parser(summary)
            title = parsed_summary["title"]
            print(f"Parsed page title from summary = {title}")
        except ValueError:
            return f"No wikipedia entry found for '{title}'"
        req_url = f"{self.REST_API_BASEURL}page/mobile-html/{self._parse_title(title)}"
        resp = self.session.get(url=req_url)
        return f'<div class="wiki-result">{resp.text}</div>'
        # return f'<iframe srcdoc="{resp.text}"   sandbox />'

    def search(self, search_term: str):
        """
        Searches wikipedia.

        :param search_term:
        :returns:
        """
        raise NotImplementedError("search() yet handled properly!")
        req_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&format=json&srsearch=SEO&srwhat=text&srlimit=2"
        resp = self.session.get(url=req_url)

    def get_disam_links(self, title: str) -> [str]:
        """
        Gets all the disambiguation links. Assumes the title is a disambiguation page.

        :param title:
        :returns:
        """
        raise NotImplementedError("Disambiguation links not yet handled properly!")
        req_url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&list=querypage&qppage=DisambiguationPageLinks&qplimit=10"

        similar_titles = "https://en.wikipedia.org/w/api.php?action=query&list=alllinks&alfrom=Tissue&alnamespace=0&alunique=true"
        # alunique might be important?
        resp = self.session.get(url=req_url)

    def get_extract(self, title: str) -> str:
        """
        Gets and parses an extract html.
        See https://www.mediawiki.org/wiki/Extension:TextExtracts for details on the API.
        """
        summary = self.get_summary(title)
        try:
            parsed_summary = self.summary_parser(summary)
            title = parsed_summary["title"]
            print(f"Parsed page title from summary = {title}")
        except ValueError:
            return f"No wikipedia entry found for '{title}'"
        extract_params = {"action": "query",
                          "format": "json",
                          "prop": "extracts",
                          "titles": title,
                          "exchars": "1200",
                          "exintro": True,
                          "exlimit": "1"}

        resp = self.session.get(url=self.MEDIAWIKI_API_BASEURL, params=extract_params)
        extract_resp = json.loads(resp.text)
        extract_html = None
        for page in extract_resp["query"]["pages"].values():
            extract_html = page.get("extract")
            break  # there should only be one extract

        filled_html = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="utf-8"/>
                <meta
                        name="viewport"
                        content="width=device-width, initial-scale=1, shrink-to-fit=no"
                />
                <link
                        href="https://fonts.googleapis.com/css?family=Lato&display=swap"
                        rel="stylesheet"
                />
                <link rel="stylesheet" href="css/bootstrap.min.css"/>
                <title>{summary["titles"]["display"]}</title>
            </head>
            <div>
            """
        if summary.get("thumbnail") is not None:
            filled_html += f"""
                <img src="{summary["thumbnail"]["source"]}"
                     alt="{summary["titles"]["display"]}_img" style=
                     "width:{summary["thumbnail"]["width"]}px;
                     height:{summary["thumbnail"]["height"]}px;
                     float:right;margin-left:7px;margin-bottom:5px;">
                """
        filled_html += f"""
                <span style="font-size: 20px;">
                    <b>{summary["titles"]["display"]}</b></span>
                {extract_html or f"No extract found for {title}"}
                <p>Click <a href="{summary['content_urls']['desktop']['page']}">here for the full article.</a></p>
            </div>
        """

        return f'<div class="wiki-result">{filled_html}</div>'

    def summary_parser(self, summary_resp: {}) -> {}:
        """
        Handles disambiguation routing, search failuers

        :returns:
        """
        if summary_resp.get("title") == "Not found.":
            raise ValueError(f"No wikipedia article exists at {summary_resp['uri']}")
        elif summary_resp.get("type") == "disambiguation":
            print(f"handling disambiguation for {summary_resp['title']}")

            return summary_resp
        else:
            return summary_resp

    @staticmethod
    def _parse_title(title: str) -> str:
        """
        Formats title to format used in REST API (see: https://en.wikipedia.org/api/rest_v1/#/)

        :param title: Requested title
        :returns: Correctly formatted title
        """
        return title.strip().replace(" ", "_")

    def _fix_relative_pths(self, html_str: str) -> str:
        """ Changes relative paths to reference the wiki server, so that relative links inside HTMl
        work properly. Is not currently used due to some issues"""

        # TODO re-write to fix only the needed paths
        def srcrepl(match):  # Return the file contents with paths replaced
            print("<" + match.group(1) + match.group(2) + "=" + "\"" + self.WIKI_BASEURL + match.group(3) + match.group(
                4) + "\"" + ">")
            return "<" + match.group(1) + match.group(2) + "=" + "\"" + self.WIKI_BASEURL + match.group(
                3) + match.group(
                4) + "\"" + ">"

        p = re.compile(r"<(.*?)(src|href)=\"(?!http)(.*?)\"(.*?)>")
        return p.sub(srcrepl, html_str)

    @staticmethod
    def _write_htmlfile(html, pth: PathLike) -> int:
        return Path(pth).write_text(html, encoding="utf-8")
