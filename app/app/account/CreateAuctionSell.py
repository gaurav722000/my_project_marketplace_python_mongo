import datetime
from bson import ObjectId
import re
import random
import string
import logging
from fastapi import Depends
from shared.db import mdb
from .route import account
from .forms.CreateAuctionSellForm import CreateAuctionSellForm
from ..common.common_function import activity_log, error_log

logger = logging.getLogger(__name__)

@account.post("/account/create_auctionsell", tags=["account"])
async def CreateAuctionSell(form_data: CreateAuctionSellForm = Depends()):
    try:
        logger.info("create_auctionsell api == called")
        if mdb.nft_mint.count({'tokenid': form_data.tokenid , 'istatus':'Available'}) > 0 :
            nftMintData = mdb.nft_mint.find({'tokenid': form_data.tokenid, 'istatus':'Available'})
            for i in nftMintData:
                if(i['_id'] == ObjectId(form_data.nftid)):
                    json = {
                        "nftid": form_data.nftid,
                        "tranhash": form_data.tranhash,
                        "type": form_data.type,
                        "price": form_data.price,
                        "startdate": form_data.startdate,
                        "enddate": form_data.enddate,
                        "tokenid": form_data.tokenid,
                        "address": form_data.address,
                        "lastprice" : form_data.price,
                        "buyerid" : form_data.address,
                        "istatus" : "CONFIRM",
                        "is_valid": 0,
                        "ondate": datetime.datetime.now()
                    }
                    mdb.auction_sell.insert_one(json)
                    mdb.nft_mint.update_one({"tokenid":form_data.tokenid} ,{'$set': {'auxtype':form_data.type , 'istatus':form_data.type}})
                    logger.info("create_auctionsell api successfully")
                    return {
                        "code": 200,
                        "status": "success",
                        "message": "Auction Successfully"
                    }
                else :
                    logger.error("create_auctionsell somthing wrong")
                    return {
                        "code": 404,
                        "status": "error",
                        "message": "Invalid Selected Asset."
                    }
            
        # nftMintData = mdb.nft_mint.find({'tokenid': form_data.tokenid})
        # for i in nftMintData:
        #     if(i['_id'] == ObjectId(form_data.nftid)):
        #         json = {
        #             "nftid": form_data.nftid,
        #             "tranhash": form_data.tranhash,
        #             "type": form_data.type,
        #             "price": form_data.price,
        #             "startdate": form_data.startdate,
        #             "enddate": form_data.enddate,
        #             "tokenid": form_data.tokenid,
        #             "address": form_data.address,
        #             "lastprice" : form_data.price,
        #             "buyerid" : form_data.address,
        #             "istatus" : "CONFIRM",
        #             "is_valid": 0,
        #             "ondate": datetime.datetime.now()
        #         }
        #         mdb.auction_sell.insert_one(json)
        #         mdb.nft_mint.update_one({"tokenid":form_data.tokenid} ,{'$set': {'auxtype':form_data.type , 'istatus':form_data.type}})
        #         logger.info("create_auctionsell api successfully")
        #         return {
        #             "code": 200,
        #             "status": "success",
        #             "message": "Auction Successfully"
        #         }
        #     else :
        #         logger.error("create_auctionsell somthing wrong")
        #         return {
        #             "code": 404,
        #             "status": "error",
        #             "message": "Invalid Selected Asset."
        #         }
        
    except Exception as e: 
        logger.exception("Error {} occurred while create auction sell nft .".format(e))
        return {
            "code": 500,
            "status": "error",
            "message": " Exception {} occurred while create auction sell nft .".format(e)
        }
