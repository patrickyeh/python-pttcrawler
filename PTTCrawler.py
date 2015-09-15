__author__ = 'PatrickYeh'

import WebRetriever
import Logger
import re
log = Logger.getLogger("PttBoard")

PAGE_REG = ".*index(?P<page_num>\d*).html"

class Board():
    def __init__(self,board_id="joke"):
        self.base_url = 'https://www.ptt.cc/bbs/{board_id}/index{idx}.html'
        self.board_id = board_id
        #fetchh page information
    def _fetch_board_data(self):
        self.html_raw_soup = WebRetriever().make_request(self.base_url.format(board_id=self.board_id,idx=""))

    def get_all_article_list(self,top=None,query_inverse=False):
        pass

    def get_total_page(self):
        pass

    def get_article_list_by_page(self,page_num,query_inverse=False):
        pass


    @property
    def board_name(self):
        return self.html_raw_soup.find("a",attrs= {"class":"board"}).contents[1]

    @property
    def url(self):
        pass

    @property
    def num_page(self):
        pass

if __name__ == '__main__':
    pass