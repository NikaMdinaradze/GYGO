from dotenv import load_dotenv
import os


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
USERNAME = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")

print(USERNAME, PASSWORD)