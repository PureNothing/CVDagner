from dotenv import load_dotenv
import os
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GRAPHQL_URL = "http://localhost:8000/graphql"
SECRET_A = os.getenv("SECRET_A")