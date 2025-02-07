from elasticsearch import Elasticsearch

from src.settings.app import AppSettings

es = Elasticsearch([AppSettings().elasticsearch_url])


async def create_index():
    index_name = "fastapi_blog_posts"

    mapping = {
        "settings": {
            "analysis": {
                "analyzer": {
                    "content_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": ["lowercase", "english_stemmer", "synonym_filter"]
                    }
                },
                "filter": {
                    "synonym_filter": {
                        "type": "synonym",
                        "synonyms": [
                            "fastapi, web framework",
                            "python, programming language",
                            "writer, author",
                            "blog, journal, diary, article feed, publication",
                            "post, article, entry, story",
                            "comment, reply, feedback, response, discussion",
                            "guide, tutorial, handbook, walkthrough, how-to",
                            "tag, keyword, label, topic",
                            "search, find, lookup, discover, explore"
                        ]
                    },
                    "english_stemmer": {
                        "type": "stemmer",
                        "name": "english"
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "title": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "content": {
                    "type": "text",
                    "analyzer": "content_analyzer"
                }
            }
        }
    }

    exists = es.indices.exists(index=index_name)
    if not exists:
        es.indices.create(index=index_name, body=mapping)
        print(f"✅ Index '{index_name}' created successfully.")
    else:
        print(f"ℹ️ Index '{index_name}' already exists.")
