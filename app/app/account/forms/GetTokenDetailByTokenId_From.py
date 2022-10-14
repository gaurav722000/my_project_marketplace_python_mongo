from typing import Optional
from fastapi.param_functions import Body, Form
from fastapi import File, UploadFile, Depends

class GetTokenDetailByIdForm:
    def __init__(
            self,
            tokenid: Optional[int] = Form(0),
    ):
        self.tokenid = tokenid

