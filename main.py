# Author: Kyle Rosenstein
# Developed on 01/20/2022
# General website connection

import urllib
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
import logging
import json
import sys

# define the tags that you want to pull -- optional if you are searching for one

def main(html_url):
    try:
        req = urllib.request.Request(html_url)
        response = urllib.request.urlopen(req)
        result = response.read()
    except urllib.error.URLError:
        logging.error("This URL cannot be found or accessed")
    except urllib.error.HTTPError:
        logging.error("This returned broken code or has authentication errors")

    # check resulting html code
    logging.info(f"HTML code: {result}")

    # begin scraping html code
    soup = BeautifulSoup(result, 'html.parser')
    title = soup.find("title").get_text()
    
    headers = {"h1": [], "h2": [], "h3": [], "h4": [], "h5": [], "h6": []}
    tables = {"table": [], "th": [], "td": [], "tr": [], "thead": [], "tfoot": []}
    lists = {"ul": [], "li": [], "dl": [], "dt": [], "dd": []}
    links = {"a": []}
    paragraphs = {"p": []}
    tag_types = [headers, tables, lists, links, paragraphs]

    for tag_type in tag_types:
        for tag in tag_type.keys():
            for item in soup.findAll(tag):
                tag_type[tag].append(item.text)

                
    html_json = json.dumps(tag_types, indent = 2)
    print(f"{title}: {html_json}")

if __name__ == "__main__":
    main(sys.argv[1])
    