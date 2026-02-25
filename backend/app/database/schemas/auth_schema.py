from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(Token):
    pass

class TokenResponse(Token):
    pass

class LoginRequest(Token):
    pass

class ChangePass(BaseModel):
    current: str
    new: str
