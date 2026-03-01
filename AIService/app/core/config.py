from dotenv import load_dotenv
from groq import AsyncGroq
import os
load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
UPDATE_ALERTS_URL = "http://localhost:8002/change_rules"
UPDATE_COORDINATES_URL = "http://localhost:8002/change_coordinates"
GET_COORDINATES_URL = "http://localhost:8002/get_coordinates"
KAFKA_URL = "localhost:9092"
client = AsyncGroq(api_key=API_KEY)
