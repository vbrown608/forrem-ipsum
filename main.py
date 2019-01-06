import http.cookiejar
import urllib.request

import time

from lxml.cssselect import CSSSelector
from lxml.html import fromstring

ARTICLES_INDEX_URL="https://www.forrester.com/search?sort=3&N=10001"

# Create opener with cookies
cj = http.cookiejar.MozillaCookieJar("cookies.txt")
cj.load()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

index_html = opener.open(ARTICLES_INDEX_URL).read()
page = fromstring(index_html)

# Get a list of articles to visit
article_urls = []
for article_link in page.cssselect("a.title"):
    article_urls.append(article_link.get('href'))

class Style:
    def __init__(self, name, selector, newline=False):
        self.name = name
        self.selector = selector
        self.separator = "\n" if newline else ""
        self.f = open(Path("corpus/" + name + ".txt"), "w")

    def select_from_page(self, page):
        for el in page.cssselect(self.selector):
            if el.text:
                self.f.write(el.text + self.separator)

styles = [
    Style("title", ".main-wrapper h1", True),
    Style("subtitle", "h1 + h2"),
    # Style("section_header", "#key-takeaway p"),
    Style("section", "section > p"),
    Style("key_takeaway_title", "#key-takeaway h3", True),
    Style("key_takeaway_body", "#key-takeaway p"),
    # Style("bullet_bold", "#key-takeaway p", True),
    # Style("bullet_body", "#key-takeaway p"),
]

for url in article_urls:
    html = opener.open("https://www.forrester.com" + url).read()
    page = fromstring(html)
    for style in styles:
        style.select_from_page(page)
    time.sleep(5)

# Close files
for style in styles:
    style.f.close()

