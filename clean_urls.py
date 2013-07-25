import re
import requests
from urlparse import urlparse
import yaml

c = yaml.safe_load(open('config.yml'))
def is_short_link(url):
    if url is not None:
        if c.has_key('short_url'):
            short_url = c['short_url']
        else:
            short_url = r".*bit\.ly.*"
        re_short_links = [
            re.compile(short_url),
            re.compile(r".*bit\.do.*"),
            re.compile(r".*t\.co.*"),
            re.compile(r".*go2\.do.*"),
            re.compile(r".*adf\.ly.*"),
            re.compile(r".*goo\.gl.*"),
            re.compile(r".*bitly\.com.*"),
            re.compile(r".*bit\.ly.*"),
            re.compile(r".*tinyurl\.com.*"),
            re.compile(r".*ow\.ly.*"),
            re.compile(r".*bit\.ly.*"),
            re.compile(r".*adcrun\.ch.*"),
            re.compile(r".*zpag\.es.*"),
            re.compile(r".*ity\.im.*"),
            re.compile(r".*q\.gs.*"),
            re.compile(r".*lnk\.co.*"),
            re.compile(r".*viralurl\.com.*"),
            re.compile(r".*is\.gd.*"),
            re.compile(r".*vur\.me.*"),
            re.compile(r".*bc\.vc.*"),
            re.compile(r".*yu2\.it.*"),
            re.compile(r".*twitthis\.com.*"),
            re.compile(r".*u\.to.*"),
            re.compile(r".*j\.mp.*"),
            re.compile(r".*bee4\.biz.*"),
            re.compile(r".*adflav\.com.*"),
            re.compile(r".*buzurl\.com.*"),
            re.compile(r".*xlinkz\.info.*"),
            re.compile(r".*cutt\.us.*"),
            re.compile(r".*u\.bb.*"),
            re.compile(r".*yourls\.org.*"),
            re.compile(r".*fun\.ly.*"),
            re.compile(r".*hit\.my.*"),
            re.compile(r".*nov\.io.*"),
            re.compile(r".*crisco\.com.*"),
            re.compile(r".*x\.co.*"),
            re.compile(r".*shortquik\.com.*"),
            re.compile(r".*prettylinkpro\.com.*"),
            re.compile(r".*viralurl\.biz.*"),
            re.compile(r".*longurl\.org.*"),
            re.compile(r".*tota2\.com.*"),
            re.compile(r".*adcraft\.co.*"),
            re.compile(r".*virl\.ws.*"),
            re.compile(r".*scrnch\.me.*"),
            re.compile(r".*filoops\.info.*"),
            re.compile(r".*linkto\.im.*"),
            re.compile(r".*vurl\.bz.*"),
            re.compile(r".*fzy\.co.*"),
            re.compile(r".*vzturl\.com.*"),
            re.compile(r".*picz\.us.*"),
            re.compile(r".*lemde\.fr.*"),
            re.compile(r".*golinks\.co.*"),
            re.compile(r".*xtu\.me.*"),
            re.compile(r".*qr\.net.*"),
            re.compile(r".*1url\.com.*"),
            re.compile(r".*tweez\.me.*"),
            re.compile(r".*sk\.gy.*"),
            re.compile(r".*gog\.li.*"),
            re.compile(r".*cektkp\.com.*"),
            re.compile(r".*v\.gd.*"),
            re.compile(r".*p6l\.org.*"),
            re.compile(r".*id\.tl.*"),
            re.compile(r".*dft\.ba.*"),
            re.compile(r".*aka\.gr.*")
        ]

        return any([r.search(url) for r in re_short_links])

def is_facebook(link):
    if re.search(".*facebook.*", link):
        return True
    else:
        return False

def extract_url(string):
    """
    get urls from input string
    """
    pattern = "(https?://[^\s]+)"
    return [unshorten_link(l) for l in re.findall(pattern, string)]

def unshorten_link(link):
  if is_short_link(link):
    try:
      r = requests.get(link)
    except:
      return link
    else:
      return r.url
  else:
    return link