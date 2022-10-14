from fastapi.param_functions import Body, Form
from fastapi import File, UploadFile, Depends

class UpdateUserDetailByIdForm:
    def __init__(
            self,
            # id : str = Form(''),
            address : str = Form(...),
            username : str = Form(''),
            firstname : str = Form(''),
            description: str = Form(''),
            profilephoto: UploadFile = File(''),
            coverphoto: UploadFile = File(''),
    ):
        # self.id = id
        self.address = address
        self.username = username
        self.firstname = firstname
        self.description = description
        self.profilephoto = profilephoto
        self.coverphoto = coverphoto

        
