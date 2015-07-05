import requests
import grequests
from lxml import html
from urllib import parse

# TODO: Detect redirect statuses


class Vamp(object):

    def __init__(self, url):
        self.url = url

    def scan_page(self, page=None):
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
        request_urls = []
        http_urls = self.sanitize_urls(urls)

        # Make relative urls absolute
        for url in http_urls:
            if url.startswith(r'/'):
                url = parse.urljoin(self.url, url)
                request_urls.append(url)
            else:
                request_urls.append(url)

        responses = self.perform_async_requests(request_urls)

        for response in responses:
            url_results[response.url] = response.status_code

        return url_results

    def perform_async_requests(self, urls):
        """Perform asynchronous get requests given multiple links

        Args:
            urls: An list of URLs
        Returns:
            An list of requests response objects
        """
        unsentRequests = ((grequests.get(resource) for resource in urls))
        # Size param specifies the number of requests to be made at a time
        return grequests.map(unsentRequests, size=10)

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
