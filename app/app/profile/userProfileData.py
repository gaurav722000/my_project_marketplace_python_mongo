from bson import ObjectId
from fastapi.responses import Response, FileResponse, JSONResponse
import datetime
import logging
from fastapi import Depends
from .route import profile
from shared.db import mdb
from ..common.common_function import activity_log, error_log
import base64
from .forms.userProfileDataForm import UserProfileDataForm

logger = logging.getLogger(__name__)

@profile.post("/profile/user_profile_data", tags=["profile"])
async def userProfileData(form_data: UserProfileDataForm = Depends()):
    try:
        logger.info("user_profile_date api == called")
        createdMint = mdb.nft_mint.find({"buyerid": form_data.address, 'istatus':'Available'})

        auctionData = list(mdb.auction_sell.find({"buyerid": form_data.address, 'istatus':'CONFIRM', 'type':'aux'}))
        
        sellData = list(mdb.auction_sell.find({"buyerid": form_data.address, 'istatus':'CONFIRM', 'type':'sell'}))
        mainData = []
        owned_detail = []
        onauction = []
        onsell = []

        for i in createdMint:
            owned_detail.append({
                "thumbnil": i['thumbnil'],
                "ipfsid": i['ipfsid'],
                "name": i['name'],
                "description": i['description'],
                "tranhash": i['tranhash'],
                "tokenid": i['tokenid'],
                "type": i['type'],
                "account": i['account'],
                "auxtype": i['auxtype'],
                "ipfsimgcid": i['ipfsimgcid']
            })
        for j in auctionData:
            mintDataAux = mdb.nft_mint.find({"buyerid": form_data.address,'istatus':'aux'})
            for k in mintDataAux:
                if k['tokenid'] == j['tokenid']:
                    onauction.append(({
                        "_id": str(j['_id']),
                        "ipfsid": k['ipfsid'],
                        "ipfsimgcid": k['ipfsimgcid'],
                        "name": k['name'],
                        "nftid": j['nftid'],
                        "tranhash": j['tranhash'],
                        "type": j['type'],                
                        "price": j['price'],
                        "startdate": j['startdate'],
                        "enddate": j['enddate'],
                        "tokenid": j['tokenid'],
                        "address": j['address'],
                        "lastprice": j['lastprice'],
                        "istatus": j['istatus'],
                    }))
        for a in sellData:
            mintDataSell = mdb.nft_mint.find({"buyerid": form_data.address,'istatus':'sell'})
            for b in mintDataSell:
                if b['tokenid'] == a['tokenid']:
                    onsell.append(({
                        "_id": str(a['_id']),
                        "ipfsid": b['ipfsid'],
                        "ipfsimgcid": b['ipfsimgcid'],
                        "name" : b['name'],
                        "nftid": a['nftid'],
                        "tranhash": a['tranhash'],
                        "type": a['type'],                
                        "price": a['price'],
                        "startdate": a['startdate'],
                        "enddate": a['enddate'],
                        "tokenid": a['tokenid'],
                        "address": a['address'],
                        "lastprice": a['lastprice'],
                        "istatus": a['istatus'],
                    }))

        mainData.append({
            "owned": owned_detail,
            "onauction" : onauction,
            "onsell" : onsell
        })
        logger.info("user_profile_date api successfully")
        return {
            "code": 200,
            "status": "success",
            "data": mainData
        }
    except Exception as e:
        logger.exception("Error {} occurred while user_profile_date .".format(e))
        return {
            "code": 500,
            "status": "error",
            "message": " Exception {} occurred while user_profile_date .".format(e)
        }
