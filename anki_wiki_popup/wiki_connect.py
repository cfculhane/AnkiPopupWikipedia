import json

import requests


class WikiConnect(object):
    """ Handle connections to wikipedia and return preview data"""
    API_BASEURL = "https://en.wikipedia.org/api/rest_v1/"

    def __init__(self):
        self.session = requests.Session()

    def get_preview(self, title: str) -> {}:
        req_url = f"{self.API_BASEURL}page/summary/{self._parse_title(title)}"
        resp = self.session.get(url=req_url)
        return json.loads(resp.text)

    def get_extract(self, title: str) -> str:
        return self.get_preview(title=title)["extract_html"]

    def get_mobile_html(self, title: str) -> str:
        """ Gets page as mobile-formatted text """
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

    def format_extract(self, title: str) -> str:
        """ Makes a pretty popup preview in html"""
        preview = self.get_preview(title)

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
                <title>{preview["titles"]["display"]}</title>
            </head>
            <div>
            """
        if preview.get("thumbnail") is not None:
            filled_html += f"""
                <img src="{preview["thumbnail"]["source"]}"
                     alt="{preview["titles"]["display"]}_img" style=
                     "width:{preview["thumbnail"]["width"]}px;
                     height:{preview["thumbnail"]["height"]}px;
                     float:right;margin-left:7px;margin-bottom:5px;">
                """
        filled_html += f"""
                <span style="font-size: 20px;">
                    <b>{preview["titles"]["display"]}</b></span>
                {preview["extract_html"]}
            </div>
        """
        return filled_html

    def _diambig_handler(self, ):
        """
        Handles disambiguation routing

        :returns:
        """
        pass

    def _parse_title(self, title: str) -> str:
        """
        Formats title to format used in REST API (see: https://en.wikipedia.org/api/rest_v1/#/)

        :param title: Requested title
        :returns: Correctly formatted title
        """
        return title.strip().replace(" ", "_")


if __name__ == '__main__':
    wiki = WikiConnect()
