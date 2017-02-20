from urllib.parse import urljoin, urlparse
import logging
import sys

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# TODO: Detect redirect statuses


class Vamp(object):

    def __init__(self, url, log_level='INFO'):
        """
        Args:
                string: url of the main site
                string: log_level of how much information you need (INFO, DEBUG etc)
        """
        self.site_url = url
        self.site_domain = urlparse(self.site_url).hostname

        self.internal_links = []
        self.external_links = []
        self.checked_links = []
        self.dead_links = []

        self.logger = logging.getLogger('Vamp')
        if log_level:
            logging.basicConfig()
            self.level = logging.getLevelName(log_level)
            self.logger.setLevel(self.level)

    def scan(self):
        self.crawl()
        return (self.dead_links)

    def crawl(self, page=None):
        """
        Given the configured url return dead links

        Args:
                String: A specific page on the site

        Return:
                Dictionary: Containing key value links and status
        """

        if page is None:
            page = self.site_url

        if self.site_domain in page and page not in self.internal_links:
            self.internal_links.append(page)

            self.logger.debug('[ Requesting ] page %s', page)
            response = requests.get(page, verify=False)
            from time import sleep
            sleep(0.5)

            self.logger.debug('[ Gathering ] links from %s', response.url)
            page_urls = self.get_page_urls(response.text)

            clean_urls = self.sanitize_urls(page_urls)
            urls_and_statuses = self.check_url_status(clean_urls)
            dead_links = self._filter_ok_responses(urls_and_statuses)

            for link, status in dead_links.items():
                self.dead_links.append({link: status})

            if clean_urls:
                for url in clean_urls:
                    self.crawl(url)
            else:
                return None

        elif self.site_domain not in page and page not in self.external_links:
            self.external_links.append(page)

            clean_urls = self.sanitize_urls([page])
            urls_and_statuses = self.check_url_status(clean_urls)
            dead_links = self._filter_ok_responses(urls_and_statuses)

            for link, status in dead_links.items():
                self.dead_links.append({link: status})

        else:
            return None

    def get_page_urls(self, html_page):
        """
        Given an HTML page, return a dictionary with all the URL
        found on the page

        Args:
            html_page: A string with HTML formated content

        Returns:
            A list with HTML links or and empty dictionary
        """
        soup = BeautifulSoup(html_page, 'html.parser')
        links = [link.get('href') for link in soup.find_all('a')]
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

        for item in urls:
            if item not in self.checked_links:
                self.checked_links.append(item)

                url_response = requests.head(item)
                from time import sleep
                sleep(0.5)

                url_results[item] = url_response.status_code
                self.logger.debug('[ %d ] %s', url_response.status_code, item)

        return url_results

    def sanitize_urls(self, urls):
        """
        Takes a list of urls and removes all items that do not start
        with 'http' or are not relative links or have localhost in the hostname.

        Will also make relative links absolite

        Args:
                urls: A list of urls

        Returns:
                A list of urls
        """

        absolute_and_relative = [item for item in urls if item.startswith('http') or item.startswith(r'/')]
        clean_links = []

        # Make relative urls absolute
        for item in absolute_and_relative:
            if item.startswith(r'/'):
                item = urljoin(self.site_url, item)
                clean_links.append(item)

            else:
                clean_links.append(item)

        clean_links = [link for link in clean_links if 'localhost' not in urlparse(item).hostname]
        return clean_links

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


if __name__ == '__main__':
    crawl = Vamp(sys.argv[1], 'DEBUG')
    crawl.scan()
