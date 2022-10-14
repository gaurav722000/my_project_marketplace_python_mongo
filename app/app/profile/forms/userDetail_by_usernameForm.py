from fastapi.param_functions import Body, Form
from fastapi import File, UploadFile, Depends
from typing import Optional



class GetUserDetailByUserNameForm:
    def __init__(
            self,
            username: Optional[str] = Form(''),
    ):
        self.username = username


