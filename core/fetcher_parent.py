import requests
import bs4


class Fetcher:
    @staticmethod
    def http_get(url: str, **params) -> requests.Response:
        return requests.get(url, params)

    @staticmethod
    def html_bs_parser(html: str) -> bs4.BeautifulSoup:
        return bs4.BeautifulSoup(html, 'html.parser')
