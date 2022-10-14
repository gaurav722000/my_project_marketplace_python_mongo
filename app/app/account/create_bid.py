import datetime
from bson import ObjectId
import re
import random
import string
import logging
from fastapi import Depends
from shared.db import mdb
from .route import account
from .forms.create_bidForm import CreateBidForm

logger = logging.getLogger(__name__)

@account.post("/account/create_bid", tags=["account"])
async def createBid(form_data: CreateBidForm = Depends()):
    try:
        logger.info("create_bid api == called")
        if mdb.auction_sell.count({'nftid': form_data.nftid, 'istatus': 'CONFIRM'}) > 0:
            json = {
                "nftid": form_data.nftid,
                "bidprice" : form_data.bidprice,
                "tranhash": form_data.tranhash,
                "ttype": 'BID',
                "address": form_data.address,
                "tokenid" : form_data.tokenid,
                "is_valid":0,
                "ondate": datetime.datetime.now()
            }

            mdb.tbl_nftbid.insert_one(json)
            mdb.auction_sell.update_one({"nftid": form_data.nftid },{'$set': {'lastprice': form_data.bidprice}})
            logger.info("create_bid api == save successfully")
            return {
                "code": 200,
                "status": "success",
                "message": "Bid Successfully"
            }
        else:
            return {
                "code": 404,
                "status": "error",
                "message": "No Data Found"
            }
    except Exception as e:
        logger.exception("Error {} occurred while create_bid .".format(e))
        return {
            "code": 500,
            "status": "error",
            "message": " Exception {} occurred while create_bid .".format(e)
        }
