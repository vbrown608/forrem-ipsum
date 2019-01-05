import http.cookiejar
import urllib.request

from lxml.cssselect import CSSSelector
from lxml.html import fromstring

ARTICLES_INDEX_URL="https://www.forrester.com/search?sort=3&N=10001"

# Create opener with cookies
cj = http.cookiejar.MozillaCookieJar("cookies.txt")
cj.load()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

index_html = opener.open(ARTICLES_INDEX_URL).read()
soup = fromstring(index_html)

article_urls = []
sel = CSSSelector("a.title")
for article_link in sel(soup):
    article_urls.append(article_link.get('href'))

# titles_file = open('titles.txt', 'w')
body_file = open('body.txt', 'w')

for url in article_urls:
    html = opener.open("https://www.forrester.com" + url).read()
    soup = fromstring(html)
    sel = CSSSelector("section > p")
    for txt in sel(soup):
        body_file.write(txt.text or "")
    break

# titles_file.close()
body_file.close()


