from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from google.auth.transport import requests
from google.oauth2 import id_token

from ..database import create_user, get_user, update_user_password
from ..schemas import (
    GoogleLoginRequest,
    Message,
    NewUser,
    Token,
    UpdatePasswordRequest,
    User,
    UserInDB,
)
from ..utils.auth import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
    get_password_hash,
)

router = APIRouter(
    tags=["Users"],
)


@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    """Login and recive a JWT to access data in the API, username is expected to be the user's email."""

    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return create_access_token(user.email)


@router.post("/signup", response_model=Token)
async def signup_for_access_token(user: NewUser) -> Token:
    exisiting_user = await get_user(user.email)
    if exisiting_user:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail=f"User with email '{user.email}' already exists",
        )

    user_for_db = UserInDB(
        **dict(user), hashed_password=get_password_hash(user.password)
    )
    await create_user(user_for_db)

    return create_access_token(user.email)


@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)) -> User:
    return current_user


@router.post("/login/google", response_model=Token)
async def login_with_google_token(request: GoogleLoginRequest) -> Token:
    """Exchange a token from Google for a user token."""
    try:
        token_info = id_token.verify_token(request.token, requests.Request())

        email = token_info["email"]
        user = await get_user(email)

        if not user:
            await create_user(
                UserInDB(
                    email=email,
                    hashed_password="",
                    full_name=email.split("@")[0],
                )
            )

        return create_access_token(email)

    except ValueError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Error while verifying token",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.put("/users/me/update-password", response_model=Message)
async def update_password(
    request: UpdatePasswordRequest, user: User = Depends(get_current_active_user)
) -> Message:

    new_hashed_password = get_password_hash(request.new_password)
    await update_user_password(user, new_hashed_password)

    return Message(detail="Password updated successfully")
