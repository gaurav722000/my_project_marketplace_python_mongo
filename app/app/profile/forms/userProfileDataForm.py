from fastapi.param_functions import Body, Form
from fastapi import File, UploadFile, Depends
from typing import Optional

class UserProfileDataForm:
    def __init__(
            self,
            address: Optional[str] = Form(...),
    ):
        self.address = address
