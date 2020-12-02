#!/usr/bin/python3

import csv
import requests
import argparse

from elasticsearch import helpers, Elasticsearch

def str2bool(v):
	if isinstance(v, bool):
	 return v
	if v.lower() in ('yes', 'true', 't', 'y', '1'):
		return True
	elif v.lower() in ('no', 'false', 'f', 'n', '0'):
		return False
	else:
		raise argparse.ArgumentTypeError('Boolean value expected.')

def create_parser():
  parser = argparse.ArgumentParser(
    description='Download remote CSV file and import data to Elasticsearch.'
  )
  parser.add_argument(
    '-c',
    dest='create',
    help='create a new index',
    type=str2bool,
		nargs='?',
    const=True,
    default=False
  )
  parser.add_argument(
    '-u',
    '--url',
    dest='url',
    help='remote url of the CSV file',
    required=True
  )
  parser.add_argument(
    '-i',
    '--index_name',
    dest='index_name',
    help='name of the index',
    required=True
  )
  return parser

def create_index(es, url, index_name):
	if es.indices.exists(index_name):
		return True
	req = requests.get(url)
	if req.status_code != 200:
		return False
	content = req.content.decode('utf-8')
	reader = csv.DictReader(content.splitlines(), delimiter=',')
	helpers.bulk(es, reader, index=index_name)
	return True

if __name__ == '__main__':
	parser = create_parser()
	args = parser.parse_args()
	es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
	if args.create == True:
		status = create_index(es, args.url, args.index_name)
		print(status)
