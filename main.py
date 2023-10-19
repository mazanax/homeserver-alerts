from os import getenv
from time import time

from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException

load_dotenv()
app = FastAPI()
ACCESS_TOKEN = getenv("ACCESS_TOKEN")


@app.post("/heartbeat")
async def ping(token: str = Header(alias="authorization")):
    if token != ACCESS_TOKEN or ACCESS_TOKEN == "":
        raise HTTPException(detail="Not found", status_code=404)

    now = int(time())
    with open("heartbeat", "w") as file:
        file.write(f"{now}")

    return {"time": now}
