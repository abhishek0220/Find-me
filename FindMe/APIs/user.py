import datetime
from fastapi import APIRouter, HTTPException, Depends, Header
from fastapi_sqlalchemy import db
from fastapi_jwt_auth import AuthJWT
from typing import Optional

from FindMe.Schemas.user import UserRegister, UserLogin, TokenJWT, CompleteUserInfo
from FindMe.models import UserModel
from FindMe.Utils.image import save_img_to_cloud, save_image_locally
from FindMe.Utils.gstorage import cloud_storage
from .Example_Response import user as example_resp

router = APIRouter()

def profile_pic_update(db_user,b64_img):
    if(db_user.display_picture is not None):
        cloud_storage.delete(db_user.display_picture)     
    new_url = save_img_to_cloud(
        img_b64=b64_img,
        file_prefix=db_user.username
    )     
    db_user.display_picture = new_url    
    

@router.post(
    "/signup",
    tags=['Authentication'],
    responses=example_resp.user_register_example_response
)
async def signup(user: UserRegister):
    """
    User Login Endpoint
    - **name**: Name of the registrant
    - **username**: Username of the registrant (unique)
    - **email**: Email by which you want to register (unique)
    - **password**: password to used at the time of login
    """
    return {"msg":"Disabled"}
    user_exist = db.session.query(UserModel).filter(UserModel.email == user.email).first()
    if user_exist:
        raise HTTPException(status_code=400, detail="User with same email already exist")
    user_exist = db.session.query(UserModel).filter(UserModel.username == user.username).first()
    if user_exist:
        raise HTTPException(status_code=400, detail="User with same username already exist")
    db_user = UserModel(**user.dict())
    db_user.save_to_db()
    return {'status': 'OK', 'message': "User Created"}


@router.post(
    "/login",
    response_model=TokenJWT,
    tags=['Authentication'],
    responses=example_resp.user_login_example_response
)
async def login(user: UserLogin,  authorize: AuthJWT = Depends()):
    """
    User Login Endpoint
    - **email**: Email by which you want to register
    - **password**: password to used at the time of login
    """
    db_user: UserModel = db.session.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user is not None and user.password == db_user.password:
        expires = datetime.timedelta
        token = TokenJWT.construct(
            access_token=authorize.create_access_token(subject=user.email, expires_time=expires(days=7)),
            refresh_token=authorize.create_refresh_token(subject=user.email, expires_time=expires(days=14))
        )
        return token
    else:
        raise HTTPException(status_code=400, detail="Invalid ID/Password")


@router.post(
    '/refresh',
    response_model=TokenJWT,
    tags=['Authentication'],
)
def refresh(authorize: AuthJWT = Depends(), authorization: str = Header(...)):
    """
    User access token refresh Endpoint
    - **refresh_token**: Refresh token to refresh the access token (in headers)
    Authorization: Bearer {REFRESH_TOKEN}
    """
    raise NotImplementedError


@router.get(
    "/user",
    tags=['User'],
    response_model=CompleteUserInfo,
    responses=example_resp.user_get_user_example_response
)
async def get_user_details(username: Optional[str] = None, authorize: AuthJWT = Depends(), authorization: str = Header(...)):
    """
    User get details endpoint
    - **access_token**: access token (in headers)
    Authorization: Bearer {ACCESS_TOKEN}
    """
    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Not Authorized")
    if username is None:
        user_email = authorize.get_jwt_subject()
        db_user: UserModel = db.session.query(UserModel).filter(UserModel.email == user_email).first()
    else:
        db_user: UserModel = db.session.query(UserModel).filter(UserModel.username == username).first()
    return db_user
