import datetime
from bson import ObjectId
import re
import random
import string
import logging
from fastapi import Depends
from shared.db import mdb
from .route import account
from .forms.mintNftForm import MintNftForm
from ..common.common_function import activity_log, error_log

logger = logging.getLogger(__name__)

@account.post("/account/mint_nft", tags=["account"])
async def MintMft(form_data: MintNftForm = Depends()):
    try:
        logger.info("mint_nft api == called")
        userData = list(mdb.users_list.find({'address' : form_data.account}))
        if len(userData):
            for i in userData:
                if(i['username'] != ""):
                    # mint_content = await form_data.thumbnil.read()
                    # store_path = "D:/gaurav/Personal/market_place_project1/backend_market_place_project1/app/app/account/MintNft/"
                    # mint_file = store_path + form_data.thumbnil.filename
                    # open(mint_file, 'wb').write(mint_content)

                    json = {
                        "thumbnil": form_data.thumbnil,
                        "ipfsid" : form_data.ipfsid,
                        "name": form_data.name,
                        "description": form_data.description,
                        "tranhash": form_data.tranhash,
                        "tokenid": form_data.tokenid,
                        "type": form_data.type,
                        "account": form_data.account,
                        'auxtype': form_data.auxtype,
                        'ipfsimgcid': form_data.ipfsimgcid,
                        "istatus" : 'Available',
                        "buyerid" : form_data.account,
                        "is_valid":0,
                        "ondate": datetime.datetime.now()
                    }

                    mdb.nft_mint.insert_one(json)
                    logger.info("mint_nft api == save successfully")
                    return {
                        "code": 200,
                        "status": "success",
                        "message": "Nft Mint Successfully"
                    }
                else :
                    logger.info("mint_nft api == profile not update")
                    return {
                        "code": 404,
                        "status": "error",
                        "message": "Please Update Your Profile"
                    }
        else:
            return {
                "code": 404,
                "status": "error",
                "message": "Please Update Your Profile"
            }

        # json = {
        #     "thumbnil": form_data.thumbnil,
        #     "ipfsid": form_data.ipfsid,
        #     "name": form_data.name,
        #     "description": form_data.description,
        #     "tranhash": form_data.tranhash,
        #     "tokenid": form_data.tokenid,
        #     "type": form_data.type,
        #     "account": form_data.account,
        #     'auxtype': form_data.auxtype,
        #     "is_valid": 0,
        #     "ondate": datetime.datetime.now()
        # }
        #
        # mdb.nft_mint.insert_one(json)
        # logger.info("mint_nft api == save successfully")
        # return {
        #     "code": 200,
        #     "status": "success",
        #     "message": "Nft Mint Successfully"
        # }

    except Exception as e: 
        logger.exception("Error {} occurred while user mint nft .".format(e))
        return {
            "code": 500,
            "status": "error",
            "message": " Exception {} occurred while user mint nft .".format(e)
        }
