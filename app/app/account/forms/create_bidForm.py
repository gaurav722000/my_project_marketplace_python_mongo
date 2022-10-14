from fastapi.param_functions import Body, Form
from fastapi import File, UploadFile, Depends
from typing import Optional

class CreateBidForm:
    def __init__(
            self,
            nftid: Optional[str] = Form(...),
            bidprice: Optional[str] = Form(...),
            tranhash: Optional[str] = Form(''),
            address : Optional[str] = Form(...),
            tokenid : Optional[int] = Form(0),
    ):
        self.nftid = nftid
        self.bidprice = bidprice
        self.tranhash = tranhash
        self.address = address
        self.tokenid = tokenid
