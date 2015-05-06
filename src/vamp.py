import requests
from lxml import html

# TODO: Detect relative urls on a page


class Vamp(object):

    def __init__(self, url):
        self.url = url

    def scan_page(self):
        """
        Given the configured url,
        make a request to the site and get page content

        Args:
                None

        Return:
                None
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
        return [item for item in urls if item.startswith('http')]

    def _filter_ok_responses(self, urls_and_statuses):
        """
        Go through a dictionary of urls and http statuses and
        filter out 200 responses
        """
        return {url: status_code for
                url, status_code in urls_and_statuses.items()
                if status_code is not 200}
