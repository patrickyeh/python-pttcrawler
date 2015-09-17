# coding=utf-8
__author__ = 'Vetom'

import requests
from BeautifulSoup import BeautifulSoup

from pttcrawler import Logger

log = Logger.getLogger("WebRetriever")

class WebRetriever():
    def make_request(self,str_url):
        log.debug("Make Query: {url}".format(url=str_url))
        html_raw = requests.get(str_url,verify=False,cookies={'over18':'1'})
        html_raw.encoding = 'utf-8'
        return BeautifulSoup(html_raw.text)


if __name__ == '__main__':
    data = WebRetriever().make_request('https://www.ptt.cc/bbs/joke/index.html')
    import re
    PAGE_REG = ".*index(?P<page_num>\d*).html"
    pattern = re.compile(PAGE_REG)

    page_num = data.find("div",attrs= {"class":"btn-group pull-right"}).findAll("a")[1]["href"]
    print pattern.match(page_num).group("page_num")
