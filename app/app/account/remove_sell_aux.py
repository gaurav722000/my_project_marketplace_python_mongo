import datetime
from bson import ObjectId
import re
import random
import string
import logging
from fastapi import Depends
from shared.db import mdb
from .route import account
from .forms.remove_sell_auxForm import REmoveSellAuxForm

logger = logging.getLogger(__name__)

@account.post("/account/remove_sell_aux", tags=["account"])
async def MintMft(form_data: REmoveSellAuxForm = Depends()):
    try:
        logger.info("remove_sell_aux api == called")
        if mdb.nft_mint.count({'tokenid' : form_data.tokenid}) > 0 :
            nftData = mdb.nft_mint.find({'tokenid' : form_data.tokenid})
            for i in nftData:
                auxData = mdb.auction_sell.find({'nftid': str(i['_id']) , 'istatus':'CONFIRM'}).sort('_id', -1).limit(1)
                for j in auxData:
                    if mdb.auction_sell.count({'_id': ObjectId(str(j['_id'])) , 'istatus':'CONFIRM'}) > 0:
                        mdb.nft_mint.update_one({ "_id": ObjectId(str(i['_id'])) },{'$set': {'istatus': 'Available'}})
                        mdb.auction_sell.update_one({ "_id": ObjectId(str(j['_id'])) },{'$set': {'istatus': 'REMOVED', 'tranhash':form_data.tranhash}})
                        return {
                            "code": 200,
                            "status": "success",
                            "message": "Nft Remove Successfully"
                        }
        else:
            return {
                "code": 400,
                "status": "error",
                "message": "No data found"
            }
    except Exception as e: 
        logger.exception("Error {} occurred while user mint nft .".format(e))
        return {
            "code": 500,
            "status": "error",
            "message": " Exception {} occurred while user mint nft .".format(e)
        }
