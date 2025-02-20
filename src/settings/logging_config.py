import os
import logging
from logging.handlers import RotatingFileHandler

LOG_FILE = "logs/app.log"
os.makedirs("logs", exist_ok=True)

file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3)
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

logger = logging.getLogger("fastapi_app")
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

# Console logging
# console_handler = logging.StreamHandler()
# console_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
# logger.addHandler(console_handler)

# Disable Uvicorn default loggers
# uvicorn_access_logger = logging.getLogger("uvicorn.access")
# uvicorn_error_logger = logging.getLogger("uvicorn.error")
# uvicorn_access_logger.handlers.clear()
# uvicorn_error_logger.handlers.clear()
