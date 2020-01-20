import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from utilities import abort_func


AUTH0_DOMAIN = 'dev-z57q0g2a.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'http://0.0.0.0:8080/'

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header
def get_token_auth_header():
    """
    Function obtains token from Authorization header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        abort_func(401, "authorization_header_missing", False )
    parts = auth.split()
    if parts[0].lower() != "bearer":
        abort_func(401, "invalid_header! Authorization header must start with 'Bearer'", False)
    elif len(parts) == 1:
        abort_func(401, "invalid_header! Token not found", False)
    elif len(parts) > 2:
        abort_func(401, "invalid_header! Authorization header must be 'Bearer token'", False)
    token = parts[1]
    return token


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        abort_func(400, "Permissions not included in JWT.", False)
    if permission not in payload['permissions']:
        abort_func(403, "Permission not found.", False)
    return True


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    # GET THE DATA IN THE HEADER
    unverified_header = jwt.get_unverified_header(token)
    # CHOOSE OUR KEY
    rsa_key = {}
    if 'kid' not in unverified_header:
        abort_func(401, "invalid_header!Authorization malformed.", False)
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    # Finally, verify!!!
    if rsa_key:
        try:
            # USE THE KEY TO VALIDATE THE JWT
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload
        except jwt.ExpiredSignatureError:
            abort_func(401, "Token expired.", False)
        except jwt.JWTClaimsError:
            abort_func(401,
                       "Incorrect claims. Please, check the audience and issuer.",
                       False)
        except Exception:
            abort_func(400, "Unable to parse authentication token.", False)
    abort_func(400, "Invalid Header! Unable to find the appropriate key.", False)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            # print(payload)
            check_permissions(permission, payload)
            return f(*args, **kwargs)
        return wrapper
    return requires_auth_decorator
