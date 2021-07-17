from fastapi import APIRouter
router = APIRouter()


@router.post(
    "/signup",
)
async def signup():
    """
    User Login Endpoint
    - **name**: Name of the registrant
    - **email**: Email by which you want to register
    - **password**: password to used at the time of login
    - Add other details as well that maybe needed
    - Add schema in schemas.user file
    """
    raise NotImplementedError


@router.post(
    "/login",
)
async def login():
    """
    User Login Endpoint
    - **email**: Email by which you want to register
    - **password**: password to used at the time of login
    - Add schema in schemas.user file
    """
    raise NotImplementedError
