# coding=utf-8
__author__ = 'PatrickYeh'

import re

from pttcrawler import Logger
from pttcrawler.WebRetriever import WebRetriever
from pttcrawler.Page import Page
from pttcrawler.Article import Article
from BeautifulSoup import BeautifulSoup
log = Logger.getLogger("PttBoard")

PAGE_REG = ".*index(?P<page_num>\d*).html"
ARTICLE_URL_REG = ".*/(?P<article_id>.*).html"
article_url_pattern = re.compile(ARTICLE_URL_REG)
class Board(Page):
    def __init__(self,board_id="Gossiping"):
        self.base_url = 'https://www.ptt.cc/bbs/{board_id}/index{page_idx}.html'
        self.board_id = board_id
        self.html_raw_soup = self._fetch_data(self.url)

    def _article_list_iter(self,lst_article_idx):
        for article_idx in lst_article_idx:
            yield Article(board_id=self.board_id,article_id=article_idx)

    def get_topN_page_article_list(self,n_page):
        lst_article_idx = self.get_article_id_list_by_range(start_page=self.num_page-n_page,end_page=self.num_page,desc=True)
        return self._article_list_iter(lst_article_idx)

    def get_article_id_list_by_range(self,start_page=1,end_page=10,desc=True):
        if start_page <= 0 or end_page > self.num_page:
            raise "Page number is out of range"
        lst_article_idx = []
        if desc:
            page_range = xrange(end_page,start_page-1,-1)
        else:
            page_range = xrange(start_page,end_page+1)
        for page_idx in page_range:
            lst_article_idx.extend(self.get_article_id_list_by_page(page_idx))

        return lst_article_idx

    def get_article_id_list_by_page(self,page_idx,desc=True):
        log.debug("Retrieve Page {page_idx} form {board_id}".format(page_idx=page_idx,board_id = self.board_id))
        page_html_raw = WebRetriever().make_request(self.base_url.format(board_id=self.board_id,page_idx=page_idx))
        lst_article_idx = []
        for article_elem in page_html_raw.findAll("div",attrs={'class':'title'}):
            if article_elem.find("a") == None:
                continue
            article_id_inst = article_url_pattern.match(article_elem.find("a")['href'])
            if article_id_inst:

                lst_article_idx.append(article_id_inst.group('article_id'))
            else:
                continue

        if desc:
            #reverse list
            return lst_article_idx
        else:
            return lst_article_idx[::-1]


    @property
    def board_name(self):
        log.debug("Fetch board name")
        return self.html_raw_soup.find("a",attrs= {"class":"board"}).contents[1]

    @property
    def url(self):
        return self.base_url.format(board_id=self.board_id,page_idx="")

    @property
    def num_page(self):
        log.debug("Fetch number of page")
        prefix_url = self.html_raw_soup.find("div",attrs= {"class":"btn-group pull-right"}).findAll("a")[1]["href"]
        pattern = re.compile(PAGE_REG)
        page_num = int(pattern.match(prefix_url).group("page_num"))
        return page_num + 1