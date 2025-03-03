import argparse
import requests
import json
import sys
import os
import shutil
from pprint import pprint
import csv


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', required=False, type=str, default='127.0.0.1:5000', help='Server url.')
    parser.add_argument('-n', required=True, type=int, choices=[1, 2], help='Number of stocks to be samples.')
    parser.add_argument('-o', required=False, type=str, default='outputs', help='Folder where to output predictions csv.')
    return parser.parse_args()


def print_error_and_exit(r):
    try:
        error_message = json.loads(r.text)['error']
    except Exception as e:
        error_message = "Unknown error"  # str(e)
    print(error_message, file=sys.stderr)
    exit(-1)


def load(url, n):
    load_r = requests.post('http://{url}/api/load'.format(url=url), json={'n': n})
    if load_r.status_code != 200:
        print_error_and_exit(load_r)
    return json.loads(load_r.text)


def predict(url, db):
    prediction_r = requests.post('http://{url}/api/predict'.format(url=url), json=db)
    if prediction_r.status_code != 200:
        print_error_and_exit(prediction_r)
    return json.loads(prediction_r.text)


def dump_prediction(root_path, prediction):
    for exchange_name, stocks in prediction.items():
        exchange_path = os.path.join(root_path, exchange_name)
        os.makedirs(exchange_path, exist_ok=True)
        for stock in stocks:
            stock_path = os.path.join(exchange_path, stock['name'] + '.csv')
            with open(stock_path, 'w', newline='\n') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=',')
                for pred_row in stock['prediction']:
                    spamwriter.writerow(pred_row)


if __name__ == '__main__':
    args = parse_args()

    db = load(args.u, args.n)
    prediction = predict(args.u, db)
    dump_prediction(args.o, prediction)
