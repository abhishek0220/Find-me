import datetime
from fastapi import APIRouter, HTTPException, Depends, Header
from fastapi_sqlalchemy import db
from fastapi_jwt_auth import AuthJWT

from FindMe.Schemas.tasks import TasksAdd
from FindMe.models import UserModel
from .Example_Response import user as example_resp

router = APIRouter()


@router.post(
    "/add",
    tags=['User'],
    responses=example_resp.user_register_example_response
)
async def add_task(task: TasksAdd, authorize: AuthJWT = Depends(), authorization: str = Header(...)):
    """
    """
    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Not Authorized")
    current_user = authorize.get_jwt_subject()
    db_user: UserModel = db.session.query(UserModel).filter(UserModel.email == current_user).first()
    return db_user
