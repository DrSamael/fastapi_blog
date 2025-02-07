from elasticsearch import Elasticsearch

from src.settings.app import AppSettings

es = Elasticsearch([AppSettings().elasticsearch_url])


async def add_post_to_elasticsearch(post_data: dict):
    doc = {"title": post_data["title"], "content": post_data["content"]}
    es.index(index="fastapi_blog_posts", id=post_data["_id"], body=doc)


async def update_post_in_elasticsearch(post_id: str, title: str, content: str):
    doc = {"title": title, "content": content}
    # es.update(index="fastapi_blog_posts", id=post_id, body={"doc": doc})
    es.update(index="fastapi_blog_posts", id=post_id, body=doc)


async def delete_post_from_elasticsearch(post_id: str):
    es.delete(index="blog_posts", id=post_id, ignore=[404])
