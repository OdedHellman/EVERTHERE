"""
    A program that crawls a website and  determine which page is the 'partners' page of
    this website
"""
import sys
from bs4 import BeautifulSoup
import requests
import requests.exceptions
from urllib.parse import urlsplit
from collections import deque
from tldextract import extract
import re
import time
import lxml


# set the time limit for this program (current 120 second)
TIME_LIMIT = 120
# list with popular sites
POPULAR_SITES = ['slideshare', 'facebook', 'twitter', 'youtube', 'linkedin', 'instagram', 'google']
# unwanted formats (this words shouldn't be part of any URL)
EXCLUDE_FORMATS = ['#', '@', 'jpeg', 'pdf', 'txt', 'jpg', 'download', 'node']
# unwanted tags
EXCLUDE_TAGS = re.compile(
    r".*\/(photos|photo|javascript|photo-gallery|solution|legal|lang|privacy|careers|tel|solutions|learn|products"
    r"|gallery|pages|support|forms|login|faq|resources|text|jpeg|images|image|blog|news|media"
    r"|video|videos|press|pictures|latest-news|publications).*",
    re.IGNORECASE,
)


def check_status_code(url):
    """
    This function checks the status code of given URL
    :param url: the URL of a given website
    :return: the status code or -1 if the URL is broken
    """
    try:
        response = requests.get(url)
        return response.status_code
    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.InvalidURL,
            requests.exceptions.InvalidSchema, requests.exceptions.TooManyRedirects):
        return -1


def web_crawler(domain):

    """
    This function crawl the current website and classify each internal link to the correct list
    :param domain: the website to be crawl
    :return: list with all links that contains the word 'partners'
    """

    # queue of URLs to be crawled
    new_urls = deque([domain])
    # set of URLs that we have already crawled
    processed_urls = set()
    # set of domains inside the home website
    local_urls = set()
    # set of unwanted URLs
    irrelevant_urls = set()
    # list of URLs contains the tag 'partners'
    partners_urls = []
    # srt the time limit for this function
    end_time = time.time() + TIME_LIMIT

    # process URLs one by one until we exhaust the queue or until time runs out
    while len(new_urls) and time.time() < end_time:

        # move next URL from the queue to the set of processed URLs
        url = new_urls.popleft()
        processed_urls.add(url)

        # add broken URLs to irrelevant set, then continue
        if not check_status_code(url) == 200:
            irrelevant_urls.add(url)
            continue

        # check if URL contains words or tags that should be exclude if so add it to irrelevant_list
        if EXCLUDE_TAGS.search(url) or any(ext in url for ext in EXCLUDE_FORMATS) or\
                extract(url).domain in POPULAR_SITES:
            irrelevant_urls.add(url)
            continue

        # check if the word 'partners' is part of given URL, if so adds it to the correct list
        if 'partners' in url.lower():
            print('**Found potential partners page at: {}'.format(url))
            # adds this URL to partners list
            partners_urls.append(url)

        else:
            print("Processing {}:".format(url))

        # extract base URL to resolve relative links
        parts = urlsplit(url)
        base = "{0.netloc}".format(parts)
        strip_base = base.replace("www.", "")
        base_url = "{0.scheme}://{0.netloc}".format(parts)
        path = url[:url.rfind('/') + 1] if '/' in parts.path else url

        response = requests.get(url)
        # create a beautiful soup for the html
        soup = BeautifulSoup(response.text, 'lxml')

        for link in soup.findAll("a"):
            # extract link URL from the anchor
            base = link.attrs["href"] if "href" in link.attrs else ''
            if base.startswith('/'):
                local_link = base_url + base
                local_urls.add(local_link)
            elif strip_base in base:
                local_urls.add(base)
            elif not base.startswith('http'):
                local_link = path + base
                local_urls.add(local_link)

        for i in local_urls:
            if not i in new_urls and not i in processed_urls and not i in irrelevant_urls:
                # adds new URLs with affiliation to the word 'partners' to the start of the deque
                if 'partners' in url.lower() or 'partners' in i.lower():
                    new_urls.appendleft(i)
                else:
                    # adds other URLs to the end of new_urls deque
                    new_urls.append(i)

        # reset the local_urls deque for the next iteration
        local_urls.clear()

    # return only the list that contain the URLs with the word 'partners'
    return partners_urls


def partners_page_finder(urls_list):
    """
    The function is iterates the URLs_list and looking for any external links
    from the given URLs - those are the 'partners' links
    :param urls_list: list of all URLs that contains the word 'partners'
    :return: List of partners
    """
    # set that contains the extracted URLs from 'urls_list'
    external_urls_set = set()

    for url in urls_list:

        if not check_status_code(url) == 200:
            continue

        response = requests.get(url)
        # create a beautiful soup for the html
        soup = BeautifulSoup(response.text, "lxml")
        # tldextract.extract
        home = extract(url)

        # iteration over the current html page and extract URLs
        for link in soup.findAll(
                "a",
                attrs={
                    "href": re.compile(
                        r"(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9]["
                        r"a-zA-Z0-9-]+ "
                        r"[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.["
                        r"a-zA-Z0-9]+\.[ "
                        r"^\s]{2,})",
                        flags=re.IGNORECASE,
                    )
                },
        ):

            href = link.get("href").strip()
            # tldextract.extract
            ext = extract(href)

            # exclude links of Popular websites (facebook, youtube etc..) and unwanted tags or formats
            if ext.domain.lower() in POPULAR_SITES or EXCLUDE_TAGS.search(href) or any(ext in href for ext in
                                                                                       EXCLUDE_FORMATS):
                continue

            # check if the current link is external link and adds it to set
            if href not in external_urls_set and f"{home.domain}" != f"{ext.domain}":
                if ext.subdomain:
                    external_urls_set.add(f"{ext.subdomain}.{ext.domain}.{ext.suffix}")
                else:
                    external_urls_set.add(f"{ext.domain}.{ext.suffix}")

    return external_urls_set


def main(domain):

    # fix url if needed (adds 'http' first etc..)
    if "https" in domain and "www." in domain:
        full_url = domain
    elif "https" in domain and not "www." in domain:
        full_url = domain[:8] + "www." + domain[8:]
    elif "https" not in domain and "www." in domain:
        full_url = "https://" + domain
    else:
        full_url = "https://www." + domain

    # broken and unavailable links
    if not check_status_code(full_url) == 200:
        print('Unavailable URL: {}'.format(full_url))
        exit(1)

    else:
        urls_list = web_crawler(full_url)

    # if there are no URLs that contains the word 'partners'
    if not urls_list:
        print()
        print("Sorry, can't find 'Partners' page or 'Partners' page doesn't exist: {}".format(full_url))
        return

    # Print a list of 'Partners' URLs
    print()
    print("---PARTNERS---")
    for partner in partners_page_finder(urls_list):
        print(partner)


if __name__ == '__main__':
    main(sys.argv[1])
