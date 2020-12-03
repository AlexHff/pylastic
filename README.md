# pylastic

Simple python script to make CRUD operations on Elasticsearch.

## Getting Started

Install Elasticsearch with Docker

```bash
docker pull docker.elastic.co/elasticsearch/elasticsearch:7.10.0
```

Starting a multi-node cluster with Docker Compose

```bash
docker-compose up
```

## Usage

To create an index, use the following command:

```bash
./pylastic.py -c -u https://www1.ncdc.noaa.gov/pub/data/cdo/samples/PRECIP_HLY_sample_csv.csv -i my_index
```

To view an index, use the following command:

```bash
./pylastic.py -g -i my_index
```

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

