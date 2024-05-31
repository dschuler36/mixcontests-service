# auth.py
from jose import jwt
from jose.exceptions import JWTError
from fastapi import Request, HTTPException, Security
from fastapi.security import HTTPBearer
from typing import Dict
import requests
from app.api.config import AUTH0_DOMAIN, API_IDENTIFIER, ALGORITHMS


class Auth0HTTPBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials = await super().__call__(request)
        if credentials:
            token = credentials.credentials
            try:
                payload = self.decode_jwt(token)
                request.state.user = payload
                return credentials
            except JWTError:
                raise HTTPException(
                    status_code=401, detail="Invalid token"
                )
        else:
            raise HTTPException(
                status_code=401, detail="Invalid authorization code"
            )

    def decode_jwt(self, token: str) -> Dict:
        header = jwt.get_unverified_header(token)
        rsa_key = self.get_rsa_key(header)
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_IDENTIFIER,
                    issuer=f"https://{AUTH0_DOMAIN}/",
                )
                return payload
            except JWTError as e:
                raise e
        raise HTTPException(status_code=401, detail="Invalid token")

    def get_rsa_key(self, header):
        jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
        jwks = requests.get(jwks_url).json()
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }
        return rsa_key

auth_scheme = Auth0HTTPBearer()
