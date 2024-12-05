"""
This file is used to define the Elasticsearch indexes.
"""

from config.elasticsearch import elasticsearch_client


def create_index(index_name: str = "events"):
    """
    This function is used to create an index in Elasticsearch.
    Args:
        index_name (str, optional): The name of the index to create. Defaults to "events".
    """
    index_body = {
        "mappings": {
            "properties": {
                "name": {"type": "text"},
                "description": {"type": "text"},
                "category": {"type": "text"},
                "start_time": {"type": "date"},
                "end_time": {"type": "date"},
                "location": {"type": "text"},
            }
        }
    }

    if not elasticsearch_client.indices.exists(index=index_name):
        elasticsearch_client.indices.create(index=index_name, body=index_body)


def index_event(event: dict, index_name: str = "events"):
    """
    This function is used to index an event in Elasticsearch.
    Args:
        event (dict): The event to index.
        index_name (str, optional): The name of the index to use. Defaults to "events".
    """
    elasticsearch_client.index(index=index_name, body=event)


def search_events(query: str, filters: dict, limit: int, offset: int):
    """
    This function is used to search for events in Elasticsearch.
    Args:
        query (str): The query to search for.
        filters (dict): The filters to apply to the search.
        limit (int): The maximum number of events to return.
        offset (int): The offset to use for pagination.
    """
    search_body = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"name": query}},
                ],
                "filter": [],
            }
        },
        "from": offset,
        "size": limit,
    }

    if filters.get("category"):
        search_body["query"]["bool"]["filter"].append(
            {"term": {"category": filters["category"]}}
        )
    if filters.get("location"):
        search_body["query"]["bool"]["filter"].append(
            {"term": {"location": filters["location"]}}
        )

    response = elasticsearch_client.search(index="events", body=search_body)
    results = {
        "total": response["hits"]["total"]["value"],
        "data": [hit["_source"] for hit in response["hits"]["hits"]],
    }

    return results
