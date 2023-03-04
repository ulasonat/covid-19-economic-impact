import requests
import gzip
import re

url = "https://data.commoncrawl.org/crawl-data/CC-MAIN-2020-45/warc.paths.gz"
response = requests.get(url)
lines = gzip.decompress(response.content).decode('utf-8').split('\n')
urls = [line.strip() for line in lines if line.strip()]

for url in urls:
    if url.endswith('.warc.gz'):
        print(url)