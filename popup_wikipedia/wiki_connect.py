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
from typing import Dict

from requests_cache import CachedSession


class WikiConnect(object):
    """ Handle connections to wikipedia and return preview data"""
    API_BASEURL = "https://en.wikipedia.org/api/rest_v1/"

    def __init__(self, cache_expiry_hrs: int):
        self.session = CachedSession(expire_after=cache_expiry_hrs * 3600)  # expire_after is in seconds

    def get_summary(self, title: str) -> {}:
        """ Gets the raw preview JSON API response for a title"""
        req_url = f"{self.API_BASEURL}page/summary/{self._parse_title(title)}"
        resp = self.session.get(url=req_url)
        return json.loads(resp.text)

    def get_mobile_html(self, title: str) -> str:
        """ Gets page as mobile-formatted text """
        summary = self.get_summary(title)  # Get preview first to handle disambiguation
        try:
            parsed_summary = self.summary_parser(summary)
        except ValueError:
            return f"No wikipedia entry found for '{title}'"
        req_url = f"{self.API_BASEURL}page/mobile-html/{self._parse_title(title)}"
        resp = self.session.get(url=req_url)
        return resp.text

    def search(self, search_term: str):
        """
        Searches wikipedia.

        :param search_term:
        :returns:
        """
        req_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&format=json&srsearch=SEO&srwhat=text&srlimit=2"
        resp = self.session.get(url=req_url)

    def get_disam_links(self, title: str) -> [str]:
        """
        Gets all the disambiguation links. Assumes the title is a disambiguation page.

        :param title:
        :returns:
        """
        req_url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&list=querypage&qppage=DisambiguationPageLinks&qplimit=10"
        resp = self.session.get(url=req_url)

    def get_extract(self, title: str) -> str:
        """ Makes a pretty popup preview in html"""
        summary = self.get_summary(title)
        try:
            parsed_summary = self.summary_parser(summary)
        except ValueError:
            return f"No wikipedia entry found for '{title}'"

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
                {summary["extract_html"]}
            </div>
        """
        return filled_html

    def summary_parser(self, summary_resp: Dict) -> Dict:
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


if __name__ == '__main__':
    wiki = WikiConnect()
