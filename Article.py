# coding=utf-8
__author__ = 'PatrickYeh'
from Page import Page
from BeautifulSoup import BeautifulSoup
ARTICLE_BASE_URL = 'https://www.ptt.cc/bbs/{board_id}/{article_id}.html'

class Article(Page):
    def __init__(self,board_id="Gossiping",article_id="M.1442337186.A.9C1",lazy=False):
        self.article_id = article_id
        self.board_id = board_id
        self.dict_element = {}
        if not lazy:
            self._parse()

    def _parse(self):
        self.html_raw_soup = self._fetch_data(self.url)
        lst_top_element = self.html_raw_soup.findAll("span",attrs={"class":"article-meta-value"})

        self.dict_element['author'] = lst_top_element[0].string
        self.dict_element['title'] = lst_top_element[2].string
        self.dict_element['publish_time'] = lst_top_element[3].string

        #fetch article content
        lst_content = []
        for content in self.html_raw_soup.find("div",attrs={"id":"main-content"}).contents[4:]:
            stop_tag = BeautifulSoup(str(content)).find('span',attrs={'class':'f2'})
            if stop_tag :
                if u"※ 發信站:" in stop_tag.string:
                    #retrieve IPAddress
                    pass
            lst_content.append(str(content))
        self.dict_element['content'] = '\n'.join(lst_content)

    def test(self):
        lst_content = []
        for content in self.html_raw_soup.find("div",attrs={"id":"main-content"}).contents[4:]:
            stop_tag = BeautifulSoup(str(content)).find('span',attrs={'class':'f2'})
            if stop_tag :
                if u"※ 發信站:" in stop_tag.string:
                    #should get IP Address
                    break
            lst_content.append(str(content))
        print '\n'.join(lst_content)

    def get_element(self,element_id):
        if self.dict_element.has_key(element_id):
            return self.dict_element[element_id]
        else:
            return ""
    @property
    def url(self):
        return ARTICLE_BASE_URL.format(board_id=self.board_id,article_id=self.article_id)


    @property
    def title(self):
        return self.get_element('title')

    @property
    def publish_time(self):
        return self.get_element('publish_time')

    @property
    def author(self):
        return self.get_element('author')

    @property
    def content(self):
        return self.get_element('content')

