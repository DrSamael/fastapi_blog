from elasticsearch import Elasticsearch

from src.settings.app import AppSettings

es = Elasticsearch([AppSettings().elasticsearch_url])


async def add_post_to_elasticsearch(post_data: dict) -> None:
    doc = await generate_mongo_data(post_data)
    es.index(index="fastapi_blog_posts", id=post_data["_id"], body=doc)


async def update_post_in_elasticsearch(post_id: str, post_data: dict) -> None:
    es.update(index="fastapi_blog_posts", id=post_id, body={"doc": post_data})


async def delete_post_from_elasticsearch(post_id: str) -> None:
    es.delete(index="fastapi_blog_posts", id=post_id, ignore=[404])


async def search_post_in_elasticsearch(search_body: dict) -> list:
    response = es.search(index="fastapi_blog_posts", body=search_body)
    results = [{**hit["_source"], "id": hit["_id"]} for hit in response["hits"]["hits"]]

    return results


async def generate_mongo_data(post_data):
    return {
        "id": str(post_data["_id"]),
        "title": post_data["title"],
        "content": post_data["content"],
        "published": post_data["published"],
        "user_id": str(post_data["user_id"])
    }
