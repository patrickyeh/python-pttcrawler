# coding=utf-8
__author__ = 'PatrickYeh'

from WebRetriever import WebRetriever

class Page():
    def _fetch_data(self,str_url):
        return WebRetriever().make_request(str_url)

    @property
    def url(self):
        raise "Need implementation"
