"""
This file is used to configure the Elasticsearch client.
"""

import os

from elasticsearch import Elasticsearch

ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")


def get_elasticsearch_client():
    """
    This function is used to get the Elasticsearch client.
    """
    client = Elasticsearch(ELASTICSEARCH_URL)
    if not client.ping():
        raise Exception("Elasticsearch is not running")
    return client


elasticsearch_client = get_elasticsearch_client()
