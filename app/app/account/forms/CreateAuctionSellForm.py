from typing import Optional
from fastapi.param_functions import Body, Form
from fastapi import File, UploadFile, Depends

class CreateAuctionSellForm:
    def __init__(
            self,
            nftid: str = Form(...),
            tranhash: str = Form(''),
            type: str = Form(...),
            price: float = Form(...),
            startdate: Optional[str] = Form(''),
            enddate: Optional[str] = Form(''),
            tokenid : int = Form(...),
            address : str = Form(...),
            lastprice : Optional[int] = Form(0),
    ):
        self.nftid = nftid
        self.tranhash = tranhash
        self.type = type
        self.price = price
        self.startdate = startdate
        self.enddate = enddate
        self.tokenid = tokenid
        self.address = address
        self.lastprice = lastprice

