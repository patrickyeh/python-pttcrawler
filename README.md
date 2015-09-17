# python-pttcrawler

## Installation:
```shell
pip install pttcrawler
```
## Usage:
#To get board instance
```python
from pttcrawler.Board import Board
obj_joke_board = Board("joke")
print obj_joke_board.board_name
```
#To get top 10 pages article:
```python
from pttcrawler.Board import Board
for obj_article in pttcrawler.get_topN_page_article_list(10):
    print obj_article.article_id,obj_article.title,obj_article.content
    #get replay list
    print obj_article.reply
```
