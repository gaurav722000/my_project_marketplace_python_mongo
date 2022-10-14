import datetime
from bson import ObjectId
import re
import random
import string
import logging
import time
from fastapi import Depends
from shared.db import mdb
from .route import account
from .forms.finalize_auctionForm import FinalizeAuctionForm

logger = logging.getLogger(__name__)

@account.post("/account/finalize_auction", tags=["account"])
async def finalizeAuction(form_data: FinalizeAuctionForm = Depends()):
    try:
        # ts = time.time()
        # print("TSSSSS", ts)
        if mdb.nft_mint.count({'tokenid':form_data.tokenid , 'istatus':'aux'}) > 0 :
            mintData = mdb.nft_mint.find({'tokenid':form_data.tokenid})
            for i in mintData:
                auxData = mdb.auction_sell.find({'nftid' : str(i['_id']) , 'istatus':'CONFIRM'}).sort([('_id', -1)]).limit(1)
                # auxData = mdb.auction_sell.find({'nftid' : str(i['_id']) , 'istatus':'CONFIRM'})._addSpecial( "$orderby", { '_id' : -1 }).limit(1)
                for j in auxData:
                    # if mdb.auction_sell.count({"_id": ObjectId(str(j['_id'])), 'enddate':{'$lt':str(ts)} , 'istatus':'CONFIRM'}) > 0 :
                    if mdb.auction_sell.count({"_id": ObjectId(str(j['_id'])) , 'istatus':'CONFIRM'}) > 0 :
                        # bidData = mdb.tbl_nftbid.find({'nftid': str(j['_id']) }).sort( { '_id': -1 } ).limit(1)
                        bidData = mdb.tbl_nftbid.find({'nftid': str(j['nftid']) }).sort([('_id', -1)]).limit(1)
                        for k in bidData:
                            if k['_id'] != '' :
                                biddata = mdb.tbl_nftbid.find({"_id":ObjectId(str(k['_id']))})
                                for x in biddata:
                                    mdb.auction_sell.update_one({'_id': ObjectId(str(j['_id']))}, {'$set': {'buyerid':x['address'], 'lastprice':x['bidprice'], 'istatus':'TRANSFER'}})
                                    mdb.nft_mint.update_one({'_id': ObjectId(str(i['_id']))}, {'$set': {'buyerid':x['address'], 'istatus':'Available'}})
                                    mdb.tbl_nftbid.update_one({"_id":ObjectId(k['_id'])}, {'$set': {'ttype':"Finalize"}})
                                    return{
                                        "msg":"OK"
                                    }
                            else:
                                print("88888")
                                mdb.nft_mint.update_one({'_id': str(i['_id'])}, {'$set': {'istatus':'Available'}}) 
                                mdb.auction_sell.update_one({'nftid': str(i['_id'])}, {'$set': {'istatus':'TRANSFER'}})
                                return{
                                    "msg":"OK"
                                }

    except Exception as e:
        logger.exception("Error {} occurred while finalize_auction .".format(e))
        return {
            "code": 500,
            "status": "error",
            "message": " Exception {} occurred while finalize_auction .".format(e)
        }
