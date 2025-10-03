
#tests/firefly_credentials.py
import os

def get_firefly_credentials():
    BASE_URL = os.getenv("FIREFLY_URL", "http://54.77.26.161:8082/")
    TOKEN = os.getenv("FIREFLY_TOKEN", "")
    return {"token": TOKEN, "base_url": BASE_URL}





    #http://127.0.0.1