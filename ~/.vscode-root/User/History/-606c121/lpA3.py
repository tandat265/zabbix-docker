from elasticsearch import Elasticsearch
from confluent_kafka import Consumer, KafkaError

# from production import predict_single_url
import json
import re
from telegram import Bot
import asyncio

import pickle
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing import sequence

class Detector:
    def __init__(self):
        self.tokenizer = pickle.load(open("./tokenizer/tokenizer.pickle", "rb"))
        self.model = load_model("./model/cnn_clf.h5")
        self.max_len = 600
        self.labels_type = ['SQLi', 'anomalous', 'normal', 'XSS', 'SSI', 'BufferOverflow', 'CRLFi', 'XPath', 'LDAPi', 'FormatString']

    def props_to_labels(self, props_matrix):
        labels = []
        for props_vector in props_matrix:
            idx = np.argmax(props_vector)
            label = self.labels_type[idx]
            labels.append(label)
        return labels

    def predict_url(self, url):
        # Convert the URL into a sequence of integers using the tokenizer
        seq = self.tokenizer.texts_to_sequences([url])
        X = sequence.pad_sequences(seq, maxlen=self.max_len)

        # Make a prediction
        Y_pred = self.model.predict(X)

        # Convert prediction probabilities to labels
        label_pred = self.props_to_labels(Y_pred)
        return label_pred[0]  # Return the first (and only) prediction

API_KEY = "7233719656:AAEOon4t_khOGhoDnrUbjWlXAGqP9xLY5sA"
ID = "6290139637"
def send_message(chat_id, text):
    bot = Bot(token=API_KEY)
    asyncio.run(bot.send_message(chat_id=chat_id, text=text))


conf = {
    'bootstrap.servers': 'kafka:9092',
    'group.id' : 'consumer',
    'auto.offset.reset': 'latest'
}

consumer = Consumer(conf)
topics = ['webserver-logs']
consumer.subscribe(topics)
es = Elasticsearch(hosts='http://zabbix-agent:9200')
def process_data(message):
    pattern = r'(?P<ip>[\d.]+) - - \[(?P<timestamp>[^\]]+)\] "(?P<request>[^"]+)" (?P<status>\d+) (?P<response_size>\d+) "(?P<referrer>[^"]+)" "(?P<user_agent>[^"]+)"'
    log_entry = message['message']
    match = re.match(pattern, log_entry)
    
    if match:
        type_attack = "none"
        ip = match.group('ip')
        request = match.group('request')
        status = match.group('status')
        response_size = match.group('response_size')
        data_predict = request.split(' ')
        detector = Detector()
        type_attack = detector.predict_url(request)
        if request == "GET / HTTP/1.1":
            type_attack = "normal"
        data = {
            "request": request,
            "status": status,
            "@timestamp": message['@timestamp'],
            "type": message['event']['dataset'],
            "response_size": response_size,
            "ip": ip,
            "attack" : type_attack
        }
        print(data)
        return data
    else:
        return None
    
def push_es(message):
    data = process_data(message)
    if data['attack'] != None and data['attack'] != 'normal':
        res = es.index(index='alert-log', document=data)   
        send_message(ID, message) 
    if data != None:
        res = es.index(index='nginx-log',document=data)

def get_message():
    while True:
        try:
            msg = consumer.poll(1.0)  # Adjust the timeout as needed
            if msg is None or msg.error():
                continue
            message_json = json.loads(msg.value().decode('utf-8'))
            print(message_json)
            push_es(message_json)
        except Exception as e:
            print(e)

# url_test = "GET /tienda1/publico/caracteristicas.jsp?id=d%27z%220"
# detector = Detector()
# t = detector.predict_url(url_test)
# print(t)


get_message()





