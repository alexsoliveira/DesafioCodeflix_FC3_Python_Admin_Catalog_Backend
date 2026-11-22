import os
import jwt

from src.core._shared.infrastructure.auth.auth_service_interface import AuthServiceInterface

class JwtAuthService(AuthServiceInterface):
    def __init__(self, token: str = "") -> None: 
        self.public_key = os.getenv("AUTH_PUBLIC_KEY")
        self.token = token.replace('Bearer ', '', 1)

    def _decode_token(self) -> dict:
        try:
            return jwt.decode(self.token, self.public_key, algorithms=["RS256"], audience="account")
        except jwt.PyJWTError:
            return {}
        

    def is_authenticate(self) -> bool:
        return bool(self._decode_token())


    def has_role(self, role: str) -> bool:
        return role in self._decode_token().get("realm_access", {}).get("roles", [])
    
        # decoded_token = self._decode_token()
        # realm_access = decoded_token.get("realm_access", {})
        # roles = realm_access.get("roles", [])
        # return role in roles