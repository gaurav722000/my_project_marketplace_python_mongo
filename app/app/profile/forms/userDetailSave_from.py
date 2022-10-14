from fastapi.param_functions import Body, Form
from fastapi import File, UploadFile, Depends
from typing import Optional

class UserDetailSaveForm:
    def __init__(
            self,
            username: Optional[str] = Form(...),
            firstname: Optional[str] = Form(''),
            lastname: Optional[str] = Form(''),
            description: Optional[str] = Form(''),
            profilephoto: Optional[UploadFile] = File(None),
            coverphoto: Optional[UploadFile] = File(None),
            address: Optional[str] = Form(...),

    ):
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.description = description
        self.profilephoto = profilephoto
        self.coverphoto = coverphoto
        self.address = address
