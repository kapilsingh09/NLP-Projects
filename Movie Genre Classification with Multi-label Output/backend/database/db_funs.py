from collections.abc import Mapping
from typing import Any

from bson import ObjectId
from pymongo.errors import PyMongoError

if __package__ and "." in __package__:
    from ..utils.logger import get_logger
else:
    from utils.logger import get_logger

from .db import collection

logger = get_logger(__name__)


def _respond(info: Any, message: str) -> dict[str, Any]:
    response = {
        "[INFO]": info,
        "[RESPONSE]": message,
    }
    logger.info("%s", message)
    return response


def _serialize_movie(movie: dict[str, Any]) -> dict[str, Any]:
    serialized = dict(movie)
    serialized["_id"] = str(serialized["_id"])
    return serialized


def _parse_movie_id(movie_id: str) -> ObjectId:
    if not ObjectId.is_valid(movie_id):
        raise ValueError(f"Invalid movie ID: {movie_id}")
    return ObjectId(movie_id)


def save_data(movie: Mapping[str, Any]) -> dict[str, Any]:
    try:
        result = collection.insert_one(movie)
    except PyMongoError:
        logger.exception("Failed to save movie prediction")
        raise
    logger.info("Inserted movie with ID: %s", result.inserted_id)
    return _respond(result.inserted_id, "Stored successfully!")


def get_all_data() -> dict[str, Any]:
    try:
        movies = [_serialize_movie(movie) for movie in collection.find().limit(5)]
    except PyMongoError:
        logger.exception("Failed to retrieve movie predictions")
        raise
    return _respond(movies, "Movies retrieved successfully!")


def get_data_by_id(movie_id: str) -> dict[str, Any]:
    try:
        movie = collection.find_one({"_id": _parse_movie_id(movie_id)})
    except PyMongoError:
        logger.exception("Failed to retrieve movie prediction")
        raise
    if movie is None:
        return _respond(None, "Movie not found.")
    return _respond(_serialize_movie(movie), "Movie retrieved successfully!")


def update_data(movie_id: str, updates: Mapping[str, Any]) -> dict[str, Any]:
    if not updates:
        raise ValueError("At least one field is required to update a movie")
    if "_id" in updates:
        raise ValueError("A movie ID cannot be updated")

    try:
        result = collection.update_one(
            {"_id": _parse_movie_id(movie_id)},
            {"$set": dict(updates)},
        )
    except PyMongoError:
        logger.exception("Failed to update movie prediction")
        raise
    info = {
        "matched_count": result.matched_count,
        "modified_count": result.modified_count,
    }
    message = "Movie updated successfully!" if result.matched_count else "Movie not found."
    return _respond(info, message)


def delete_data(movie_id: str) -> dict[str, Any]:
    try:
        result = collection.delete_one({"_id": _parse_movie_id(movie_id)})
    except PyMongoError:
        logger.exception("Failed to delete movie prediction")
        raise
    deleted = result.deleted_count == 1
    message = "Movie deleted successfully!" if deleted else "Movie not found."
    return _respond(deleted, message)