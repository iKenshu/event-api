"""
This file is used to configure the Elasticsearch client.
"""

from elasticsearch import Elasticsearch


def get_elasticsearch_client():
    """
    This function is used to get the Elasticsearch client.
    """
    client = Elasticsearch("http://elasticsearch:9200")
    if not client.ping():
        raise Exception("Elasticsearch is not running")
    return client


elasticsearch_client = get_elasticsearch_client()
