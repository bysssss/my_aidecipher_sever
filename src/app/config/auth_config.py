import jwt

from typing import Optional
from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from fastapi.exceptions import HTTPException
from pydantic import BaseModel


class MyAuth(BaseModel):
    token: str
    user_id: str
    email: Optional[str] = ''
    roles: list[str]

    def __str__(self) -> str:
        return f"{self.token[:4]}...{self.user_id[:4]}...{self.roles}"


_token_of_bearer = OAuth2PasswordBearer(
    tokenUrl='/.../token',
    scopes={
        "ADMIN": "관리자용",
        "USER": "사용자용",
    },
    auto_error=True)


def init_auth(
    security: SecurityScopes,
    # token: str = Depends(_token_of_bearer),
):
    try:
        # claims = jwt_util.decode_token(token, secret=my_settings.etc.jwt_secret)
        user_id = '1234567890'
        email = 'test@test.test'
        test_auth = MyAuth(token='', user_id=user_id, email=email, roles=['ADMIN'])

        is_role = False
        for role in test_auth.roles:
            if role in security.scopes:
                is_role = True
                break
        if not is_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"role {test_auth.roles} is not enough scopes",
                headers={"WWW-Authenticate": f"Bearer scope=\"{security.scope_str}\""})

    except jwt.ExpiredSignatureError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e), headers={"WWW-Authenticate": "Bearer"})
    except jwt.DecodeError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e), headers={"WWW-Authenticate": "Bearer"})
    except jwt.InvalidAudienceError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e), headers={"WWW-Authenticate": "Bearer"})
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e), headers={"WWW-Authenticate": "Bearer"})
    return test_auth
