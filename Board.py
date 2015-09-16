# coding=utf-8
__author__ = 'PatrickYeh'

import Logger
import re
from WebRetriever import WebRetriever
from Page import Page
log = Logger.getLogger("PttBoard")

PAGE_REG = ".*index(?P<page_num>\d*).html"

class Board(Page):
    def __init__(self,board_id="joke"):
        self.base_url = 'https://www.ptt.cc/bbs/{board_id}/index{page_idx}.html'
        self.board_id = board_id
        self.html_raw_soup = self._fetch_data(self.url)


    def get_all_article_list(self,top=None,query_inverse=False):
        pass

    def get_total_page(self):
        pass

    def get_article_list_by_idx(self,page_idx,query_inverse=False):
        page_html_raw = WebRetriever().make_request(self.base_url.format(board_id=self.board_id,page_idx=page_idx))



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
        return page_num