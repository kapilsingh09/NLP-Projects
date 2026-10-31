from pymongo import MongoClient
from pymongo.errors import PyMongoError

if __package__ and "." in __package__:
    from ..utils.logger import get_logger
else:
    from utils.logger import get_logger

logger = get_logger(__name__)

try:
    client = MongoClient(
        "mongodb://localhost:27017/",
        serverSelectionTimeoutMS=5000
    )

    # Verify MongoDB connection
    client.admin.command("ping")

    db = client["movie_genre_db"]
    collection = db["movies"]

except PyMongoError:
    logger.exception("MongoDB connection failed")
    raise