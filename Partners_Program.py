from bs4 import BeautifulSoup
from tldextract import extract
import csv
import re
import requests
import os

OUTPUT_FILE_NAME = "Output.csv"
POPULAR_SITES = ["slideshare", "facebook", "twitter", "youtube", "linkedin", "instagram", "google"]


def main():
    input_file = get_file_from_user()
    print('Processing: {}'.format(os.path.abspath(input_file)))
    extract_partners_links_from_csv_file(input_file)
    print('Output file: {}'.format(os.path.abspath(OUTPUT_FILE_NAME)))


def get_file_from_user():
    input_file = input('Enter input file name: ')

    while not input_file or not input_file.strip() or not os.path.isfile(input_file):
        print("Sorry we can't find the desirable file")
        input_file = input('Enter input file name : ')

    return input_file


def extract_partners_links_from_csv_file(input_file):
    """
    This function extract urls from the input csv file and check the response status of every link.
    the approved links transfer to extract_links_from_url for processing.
    """

    with open(input_file, newline="\n") as fin:
        reader = csv.DictReader(fin)

        with open(os.path.dirname(input_file) + '/' + OUTPUT_FILE_NAME, "w", newline="\n") as fout:
            fieldnames = ["--Home web--", "--Partners--"]
            writer = csv.DictWriter(fout, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                # adding prefix for this address
                full_url = "http://" + row["page"]

                try:
                    response = requests.get(full_url)
                except:
                    # denied urls
                    print('Request denied : {}'.format(full_url))
                    pass
                else:
                    # approved urls
                    if response.status_code == 200:
                        print('Request approved: {}'.format(full_url))
                        extract_links_from_url(response.text, full_url, writer)
                    else:
                        print('{}: {}'.format(response.status_code, full_url))


def extract_links_from_url(html_page, url, writer):
    """
    This function extract links that not appears in POPULAR_SITES and they are not internal.
    :param writer: Writer object of fout (output file)
    :param html_page: HTML version of the Web page (url)
    :param url: full address of 'Home web page'
    """
    urls_list = []  # list that contains the extracted urls from 'home web page'
    soup = BeautifulSoup(html_page, "lxml")
    home = extract(url)  # tldextract.extract

    # iteration over the current html page and extract urls
    for link in soup.findAll(
            "a",
            attrs={
                "href": re.compile(
                    r"(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9]["
                    r"a-zA-Z0-9-]+ "
                    r"[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.["
                    r"^\s]{2,})",
                    flags=re.IGNORECASE,
                )
            },
    ):
        href = link.get("href").strip()
        ext = extract(href)  # tldextract.extract

        # exclude links of Popular websites (facebook, youtube etc..)
        if ext.domain.lower() in POPULAR_SITES:
            continue

        # exclude duplicate urls and urls that contains 'home web page' domain and suffix
        if href not in urls_list and f"{home.domain}.{home.suffix}" != f"{ext.domain}.{ext.suffix}":
            writer.writerow(
                {
                    "--Home web--": url,
                    "--Partners--": " " + href,
                }
            )

        urls_list.append(href)


if __name__ == "__main__":
    main()
