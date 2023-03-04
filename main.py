from warcio.archiveiterator import ArchiveIterator
import requests
import gzip
import re


covid_terms = 'covid|covid-19|corona|coronavirus|pandemic|epidemic'
economic_terms = 'economic|economical|unemployment|recession'

regex = re.compile(f"({covid_terms}).*({economic_terms})", re.IGNORECASE)

url = 'https://data.commoncrawl.org/crawl-data/CC-MAIN-2020-45/warc.paths.gz'
response = requests.get(url)

lines = gzip.decompress(response.content).decode('utf-8').split('\n')
urls = [line.strip() for line in lines if line.strip()]

total_counter = 0
matched_counter = 0
hits = 0

for url in urls:
    if url.endswith('.warc.gz'):
        final_url = 'https://data.commoncrawl.org/' + url

        stream = None
        if final_url.startswith("http://") or final_url.startswith("https://"):
            stream = requests.get(final_url, stream=True).raw
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

            m = regex.search(contents)
            if m:
                matched_counter += 1
                hits += 1
                m = regex.search(contents, m.end())
                print(contents)

            while m:
                m = regex.search(contents, m.end())
                hits += 1

        print(
            "Python: "
            + str(hits)
            + " matches in "
            + str(matched_counter)
            + "/"
            + str(total_counter)
        )
