from pttcrawler.Board import Board

if __name__ == '__main__':
    obj_gossiping_board = Board(board_id="Gossiping")
    for obj_article in obj_gossiping_board.get_topN_page_article_list(10):
        print obj_article.article_id,obj_article.title