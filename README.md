# pylastic

Simple python CLI to make CRUD operations on Elasticsearch.

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

### Create an index

```bash
./pylastic.py -c -u https://www1.ncdc.noaa.gov/pub/data/cdo/samples/PRECIP_HLY_sample_csv.csv -i my_index
```

### Get an index

```bash
./pylastic.py -g -i my_index
```

### Delete an index

```bash
./pylastic.py -d -i my_index
```

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

