from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Form, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import Field
from typing import Any, Dict, List, Optional, Union

from fastapi.exceptions import HTTPException
from fastapi.openapi.models import OAuth2 as OAuth2Model
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.param_functions import Form
from fastapi.security.base import SecurityBase
from fastapi.security.utils import get_authorization_scheme_param
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

app = FastAPI()

# Define a dictionary to store client_id and client_secret pairs (replace with a more secure storage in production)
client_credentials_db = {
    "client_id_1": {
        "client_secret": "client_secret_1",
        "grant_type": "client_credentials",
        "scope": "read write",
    }
}

class CustomOAuth2PasswordRequestForm():
    def __init__(
        self,
        grant_type: str = Form(None, regex="client_credentials"),
        username: Optional[str] = Form(None),
        password: Optional[str] = Form(None),
        scope: str = Form(""),
        client_id: Optional[str] = Form(None),
        client_secret: Optional[str] = Form(None),
    ):
        self.grant_type = grant_type
        self.username = username
        self.password = password
        self.scopes = scope.split()
        self.client_id = client_id
        self.client_secret = client_secret

# Define OAuth2 password bearer for client_id and client_secret authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def authenticate_client(client_id: str, client_secret: str):
    client_credentials = client_credentials_db.get(client_id)
    if client_credentials and client_credentials["client_secret"] == client_secret:
        return True
    return False

# Dependency function to get the current client based on the provided token
def get_current_client(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    client_id, client_secret = token.split(":")
    if not authenticate_client(client_id, client_secret):
        raise credentials_exception
    return client_id

# Token URL endpoint
@app.post("/token")
async def token(form_data: CustomOAuth2PasswordRequestForm = Depends()):
    client_id = form_data.client_id
    client_secret = form_data.client_secret

    # Authenticate the client
    if not authenticate_client(client_id, client_secret):
        raise HTTPException(
            status_code=401,
            detail="Invalid client credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # In a real-world scenario, you might check user credentials here and generate a token
    # For demonstration purposes, we'll just return a fixed token
    token = f"{client_id}:{client_secret}"

    return {"access_token": token, "token_type": "bearer"}

# Endpoint to get information for the current client
@app.get("/clients/me")
async def read_clients_me(current_client: str = Depends(get_current_client)):
    return {"client_id": current_client}
