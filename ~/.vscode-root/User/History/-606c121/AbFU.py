from elasticsearch import Elasticsearch
from confluent_kafka import Consumer, KafkaError

# from production import predict_single_url
import json
import re
conf = {
    'bootstrap.servers': 'kafka:9092',
    'group.id' : 'consumer',
    'auto.offset.reset': 'latest'
}

consumer = Consumer(conf)
topics = ['webserver-logs']
consumer.subscribe(topics)
# es = Elasticsearch(hosts='http://elasticsearch:9200')
# def process_data(message):
#     pattern = r'(?P<ip>[\d.]+) - - \[(?P<timestamp>[^\]]+)\] "(?P<request>[^"]+)" (?P<status>\d+) (?P<response_size>\d+) "(?P<referrer>[^"]+)" "(?P<user_agent>[^"]+)"'
#     log_entry = message['message']
#     match = re.match(pattern, log_entry)
    
#     if match:
#         type_attack = "none"
#         ip = match.group('ip')
#         request = match.group('request')
#         status = match.group('status')
#         response_size = match.group('response_size')
#         data_predict = request.split(' ')
#         if(len(data_predict) == 3):
#            type_attack = predict_single_url(data_predict[1])
#         data = {
#             "request": request,
#             "status": status,
#             "@timestamp": message['@timestamp'],
#             "type": message['event']['dataset'],
#             "response_size": response_size,
#             "ip": ip,
#             "attack" : type_attack
#         }
        
#         return data
#     else:
#         return None
    
# def push_es(message):
#     data = process_data(message)
#     if data != None:
#         res = es.index(index='apache-log',document=data)

def get_message():
    while True:
        try:
            msg = consumer.poll(1.0)  # Adjust the timeout as needed
            if msg is None or msg.error():
                continue
            message_json = json.loads(msg.value().decode('utf-8'))
            print(message_json)
            # push_es(message_json)
        except Exception as e:
            print(e)
        

get_message()



