from typing import Optional
from fastapi.param_functions import Body, Form
from fastapi import File, UploadFile, Depends

class MintNftForm:
    def __init__(
            self,
            # thumbnil: Optional[UploadFile] = File(None),
            thumbnil: Optional[str] = Form(''),
            ipfsid: Optional[str] = Form(''),
            name: Optional[str] = Form(''),
            description: Optional[str] = Form(''),
            tranhash: Optional[str] = Form(''),
            tokenid: Optional[int] = Form(0),
            type: Optional[str] = Form('image'),
            account: Optional[str] = Form(''),
            auxtype: Optional[str] = Form('NONE'),
            ipfsimgcid: Optional[str] = Form('')
    ):
        self.thumbnil = thumbnil
        self.ipfsid = ipfsid
        self.name = name
        self.description = description
        self.tranhash = tranhash
        self.tokenid = tokenid
        self.type = type
        self.account = account
        self.auxtype = auxtype
        self.ipfsimgcid = ipfsimgcid

