# python-pttcrawler

## Installation
```shell
pip install pttcrawler
```
## Usage
#####Get board instance:
```python
from pttcrawler.Board import Board
obj_joke_board = Board("joke")
print obj_joke_board.board_name
```
##### Get articles from top 10 pages:
```python
from pttcrawler.Board import Board
obj_joke_board = Board("joke")
for obj_article in obj_joke_board.get_articles(obj_joke_board.get_topN_page_article_idx_list(10)):
    print obj_article.article_id,obj_article.title,obj_article.content
    #get replay list
    print obj_article.reply
```
##### Stream to Kafka broker:
```python

from pttcrawler.Board import Board
from pttcrawler.Article import Article
import kafka_producer

obj_article_receiver = kafka_producer.article_producer()
obj_article_receiver.set_kafka_client("192.168.68.128","6667")
obj_reply_receiver = kafka_producer.reply_producer()
obj_reply_receiver.set_kafka_client("192.168.68.128","6667")
obj_board_monitor = board_monitor('Gossiping')
obj_board_monitor.add_receiver(obj_article_receiver)
obj_board_monitor.set_reply_receiver(obj_reply_receiver)
obj_board_monitor.start()
```
