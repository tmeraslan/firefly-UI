
#tests/firefly_credentials.py
import os

def get_firefly_credentials():
    # UI base (עמוד ההתחברות), לא /api
    BASE_URL = os.getenv("FIREFLY_URL", "http://127.0.0.1:8082/")
    TOKEN = os.getenv("FIREFLY_TOKEN", "")
    return {"token": TOKEN, "base_url": BASE_URL}



    # def get_firefly_credentials():
    # BASE_URL = os.getenv("FIREFLY_URL", "http://localhost:8080/api/v1/accounts")
    # TOKEN = os.getenv("FIREFLY_TOKEN", "")

    # return {"token": TOKEN, "base_url": BASE_URL}