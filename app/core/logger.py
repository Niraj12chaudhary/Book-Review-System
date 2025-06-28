# app/core/logger.py
import logging
from logging.handlers import RotatingFileHandler
import os

# Logs folder bana lo agar nahi hai toh
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

log_file_path = os.path.join(log_dir, "app.log")

# Logger Configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        RotatingFileHandler(log_file_path, maxBytes=5*1024*1024, backupCount=5),  # 5 MB max per file
        logging.StreamHandler()  
    ]
)

logger = logging.getLogger("book-review-service")
