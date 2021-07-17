from typing import Optional, Union, List
import os
from fastapi import APIRouter, HTTPException, Depends, Header
from fastapi_sqlalchemy import db
from fastapi_jwt_auth import AuthJWT

from FindMe.Schemas.tasks import TasksAdd, GetSingleTask, TasksComplete
from FindMe.models import UserModel, TaskModel
from .Example_Response import tasks as example_resp
from FindMe.Utils.image import save_img_to_cloud, save_image_locally
from FindMe.Utils.imageSimilarity import cv_client

router = APIRouter()

TASK_CREATION_SCORE = 50


@router.post(
    "/add",
    tags=['Tasks'],
    responses=example_resp.task_added_response
)
async def add_task(task: TasksAdd, authorize: AuthJWT = Depends(), authorization: str = Header(...)):
    """
    Add Tasks for other user
    **access_token**: access token (in headers)
    - **title**: Title of the task
    - **hints**: Hints you would like to provide
    - **description**: Any description of the task
    - **city**: City in which this task can be completed
    - **country**: Country in which this task can be completed
    - **latitude**: Exact latitude of the task
    - **longitude**: Exact longitude of the task
    - **image_url**: Image base64
    """
    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Not Authorized")
    current_user = authorize.get_jwt_subject()
    db_user: UserModel = db.session.query(UserModel).filter(UserModel.email == current_user).first()
    file_loc = save_img_to_cloud(
        img_b64=task.image_url,
        file_prefix=db_user.username
    )
    task.image_url = file_loc
    db_task = TaskModel(**task.dict())
    db_user.tasks_added.append(db_task)
    db_user.score = UserModel.score + TASK_CREATION_SCORE
    db_user.save_to_db()
    return {'status': 'OK', 'message': "Task Created"}


@router.post(
    "/submit",
    tags=['Tasks']
)
async def complete_task(
        uid: int, task: TasksComplete, authorize: AuthJWT = Depends(), authorization: str = Header(...)
):
    """
    Add Tasks for other user
    **access_token**: access token (in headers)
    - **uid**: Task id in query params
    - **latitude**: Exact latitude of the task
    - **longitude**: Exact longitude of the task
    - **image_url**: Image base64
    """
    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Not Authorized")
    user_email = authorize.get_jwt_subject()
    db_task: TaskModel = db.session.query(TaskModel).filter(TaskModel.id == uid).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task Not found")
    db_user: UserModel = db.session.query(UserModel).filter(UserModel.email == user_email).first()
    if db_task in db_user.tasks_added:
        raise HTTPException(status_code=403, detail="Author of the task cannot complete that task")
    """
    Check if lies within same distance
    """
    file_loc, file_name = save_image_locally(
        img_b64=task.image,
        file_prefix=db_user.username
    )
    is_similar = cv_client.check_similar(db_task.image_url, file_loc)
    os.remove(file_loc)
    return is_similar


@router.get(
    "/",
    tags=['Tasks'],
    response_model=Union(GetSingleTask, List[GetSingleTask])
)
async def get_task(uid: Optional[str] = None, authorize: AuthJWT = Depends(), authorization: str = Header(...)):
    """
    Add Tasks for other user
    **access_token**: access token (in headers)
    - **id**: of the task
    """
    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Not Authorized")
    if uid is not None:
        db_task: UserModel = db.session.query(TaskModel).filter(TaskModel.id == uid).first()
        return db_task
    else:
        return db.session.query(TaskModel).all()
