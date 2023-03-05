import time

from warcio.archiveiterator import ArchiveIterator
import requests
import gzip
import re
from collections import Counter
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

covid_terms = 'covid|covid-19|corona|coronavirus|pandemic|epidemic|virus|mask'
economic_terms = 'economic|economical|unemployment|recession|poor|purchase|buy'

regex = re.compile(f"({covid_terms}).*({economic_terms})", re.IGNORECASE)

url = 'https://data.commoncrawl.org/crawl-data/CC-MAIN-2020-29/warc.paths.gz'
response = requests.get(url)

lines = gzip.decompress(response.content).decode('utf-8').split('\n')
urls = [line.strip() for line in lines if line.strip()]

total_counter = 0
matched_counter = 0
hits = 0

session = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
session.mount('http://', HTTPAdapter(max_retries=retries))
session.mount('https://', HTTPAdapter(max_retries=retries))

for url in urls:
    if url.endswith('.warc.gz'):
        final_url = 'https://data.commoncrawl.org/' + url

        stream = None
        if final_url.startswith("http://") or final_url.startswith("https://"):
            stream = session.get(final_url, stream=True).raw
        else:
            stream = open(final_url, "rb")

        for record in ArchiveIterator(stream):
            if record.rec_type == "warcinfo":
                continue

            if not ".com/" in record.rec_headers.get_header(
                    "WARC-Target-URI"
            ):
                continue

            total_counter += 1
            contents = (
                record.content_stream()
                .read()
                .decode("utf-8", "replace")
            )


            if regex.search(contents):
                url_pattern = re.compile(
                    r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

                matches = re.findall(url_pattern, contents)

                for match in matches:
                    if regex.search(match):
                        print(match)
                        break


        print(
            "Python: "
            + str(hits)
            + " matches in "
            + str(matched_counter)
            + "/"
            + str(total_counter)
        )
