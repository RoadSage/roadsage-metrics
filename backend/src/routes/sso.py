from typing import Any

from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Request
from starlette.config import Config

from ..database import create_user, get_user
from ..schemas import Token, UserInDB
from ..utils.auth import create_access_token

router = APIRouter(
    tags=["Users"],
)

config = Config("./.env")
oauth = OAuth(config)

oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


@router.get("/login/google")
async def login_with_google(request: Request) -> Any:
    """Redirects to the Google login page"""

    return await oauth.google.authorize_redirect(
        request, request.url_for("callback_from_google_login")
    )


@router.get("/login/google/callback", response_model=Token)
async def callback_from_google_login(request: Request) -> Token:
    """Receives the response from the Google login page and logins them into the app"""

    token = await oauth.google.authorize_access_token(request)
    user = await oauth.google.parse_id_token(request, token)

    email = user.get["email"]
    name = user.get["name"]

    # Create the user if it doesn't exist
    if not get_user(email):
        create_user(UserInDB(email=email, hashed_password="", full_name=name))

    return create_access_token(email)
