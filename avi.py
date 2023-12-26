from __future__ import annotations
from datetime import datetime, timedelta
from typing import Any, Optional, Union
import jwt
from fastapi.security.api_key import APIKeyHeader
from fastapi.routing import APIRouter
from fastapi import Security, Depends
from fastapi.param_functions import Form
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from passlib.context import CryptContext
from pydantic import BaseModel, SecretStr

SECRET_KEY = <SECRET_KEY> //To be used during hashing
ALGORITHM = <ALGORITHM> // Hashing algorithm
ACCESS_TOKEN_EXPIRE_SECONDS = <ACCESS_TOKEN_EXPIRE_SECONDS>
API_KEY_NAME = <API_KEY_NAME> keyname for the API KEY

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

class Token(BaseModel):
    '''Token Model'''
    access_token: str
    expires_in: int
    token_type: str


class TokenData(BaseModel):
    '''Token data model'''
    username: Optional[str] = None
    user_id: Optional[str] = None
    account_id: int = None
    client_id: str = None


class ClientCredentials(BaseModel):
    '''Client Credentials'''
    client_id: Optional[str] = None
    client_secret: Optional[str] = None


class UserCredentials(BaseModel):
    '''User Credentials'''
    username: Optional[str] = None
    password: Optional[SecretStr] = None
    account_id: Optional[int] = None


class User(BaseModel):
    '''User Model'''
    username: str
    disabled: Optional[bool] = None


class UserInDB(User):
    '''User in DB Model'''
    account_id: int
    user_id: int
    client_id: Optional[str] = None
    username: str
    hashed_password: Optional[str] = None


class AuthParams(BaseModel):
    '''Auth Parameter Model'''
    username: str = Form(...)
    password: SecretStr = Form(...)
    client_id: str = Form(...)
    client_secret: str = Form(...)
    
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
router = APIRouter()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Password Verification"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    '''retruns the hashed password'''
    return pwd_context.hash(password)


def get_user(db: dict[str, dict[str, Optional[str]]], username: Optional[str],) -> UserInDB:
    """return's the user details"""
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db: dict[str, dict[str, Optional[str]]], username: str, password: str,) -> Union[bool, UserInDB]:
    '''User Authentications'''
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta = None) -> bytes:
    '''creates access token'''
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Security(api_key_header),) -> UserInDB:
    '''returns the current user'''
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_payload = payload.get("sub")
        if token_payload is None:
            raise exception.could_not_validate_credentials()
        token_data = TokenData(
            username=token_payload['user_name'], user_id=token_payload['user_id'], client_id=token_payload['client_id'])
    except PyJWTError:
        raise exception.could_not_validate_credentials()
    user_data = UserService.get_user_info_by_client_id(token_data.client_id)
    user = get_user(user_data, username=token_data.username)    
    if user is None:
        raise exception.could_not_validate_credentials()
    return user

@router.post("/clientCredentials", response_model=ClientCredentials, tags=["Token"], include_in_schema=False)
async def login_for_client_credentials(form_data: UserCredentials = Depends(),) -> dict[str, Any]:
    '''generate client credentials'''
    user_data = UserService.get_users_info_by_username(form_data.username)
    user = authenticate_user(
        user_data, form_data.username, form_data.password.get_secret_value())
    if not user:
        raise exception.invalid_username_password()
    client_credentials = BaseService.generate_client_credentials(
        user.user_id, form_data.account_id)
    return{"client_id": client_credentials['client_id'], "client_secret": client_credentials['client_secret']}

@router.post("/token", response_model=Token, tags=["Token"])
async def login_for_access_token(form_data: AuthParams = Depends(),) -> dict[str, Any]:
    """
    Gives the bearer token used for Authorization.

    - **username**: username used to login to the application
    - **password**: password for the corresponding username
    - **client_id**: client id provided by the infra team.
    - **client_secret**: client secret provided by the infra team.
    :param item: User input.
    """
    user_data = UserService.get_user_info_by_client_credentials(
        form_data.client_id, form_data.client_secret)
    if not user_data:
        raise exception.invalid_client_id_and_client_secret()
    user = authenticate_user(
        user_data, form_data.username, form_data.password.get_secret_value())
    if not user:
        raise exception.invalid_username_password()
    access_token_expires = timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS)
    access_token = create_access_token(
        data={"sub": {"user_name": user.username,
                      "user_id": user.user_id,
                      "account_id": user.account_id,
                      "client_id": user.client_id}},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "expires_in": ACCESS_TOKEN_EXPIRE_SECONDS, "token_type": "bearer"}