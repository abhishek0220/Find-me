import datetime
from fastapi import APIRouter, HTTPException, Depends, Header
from fastapi_sqlalchemy import db
from fastapi_jwt_auth import AuthJWT

from FindMe.Schemas.user import UserRegister, UserLogin, TokenJWT
from FindMe.models import UserModel

router = APIRouter()


@router.post(
    "/signup",
)
async def signup(user: UserRegister):
    """
    User Login Endpoint
    - **name**: Name of the registrant
    - **email**: Email by which you want to register
    - **password**: password to used at the time of login
    """
    user_exist = db.session.query(UserModel).filter(UserModel.email == user.email).first()
    if user_exist:
        raise HTTPException(status_code=400, detail="User already exist")
    db_user = UserModel(**user.dict())
    db_user.save_to_db()
    return {'status': 'OK', 'message': "User Created"}


@router.post(
    "/login",
    response_model=TokenJWT
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
    response_model=TokenJWT
)
def refresh(authorize: AuthJWT = Depends(), authorization: str = Header(...)):
    """
    User access token refresh Endpoint
    - **refresh_token**: Refresh token to refresh the access token (in headers)
    Authorization: Bearer {REFRESH_TOKEN}
    """
    raise NotImplementedError


@router.get(
    "/info",
)
async def get_details():
    """
    User Login Endpoint
    - **email**: Email by which you want to register
    - **password**: password to used at the time of login
    - Add schema in schemas.user file
    """
    raise NotImplementedError
