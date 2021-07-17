import os
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from datetime import datetime
from FindMe.APIs.user import router as user_router
import pytz

app = FastAPI(
    title="Find ME",
    description="Backend APIs for find me Android app",
    version="1.0.0"
)

IST = pytz.timezone('Asia/Kolkata')
started_at = datetime.now(IST)


app.add_middleware(DBSessionMiddleware, db_url=os.environ["COCKROACHDB"])
app.include_router(user_router)


@app.get('/')
async def root():
    return {"project": "FindME", "status": "OK", "time_up": started_at}
