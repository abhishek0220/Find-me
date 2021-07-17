import os
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from datetime import datetime
import pytz

app = FastAPI(
    title="Find ME",
    description="Backend APIs for find me Android app",
    version="1.0.0"
)

IST = pytz.timezone('Asia/Kolkata')
started_at = datetime.now(IST)


app.add_middleware(DBSessionMiddleware, db_url=os.environ["COCKROACHDB"])


@app.get('/')
async def root():
    return {"status": "OK", "time_up": started_at}