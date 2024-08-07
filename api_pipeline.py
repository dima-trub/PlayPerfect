from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from utils.db_connectors.Postgres.postgres_connector import PostgresConnector
from config import Config
import redis.asyncio as redis
import logging



# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()


class AttributeService:
    def __init__(self):
        # Create PostgresConnector instance with connection URL
        self.postgres_conn_str = Config.postgres_url
        self.postgres_connector = PostgresConnector(connection_url=self.postgres_conn_str)

        # Initialize Redis client
        self.redis = redis.from_url(Config.redis_url)

    async def get_attribute_from_postgres(self, player_id: str, attribute_name: str) -> str:
        try:
            logger.info(f"Querying PostgreSQL for player_id={player_id} and attribute_name={attribute_name}")
            query = f"""
                SELECT {attribute_name}
                FROM user_panel
                WHERE player_id = %s
            """
            result = await self.postgres_connector.select(query, (player_id,))
            logger.info(f"Query result: {result}")

            if result:
                attribute_value = str(result[0][0])  # Adjust based on your result format
                logger.info(f"Returning value from PostgreSQL: {attribute_value}")
                return attribute_value
            else:
                logger.warning(f"No results found for player_id={player_id} and attribute_name={attribute_name}")
                raise HTTPException(status_code=404, detail="Attribute not found")
        except HTTPException as e:
            logger.error(f"HTTP Exception: {e.detail}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error in get_attribute_from_postgres: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def get_attribute(self, player_id: str, attribute_name: str) -> str:
        cache_key = f"{player_id}:{attribute_name}"

        try:
            # Check Redis cache first
            cached_value = await self.redis.get(cache_key)
            if cached_value:
                logger.info(f"Cache hit for player_id={player_id} and attribute_name={attribute_name}")
                return cached_value

            logger.info(f"Cache miss for player_id={player_id} and attribute_name={attribute_name}")
            attribute_value = await self.get_attribute_from_postgres(player_id, attribute_name)

            # Cache the result with an expiration time (e.g., 60 seconds)
            await self.redis.set(cache_key, attribute_value, ex=60)
            return attribute_value
        except Exception as e:
            logger.error(f"Error in get_attribute method: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")


# Dependency injection
def get_attribute_service():
    return AttributeService()


@app.get("/")
async def read_root():
    return {"message": "Welcome to the Attribute Service API"}


class AttributeRequest(BaseModel):
    player_id: str
    attribute_name: str


@app.post("/GetAttribute")
async def get_attribute(request: AttributeRequest, service: AttributeService = Depends(get_attribute_service)):
    logger.info(f"Received request for player_id={request.player_id} and attribute_name={request.attribute_name}")
    try:
        attribute_value = await service.get_attribute(request.player_id, request.attribute_name)
        return {request.attribute_name: attribute_value}
    except HTTPException as e:
        logger.error(f"HTTP Error occurred: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected Error occurred: {e}")
        raise HTTPException(status_code=500, detail="Unexpected error occurred")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)




