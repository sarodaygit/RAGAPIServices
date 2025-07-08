
from fastapi import APIRouter
from Utils.LoggerUtil import LoggerUtil
from bson import json_util
from Utils.JSONEncoder import JSONEncoder
from Stores.Mongo.motorstore import MotorConnection  # use actual path where MotorConnection class is
from Stores.Mongo.Models.MoviStats import Movie  # use actual path where Movie class is
from typing import List

class MovieStatsRouter:
    def __init__(self, prefix: str):
        self.logger = LoggerUtil()
        self.mongo_conn = MotorConnection()
        self.router = APIRouter(prefix=prefix)

        self.router.add_api_route("/count", self.get_movie_count, methods=["GET"], tags=["MovieStats"])
        self.router.add_api_route("/latest", self.get_latest_movie, methods=["GET"], tags=["MovieStats"], response_model=Movie)
        self.router.add_api_route("/highrated", self.get_high_rated_movies, methods=["GET"], tags=["MovieStats"], response_model=List[Movie])
        

    async def get_movie_count(self):
        try:
            collection = self.mongo_conn._db["movies"]
            count = await collection.count_documents({})
            return {"count": count}
        except Exception as e:
            self.logger.log_error(f"Error fetching movie count: {str(e)}")
            return {"error": "Failed to retrieve movie count"}

    async def get_latest_movie(self):
        try:
            collection = self.mongo_conn._db["movies"]
            document = await collection.find_one(sort=[("released", -1)])
            if document:
                return Movie(**document)
            return {"error": "No movie found"}
        except Exception as e:
            self.logger.log_error(f"Error fetching latest movie: {str(e)}")
            return {"error": "Failed to retrieve movie"}

    async def get_high_rated_movies(self):
        try:
            collection = self.mongo_conn._db["movies"]
            query = { "imdb.rating": { "$gt": 9.0 } }
            projection = { "_id": 1, "title": 1, "imdb": 1 }

            cursor = collection.find(query, projection)
            results = await cursor.to_list(length=None)
            return results
        except Exception as e:
            self.logger.log_error(f"Error fetching high-rated movies: {str(e)}")
            return {"error": "Failed to retrieve high-rated movies"}