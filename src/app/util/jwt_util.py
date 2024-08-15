import uuid
from datetime import datetime, timedelta
import jwt


def encode_token(payload: dict = dict(), secret: str = "", expire: int = 18):
    claims = {
        'iss': 'scp-aislider',
        'sub': '',
        'aud': list(),
        'exp': datetime.utcnow() + timedelta(hours=expire),
        'nbf': datetime.utcnow(),
        'iat': datetime.utcnow(),
        'jti': str(uuid.uuid4()),
    }
    claims.update(payload)
    token = jwt.encode(claims, secret, algorithm='HS256')
    return token


def decode_token(token, secret: str = ""):
    try:
        claims = jwt.decode(token, secret, algorithms=['HS256'])
    except jwt.ExpiredSignatureError as e:
        raise e
    except jwt.DecodeError as e:
        raise e
    except jwt.InvalidAudienceError as e:
        raise e
    except Exception as e:
        raise e
    return claims
