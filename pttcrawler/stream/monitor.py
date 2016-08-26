__author__ = 'PatrickYeh'
import threading,time,pickle,json
from pttcrawler import Logger
from pttcrawler.Board import Board
from pttcrawler.Article import Article
import kafka_producer
log = Logger.getLogger("Monitor")

class monitor(threading.Thread):
    def __init__(self):
        self.dict_receiver = {}

    def set_receiver(self,name,obj_receiver):
        self.dict_receiver[name] = obj_receiver

    def get_receiver(self,name):
        return self.dict_receiver[name]


    def send(self,name,obj_data):
        self.dict_receiver[name].send(obj_data)

    def broadcast(self,obj_data):
        for key in self.dict_receiver.keys():
            self.dict_receiver[key].send(obj_data)


class article_monitor(monitor):
    def __init__(self,board_id,article_id):
        threading.Thread.__init__(self)
        monitor.__init__(self)
        self.article_id = article_id
        self.board_id = board_id
        self.obj_article = Article(board_id=board_id,article_id=article_id)


    def send_article_info(self):
        log.debug("Broadcast Article")
        dict_data = {}
        dict_data['board_id'] = self.board_id
        dict_data['article_id'] = self.article_id
        dict_data['author'] = self.obj_article.author
        dict_data['publish_time'] = self.obj_article.publish_time
        dict_data['content'] = self.obj_article.content
        # print dict_data

        self.send("ptt_article",json.dumps(dict_data))

    def run(self):
        self.send_article_info()
        int_pre_reply_length = 0
        while True:
            self.obj_article.refresh()
            int_cur_reply_length = len(self.obj_article.reply_list)
            if int_cur_reply_length > int_pre_reply_length:
                log.info("Get {count} new reply".format(count=(int_cur_reply_length - int_pre_reply_length)))
                for reply in self.obj_article.reply_list[int_pre_reply_length:int_cur_reply_length-1]:
                    reply['article_id'] = self.article_id
                    reply['board_id'] = self.board_id
                    self.send("ptt_reply",json.dumps(reply))

            int_pre_reply_length = int_cur_reply_length

            time.sleep(10)


class board_monitor(monitor):
    def __init__(self,board_id):
        threading.Thread.__init__(self)
        monitor.__init__(self)
        self.board_id = board_id
        self.top_n_page = 2

    def set_top_n_page(self,top_n_page):
        self.top_n_page = top_n_page

    def set_reply_receiver(self,obj_receiver):
        self.obj_reply_receiver = obj_receiver



    def run(self):
        dict_monitoring_thread = {}
        lst_pre_article_list = []
        objBoard = Board(board_id=self.board_id)

        while True:
            lst_cur_article_list = objBoard.get_topN_page_article_idx_list(self.top_n_page)
            lst_new_article_list = list(set(lst_cur_article_list)-set(lst_pre_article_list))
            lst_remove_article_list = list(set(lst_pre_article_list) - set(lst_cur_article_list))
            lst_pre_article_list = lst_cur_article_list
            #create article monitor and send board data to receiver
            for article_id in lst_new_article_list:
                log.info("Start to monitor New article_id {article_id}".format(article_id=article_id))
                obj_new_article =  article_monitor(board_id=self.board_id,article_id=article_id)
                obj_new_article.set_receiver("ptt_article",self.get_receiver("ptt_article"))
                obj_new_article.set_receiver("ptt_reply",self.obj_reply_receiver)
                obj_new_article.start()
                dict_monitoring_thread[article_id] = obj_new_article
            log.info("Wait for 2 second")
            time.sleep(2)

if __name__ == '__main__':
    obj_article_receiver = kafka_producer.article_producer()
    obj_article_receiver.set_kafka_client("spark","6667")
    obj_reply_receiver = kafka_producer.reply_producer()
    obj_reply_receiver.set_kafka_client("spark","6667")
    obj_board_monitor = board_monitor('Gossiping')
    obj_board_monitor.set_receiver("ptt_article",obj_article_receiver)
    obj_board_monitor.set_reply_receiver(obj_reply_receiver)
    obj_board_monitor.start()
