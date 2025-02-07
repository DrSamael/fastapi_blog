from src.search.elasticsearch import create_index


def register_tasks(app):
    app.add_event_handler("startup", handle_elasticsearch_index)


async def handle_elasticsearch_index():
    await create_index()
