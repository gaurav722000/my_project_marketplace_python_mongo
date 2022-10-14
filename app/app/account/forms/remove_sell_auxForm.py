from typing import Optional
from fastapi.param_functions import Body, Form
from fastapi import File, UploadFile, Depends

class REmoveSellAuxForm:
    def __init__(
            self,
            tokenid: Optional[int] = Form(0),
            tranhash: Optional[str] = Form('')
    ):
        self.tokenid = tokenid
        self.tranhash = tranhash

