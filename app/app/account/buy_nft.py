import datetime
from bson import ObjectId
import re
import random
import string
import logging
from fastapi import Depends
from shared.db import mdb
from .route import account
from .forms.buNftForm import BuyNftForm

logger = logging.getLogger(__name__)

@account.post("/account/buy_nft", tags=["account"])
async def BuyNft(form_data: BuyNftForm = Depends()):
    try:
        if mdb.users_list.count({'address': form_data.address}) <= 0 :
            mdb.users_list.insert_one({
                "username": '',
                "firstname": '',
                "lastname": '',
                "description": '',
                "profilephoto": '',
                "coverphoto": '',
                "address": form_data.address,
                "is_valid": 0,
                "ondate": datetime.datetime.now(),
            })
        if mdb.auction_sell.count({'_id':ObjectId(str(form_data.auxid)) , 'nftid': form_data.nftid, 'buyerid': {'$ne': form_data.address}, 'istatus' : 'CONFIRM'}) > 0 :
            auxData = mdb.auction_sell.find({'_id':ObjectId(str(form_data.auxid)), 'nftid' : form_data.nftid})
            for i in auxData:
                mdb.tbl_nftbid.insert_one({
                    "nftid": form_data.nftid,
                    "auxid" : form_data.auxid,
                    "bidprice": i['price'],
                    "tranhash": form_data.tranhash,
                    "ttype": 'BUY',
                    "address": form_data.address,
                    "tokenid": form_data.tokenid,
                    "is_valid": 0,
                    "ondate": datetime.datetime.now()
                })
                json = {
                    "buyerid" : form_data.address,
                    "lastprice" : i['price'],
                    "tradehash" : form_data.tranhash,
                    "istatus" : 'TRANSFER'
                }
                mdb.auction_sell.update_one({'_id':ObjectId(str(form_data.auxid)), "nftid": form_data.nftid}, {'$set': json})
                mdb.nft_mint.update_one({"_id": ObjectId(form_data.nftid)}, {'$set': {"buyerid": form_data.address , 'istatus' : 'Available'}})
                return {
                    "code" : 200,
                    "msg" : "buy successfull"
                }
    except Exception as e:
        logger.exception("Error {} occurred while buy_nft .".format(e))
        return {
            "code": 500,
            "status": "error",
            "message": " Exception {} occurred while buy_nft .".format(e)
        }
