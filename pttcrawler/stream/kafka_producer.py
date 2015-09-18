__author__ = 'PatrickYeh'

import receiver
import pickle
from pttcrawler import Logger
from kafka import SimpleProducer, KafkaClient

log = Logger.getLogger("kafka_producer")

class kafka_producer(receiver.receiver):
    def __init__(self):
        self.topic = "Message"

    def set_kafka_client(self,host,port):
        self.kafka_client = KafkaClient("{host}:{port}".format(host=host,port=port))
        self.producer = SimpleProducer(self.kafka_client)
    def set_topic(self,topic):
        self.topic = topic

    def send(self,obj_data):
        log.debug("Broadcast Data")

        self.producer.send_messages(self.topic,obj_data)

class article_producer(kafka_producer):
    def __init__(self):
        self.set_topic("ptt_article")

class reply_producer(kafka_producer):
    def __init__(self):
        self.set_topic("ptt_reply")
