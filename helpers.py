from urllib.parse import urlparse
def is_url(url):
    return urlparse(url).scheme != ""
