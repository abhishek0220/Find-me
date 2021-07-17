from fastapi import APIRouter, HTTPException, Depends, Header
from fastapi_sqlalchemy import db
from fastapi_jwt_auth import AuthJWT

from FindMe.Schemas.tasks import TasksAdd
from FindMe.models import UserModel, TaskModel
from .Example_Response import tasks as example_resp
from FindMe.Utils.image import save_img_to_cloud

router = APIRouter()


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
    db_user.save_to_db()
    return {'status': 'OK', 'message': "Task Created"}