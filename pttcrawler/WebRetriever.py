# coding=utf-8
__author__ = 'Vetom'

import requests,time
from BeautifulSoup import BeautifulSoup
from pttcrawler import Logger

requests.packages.urllib3.disable_warnings()
log = Logger.getLogger("WebRetriever")

class WebRetriever():
    def make_request(self,str_url):
        log.debug("Make Query: {url}".format(url=str_url))
        bool_pass = False
        while not bool_pass:
            try:
                html_raw = requests.get(str_url,verify=False,cookies={'over18':'1'})
                html_raw.encoding = 'utf-8'
                bool_pass = True
            except:
                time.sleep(2)

        return BeautifulSoup(html_raw.text)


if __name__ == '__main__':
    data = WebRetriever().make_request('https://www.ptt.cc/bbs/joke/index.html')
    import re
    PAGE_REG = ".*index(?P<page_num>\d*).html"
    pattern = re.compile(PAGE_REG)

    page_num = data.find("div",attrs= {"class":"btn-group pull-right"}).findAll("a")[1]["href"]
    print pattern.match(page_num).group("page_num")
