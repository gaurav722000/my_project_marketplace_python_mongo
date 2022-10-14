from typing import Optional
from fastapi.param_functions import Body, Form

class tokenIdListDetailForm:
    def __init__(
            self,
            tokenidList: str = Form(''),
    ):
        self.tokenidList = tokenidList

