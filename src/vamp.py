import requests
from lxml import html
from urllib import parse

# TODO: Detect redirect statuses


class Vamp(object):

    def __init__(self, url):
        self.url = url

    def scan_page(self):
        """
        Given the configured url,
        and return dead links

        Args:
                None

        Return:
                Dictionary: Containing key value links and status
        """
        response = requests.get(self.url)
        page_urls = self.get_page_urls(response.text)
        urls_and_statuses = self._check_url_status(page_urls)
        dead_links = self._filter_ok_responses(urls_and_statuses)
        return dead_links

    def get_page_urls(self, html_page):
        """
        Given an HTML page, return a dictionary with all the URL
        found on the page

        Args:
            html_page: A string with HTML formated content

        Returns:
            A list with HTML links or and empty dictionary
        """
        tree = html.fromstring(html_page)
        links = tree.xpath('//a/@href')
        return(links)

    def _check_url_status(self, urls):
        """
        Given a list of URLs perform get requests and check http
        status of each URL

        Args:
                urls: A list of urls

        Returns:
                A dictionary with key values of urls and http statuses

        """
        url_results = {}
        http_urls = self.sanitize_urls(urls)

        for item in http_urls:
            if item.startswith(r'/'):
                item = parse.urljoin(self.url, item)

            url_response = requests.get(item)
            url_results[item] = url_response.status_code

        return url_results

    def sanitize_urls(self, urls):
        """
        Takes a list of urls and removes all items that do not start with http

        Args:
                urls: A list of urls

        Returns:
                A list of only urls that start with http
        """
        return [item for item in urls if item.startswith('http') or item.startswith(r'/')]

    def _filter_ok_responses(self, urls_and_statuses):
        """
        Go through a dictionary of urls and http statuses and
        filter out 200 responses

        Args:
                urls_and_statuses: A dictionary of links and responses

        Returns:
                A dictionary if only items that have 200 for values
        """
        return {url: status_code for
                url, status_code in urls_and_statuses.items()
                if status_code is not 200}
