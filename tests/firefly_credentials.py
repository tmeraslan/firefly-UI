
import os

def get_firefly_credentials():
    BASE_URL = os.getenv("FIREFLY_URL", "http://localhost:8080/api/v1/accounts")
    TOKEN = os.getenv("FIREFLY_TOKEN", "")

    return {"token": TOKEN, "base_url": BASE_URL}