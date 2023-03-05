## Trust Lab Coding Assesment: Covid 19 Economic Impact
### **Goal:** Find pages on the common crawl archive that are relevant to COVID-19's economic impact.

**Used months:** March/April 2020, May/June 2020, July 2020, August 2020, September 2020, October 2020, November/December 2020

**Number of URLs produced:** 1000

**Dependencies:**
- `Python 3.6+`
- `requests`
- `gzip`
- `re`
- `collections`
- `bs4`
- `warcio`

### **Overview**

I would say the main challenge I encountered was the 6-hour-long time aspect. It took me more than an hour to actually figure out how to access the common crawl archive data and work with WARC files and then I had to switch my approach a couple of times after implementing the algorithm, therefore my code is not properly optimized while I expect it to produce a high percentage of matching URLs.

I tried to commit everytime I implemented a major aspect of the program (in *setup* branch, which is merged into *main*), therefore you can check my progress there as well.

### **How it works and what didn't work?**

After setting up the session for HTTP requests, I fetch a list of URLs using the CommonCrawl data for all months in 2020 after March. I then integrated the sample code you provided into my code, and I use regex to check the content of each HTML-data of the URLs. I have multiple words I came up with for both coronavirus and economy. In order for my program to detect the HTML document, it needs to detect at least one covid-related term and one economy-related term. It is important as our goal is to find the economy aspect of the covid. If it finds a document, it extracts all URLs from the content using a regular expression for URLs, and then checks each URL using the same regex to see if it matches the COVID and economic terms. This was not my original plan, I originally wanted to get the related URLs of the content it detects, but was unable to achieve this during the given time. With the way it is implemented, it also checks whether the URLs have the respective terms. I believe this would result in a less amount of matching documents, as it is a bit less effective way of checking (since I expect there are tons of pages where the content is related but the URL may not necessarily be). However, thanks to the large dataset, I was able to get 1,000 URLs.

### **Multiprocessing**
My original intention was to implement multiprocessing to go through the documents quicker, as it takes some time to actually fetch the 1000 URLs but was unable to  due to time constraint.

### **Assumptions I made**

I tried not to make any assumptions as described in the assesment document. One assumption I did after observing the results is the following line:
`if regex.search(match) and match.endswith('/') and match not in matched_urls:`
I realized that some of the produced results were not actually webpages but other sorts of documents like JPG files. Due to time-constraints, instead of trying to find & exclude all types of unwanted documents, I used `match.endswith('/')` because I observed that most unwanted file or webpage types don't have the '/' at the end like twitter pages or similar.

Due to time-constraint, I also was able to spend less time on README.md file than I wanted to. Therefore, feel free to reach me out if you have any questions regarding my implementation or approach!
