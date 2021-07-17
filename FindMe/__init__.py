import os
from fastapi import FastAPI, Request
from fastapi_sqlalchemy import DBSessionMiddleware
from datetime import datetime
from FindMe.APIs.user import router as user_router
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
import pytz

from pydantic import BaseModel

app = FastAPI(
    title="Find ME",
    description="Backend APIs for find me Android app",
    version="1.0.0"
)

IST = pytz.timezone('Asia/Kolkata')
started_at = datetime.now(IST)


app.add_middleware(DBSessionMiddleware, db_url=os.environ["COCKROACHDB"])
app.include_router(user_router)


class Settings(BaseModel):
    authjwt_secret_key: str = os.environ['JWT_SECRET']


@AuthJWT.load_config
def get_config():
    return Settings()


@app.exception_handler(AuthJWTException)
def auth_jwt_exception_handler(request: Request, exc: AuthJWTException):
    return {
        'status_code': exc.status_code,  # type: ignore
        'content': {
            "detail": exc.message  # type: ignore
        }
    }


@app.get('/')
async def root():
    return {"project": "FindME", "status": "OK", "time_up": started_at}
