"""
The program gets CSV file (Input) which contains a list of URLs and generates for each URL a new CSV file (Domain name) that
contains 'partners' web site.
"""
import sys
import csv
import os
from bs4 import BeautifulSoup
import requests
import requests.exceptions
from urllib.parse import urlsplit
from collections import deque
from tldextract import extract
import re
import time
import lxml

# list of popular sites
POPULAR_SITES = ['slideshare', 'facebook', 'twitter', 'youtube', 'linkedin', 'instagram', 'google']
# unwanted formats (will not be part of the URL)
EXCLUDE_FORMATS = ['#', '@', 'jpeg', 'pdf', 'txt', 'jpg', 'download', 'node']
# unwanted tags
EXCLUDE_TAGS = re.compile(
    r".*\/(photos|photo|javascript|photo-gallery|solution|legal|lang|privacy|careers|tel|solutions|learn|products"
    r"|gallery|pages|support|forms|login|faq|resources|text|jpeg|images|image|blog|news|media"
    r"|video|videos|press|pictures|latest-news|publications).*",
    re.IGNORECASE,
)


def get_response(url):
    """
    This function checks the status code of given URL
    :param url: the URL of a given website
    :return: the status code or None if the URL is broken
    """
    try:
        return requests.get(url)
    except:
        return None


def web_crawler(domain):
    """
    This function crawl the current website and classify each internal link to the correct list
    :param domain: the website to be crawl
    :return: list with all links that contains the word 'partners'
    """

    # set the time limit for this function (currently 120 second)
    time_limit = 120
    end_time = time.time() + time_limit
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

    # process URLs one by one until we exhaust the queue or until time runs out

    while len(new_urls) and time.time() < end_time:
        # move next URL from the queue to the set of processed URLs
        url = new_urls.popleft()
        processed_urls.add(url)
        response = get_response(url)
        # add broken URLs to irrelevant set, then continue
        if not response or response.status_code != 200:
            irrelevant_urls.add(url)
            continue

        # check if URL contains words or tags that should be exclude if so add it to irrelevant_list
        if EXCLUDE_TAGS.search(url) or any(ext in url for ext in EXCLUDE_FORMATS) or \
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

        for link in local_urls:

            if not link in new_urls and not link in processed_urls and not link in irrelevant_urls:
                # adds new URLs with affiliation to the word 'partners' to the start of the deque
                if 'partners' in url.lower() or 'partners' in link.lower():
                    new_urls.appendleft(link)
                else:
                    # adds other URLs to the end of new_urls deque
                    new_urls.append(link)

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

        response = get_response(url)
        if not response or response.status_code != 200:
            continue

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


def main(input_file):
    with open(input_file, newline="\n") as fin:
        reader = csv.DictReader(fin)

        for row in reader:
            print('--------------------------------------')
            domain = row["Website"]
            # fix url if needed (adds 'http' first etc..)
            if "https://" or "http://" in domain and "www." in domain:
                full_url = domain
            elif "https://" in domain and not "www." in domain:
                full_url = domain.replace("https://", "https://www.")
            elif "http://" in domain and not "www." in domain:
                full_url = domain.replace("http://", "http://www.")
            elif "https://" and "http://" not in domain and "www." in domain:
                full_url = f"https://{domain}"
            else:
                full_url = f"https://www.{domain}"

            home_domain = extract(full_url).domain

            with open(os.path.dirname(input_file) + '/' + home_domain + '.csv', "w", newline="\n") as fout:
                fieldnames = ["Organization Web Page", "Partners Web Page"]
                writer = csv.DictWriter(fout, fieldnames=fieldnames)
                writer.writeheader()

                urls_list = web_crawler(full_url)
                # if there are no URLs that contains the word 'partners'
                if not urls_list:
                    writer.writerow(
                        {
                            "Organization Web Page": full_url,
                            "Partners Web Page": "None"
                        }
                    )
                    continue

                # write 'partners' links to CSV
                for partner in partners_page_finder(urls_list):
                    writer.writerow(
                        {
                            "Organization Web Page": full_url,
                            "Partners Web Page": " " + partner
                        }
                    )
    print()
    print('Done')


if __name__ == '__main__':
    main(sys.argv[1])
