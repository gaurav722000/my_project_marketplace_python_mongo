from fastapi.param_functions import Body, Form
from fastapi import File, UploadFile, Depends
from typing import Optional

class FinalizeAuctionForm:
    def __init__(
            self,
            tokenid : Optional[int] = Form(0),
    ):
        self.tokenid = tokenid
