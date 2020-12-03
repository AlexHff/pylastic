#!/usr/bin/python3

import csv
import requests
import argparse
import pprint

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
    '-g',
    dest='get',
    help='get all elements from an index',
    type=str2bool,
		nargs='?',
    const=True,
    default=False
  )
  parser.add_argument(
    '-d',
    dest='delete',
    help='delete an index',
    type=str2bool,
		nargs='?',
    const=True,
    default=False
  )
  parser.add_argument(
    '-e',
    dest='export',
    help='export an index',
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
  )
  parser.add_argument(
    '-f',
    '--file_name',
    dest='file_name',
    help='path to export local file',
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

def get_index(es, index_name):
  res = es.search(index=index_name, body = {
        'size' : 10000,
        'query': {
          'match_all' : {}
        }
      })
  return res

def delete_index(es, index_name):
  status = es.indices.delete(index=index_name, ignore=[400, 404])
  return status

def export_index(es, index_name, file_name):
	res = get_index(es, index_name)
	with open(file_name, 'w') as f:
		header_present  = False
		for doc in res['hits']['hits']:
			my_dict = doc['_source'] 
			if not header_present:
				w = csv.DictWriter(f, my_dict.keys())
				w.writeheader()
				header_present = True
			w.writerow(my_dict)

if __name__ == '__main__':
	parser = create_parser()
	args = parser.parse_args()
	es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
	if args.create == True:
		if not args.url:
			raise Exception("missing url")
		status = create_index(es, args.url, args.index_name)
		print(status)
	elif args.get == True:
		res = get_index(es, args.index_name)
		print("%d documents found" % res['hits']['total']['value'])
		for doc in res['hits']['hits']:
			pprint.pprint(doc['_source'])
	elif args.delete == True:
		status = delete_index(es, args.index_name)
		print(status)
	elif args.export == True:
		if not args.file_name:
			raise Exception("missing file name")
		export_index(es, args.index_name, args.file_name)
