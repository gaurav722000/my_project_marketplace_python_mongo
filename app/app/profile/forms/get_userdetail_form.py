from fastapi.param_functions import Body, Form
from fastapi import File, UploadFile, Depends
from typing import Optional



class GetUserDetailForm:
    def __init__(
            self,
            address: Optional[str] = Form(''),
    ):
        self.address = address


