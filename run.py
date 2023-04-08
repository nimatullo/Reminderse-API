import uvicorn
from main import app

PORT = 8000
HOST = "0.0.0.0"


if __name__ == "__main__":
    uvicorn.run(app, host=HOST)
