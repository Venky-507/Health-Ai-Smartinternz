# test_env.py (create this file temporarily)
from dotenv import load_dotenv
import os

load_dotenv()

print("API Key:", os.getenv('WATSONX_API_KEY'))
print("Project ID:", os.getenv('WATSONX_PROJECT_ID'))
print("URL:", os.getenv('WATSONX_URL'))
