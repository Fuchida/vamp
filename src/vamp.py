from urllib.parse import urljoin
import logging

import requests
from lxml import html

# TODO: Detect redirect statuses


class Vamp(object):

    def __init__(self, url, log_level='INFO'):
        """
        Args:
                string: url of the main site
                string: log_level of how much information you need (INFO, DEBUG etc)
        """
        self.url = url
        self.logger = logging.getLogger('Vamp')
        if log_level:
            logging.basicConfig()
            self.level = logging.getLevelName(log_level)
            self.logger.setLevel(self.level)

    def scan(self, page=None):
        """
        Given the configured url return dead links

        Args:
                String: A specific page on the site

        Return:
                Dictionary: Containing key value links and status
        """

        if page is None:
            response = requests.get(self.url)
        else:
            response = requests.get(page)

        page_urls = self.get_page_urls(response.text)
        urls_and_statuses = self.check_url_status(page_urls)
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

    def check_url_status(self, urls):
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

        # Make relative urls absolute
        for item in http_urls:
            if item.startswith(r'/'):
                item = urljoin(self.url, item)

            self.logger.debug('Checking URL %s', item)
            url_response = requests.head(item)
            url_results[item] = url_response.status_code

        return url_results

    @classmethod
    def sanitize_urls(self, urls):
        """
        Takes a list of urls and removes all items that do not start
        with 'http' or are not relative links

        Args:
                urls: A list of urls

        Returns:
                A list of urls
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
