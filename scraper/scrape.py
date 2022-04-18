#!/usr/bin/env python

import os
import time
import urllib.request
from pathlib import Path
from typing import List, Optional

import requests
import rich
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError, ConnectTimeout
from url_lists import (BLACKLISTED, DOCX_TO_PDF, MANUAL_TO_PDF, REMAPPED_URLS,
                       SLOW_URLS, TIME_OUT_ERROR, TODO_LIST)
from util import _config_requests, is_local_download_link

URL = "https://www.kb.se/samverkan-och-utveckling/biblioteksutveckling/biblioteksplaner.html"
BASE_DIR = "biblioteksplaner"
PWD = f"{os.getcwd()}/{BASE_DIR}"

# Class names in url to parse
REGIONS_CLASS = "kb-ia-list__item"
LIBRARY_PLANS_PER_REGION = "sv-text-portlet-content"


def _has_library_plans(region_list: List[Optional[str]]) -> bool:
    """Checks if the region has any uploaded region plans.

    :param region_list: List of a region name and potentially libraries included in the region, if such documents have been made available
    """
    return len(region_list) > 1


def _clean_link_texts(url):
    SOUP_TO_REMOVE = " Länk till annan webbplats."
    return url.replace(SOUP_TO_REMOVE, "")


def get_region_name_with_libraries(region_soup):
    """Get the region name and all its libraries.

    :param region_soup: An HTML string containing the region name and potentially libraries for the region.
    """
    region_name, _region_libs = region_soup
    region_name = _clean_link_texts(region_name.text)

    libs = _region_libs.find_all("a", href=True)
    region_libs = [_clean_link_texts(lib.text) for lib in libs]
    urls = [lib["href"] for lib in libs]

    return (region_name, region_libs, urls)


def create_folder_for_region(region_name: str, idx: str) -> str:
    """Create folder with relative name for each region.

    :param region_name: Name for the folder
    :param idx: Integer with leading zeros (0X) if its the 1st to 9th folder
    """
    region_path = f"{PWD}/{idx}_{region_name}"
    Path(region_path).mkdir(parents=True, exist_ok=True)
    return region_path


def download_pdf(url: str, filename: str, sleep_time=0.1, retry_counter=0):
    """Download PDF from url.

    :param url: Link to the PDFs
    :param filename: Name for the saved PDF
    """
    if not os.path.isfile(filename):
        try:
            resp = requests.get(url, verify=False)
            with open(filename, "wb+") as f:
                f.write(resp.content)

            time.sleep(5)

        except (ConnectionError, ConnectionResetError) as e:
            if retry_counter < 5:
                download_pdf(
                    url,
                    filename,
                    sleep_time=(sleep_time * 5),
                    retry_counter=(retry_counter + 1),
                )
            else:
                raise e

    else:
        time.sleep(0.001)


def parse_urls():
    """Parse and download all PDFs from URLs."""

    html_text = requests.get(URL).text
    soup = BeautifulSoup(html_text, "html.parser")
    regions = soup.find_all("li", class_=REGIONS_CLASS)

    not_valid_municipalities = ["Gotland"]
    for i, region_soup in enumerate(regions):

        region_soup = region_soup.find(class_=LIBRARY_PLANS_PER_REGION).find_all("p")
        if not _has_library_plans(region_soup):
            continue

        region_name, region_libs, urls = get_region_name_with_libraries(region_soup)
        # Skip download PDF if region has no uploaded `biblioteksplaner`
        if region_libs is None:
            continue

        idx = f"{i+1}".zfill(2)
        region_path = create_folder_for_region(region_name, idx)

        # Find the PDFs to download from HTML soup of all `biblioteksplaner` in the region
        for municipality, url in zip(region_libs, urls):
            if is_local_download_link(url):
                url = f"https://www.kb.se{url}"

            if url in MANUAL_TO_PDF:
                url = None  # skip this for now
            elif url in DOCX_TO_PDF:
                url = None  # skip this for now (needs convert to pdf)
            elif url in REMAPPED_URLS:
                url = REMAPPED_URLS[url]
            elif url in BLACKLISTED:
                url = None
            elif url in TIME_OUT_ERROR:
                url = None
            elif url in SLOW_URLS:
                url = None
            elif url in TODO_LIST:
                url = None

            # Skip certain URLs and PDFs we couldn't find
            if url is None:
                not_valid_municipalities.append(municipality)
                continue

            # Download and save pdfs
            print("--> ", url)

            if municipality[-1] == ".":
                filename = f"{region_path}/{municipality}pdf"
            else:
                filename = f"{region_path}/{municipality}.pdf"

            download_pdf(url, filename)

    # Print all incorrect municipalities
    rich.print("\n=================================\nNot valid:\n")
    for m in not_valid_municipalities:
        rich.print(f"[red]--> {m}[/red]")


if __name__ == "__main__":
    print("Starting to parse URLs")
    Path(PWD).mkdir(parents=True, exist_ok=True)

    _config_requests()
    parse_urls()
