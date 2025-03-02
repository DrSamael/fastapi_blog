from elasticsearch import Elasticsearch

from src.settings.app import AppSettings

es = Elasticsearch([AppSettings().elasticsearch_url])


async def create_index():
    index_name = AppSettings().elasticsearch_post_index

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
                "id": {
                    "type": "keyword"
                },
                "user_id": {
                    "type": "keyword"
                },
                "title": {
                    "type": "text",
                    "analyzer": "content_analyzer",
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
                },
                "published": {
                    "type": "boolean"
                }
            }
        }
    }

    exists = es.indices.exists(index=index_name)
    if not exists:
        es.indices.create(index=index_name, body=mapping)
        print(f"Index '{index_name}' created successfully.")
    else:
        print(f"Index '{index_name}' already exists.")
