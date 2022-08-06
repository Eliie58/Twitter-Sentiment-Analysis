import twint
from kafka import KafkaProducer
import json
import logging as logger
from datetime import datetime, timedelta
import time
from threading import Thread
import csv

logger.basicConfig(filename='/root/scripts/monitor.log', level=logger.INFO)
producer = None
interval_seconds = 60

def wait_for_broker():
    global producer
    while producer == None:
        try:
            producer = KafkaProducer(bootstrap_servers='broker:9092')
        except:
            logger.error('Broker not available yet.')
            time.sleep(10)
            producer = None


def write_trends_file(top_trends):
    with open('/root/scripts/trends.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['Subject','Topic'])
        for idx, subject in enumerate(top_trends):
            writer.writerow([subject,f'Trend_{idx+1}'])

def get_tweets_subject_date(subject, from_time, to_time, topic_name):
    logger.info(f'Retrieving tweets related to {subject} between {from_time} and {to_time}')
    c = twint.Config()
    c.Search = subject
    c.Since = from_time.strftime('%Y-%m-%d %H:%M:%S')
    c.Until = to_time.strftime('%Y-%m-%d %H:%M:%S')
    c.Pandas = True
    c.Hide_output = True

    tweets = run_search(c)
    if len(tweets) != 0:
        tweets['created_at'] = tweets['created_at'].map(int)
        tweets = tweets.drop_duplicates(subset=['created_at','tweet'], keep='first')
        tweets = tweets[tweets['language'] == 'en']
        tweets.reset_index(inplace=True)
        logger.info(f'Tweets found {tweets.shape}')
        tweets.apply(lambda row : write_row_to_kafka(row, topic_name), axis=1)
        twint.storage.panda.clean()

def run_search(c):
    try:
        twint.run.Search(c)
        return twint.storage.panda.Tweets_df.drop_duplicates(subset=['id'])
    except:
        logger.error('Failed running search')
        return []

def write_row_to_kafka(row, topic_name):
    # If not in english, don't send
    if row['language'] != 'en':
        return
    data = {
        "created_at" : row['created_at'],
        "tweet" : row['tweet']
    }
    try:
        logger.debug(f'Sending {json.dumps(data)} to topic {topic_name}')
        producer.send(topic_name, value=str.encode(json.dumps(data)))
    except BufferError:
        logger.warning('Buffer error, the queue must be full! Flushing...')
        producer.flush()
        logger.warning('Queue flushed, will write the message again')
        producer.send(topic_name, value=str.encode(json.dumps(data)))

def monitor(top_trends):
    wait_for_broker()
    write_trends_file(top_trends)
    to_time = datetime.today()
    from_time = to_time - timedelta(seconds=10)
    while True:
        for idx, subject in enumerate(top_trends):
            get_tweets_subject_date(subject, from_time, to_time, f'Trend_{idx+1}')
        second_difference = (datetime.now() - to_time).total_seconds()
        if second_difference < interval_seconds:
            time.sleep(interval_seconds - second_difference)
        from_time = to_time
        to_time = datetime.today()
