from bson import ObjectId
from fastapi.responses import Response, FileResponse, JSONResponse
import datetime
import logging
from fastapi import Depends
from .route import profile
from shared.db import mdb
from ..common.common_function import activity_log, error_log
import base64
from .forms.userDetail_by_usernameForm import GetUserDetailByUserNameForm

logger = logging.getLogger(__name__)

@profile.post("/profile/get_userDetail_by_username", tags=["profile"])
async def userProfileDataByUserName(form_data: GetUserDetailByUserNameForm = Depends()):
    try:
        logger.info("get_userDetail_by_username api == called")
        mainData = []
        owned_detail = []
        onauction = []
        onsell = []
        userDetailData = []
        userData = list(mdb.users_list.find({'username' : form_data.username}))
        if len(userData):
            for i in userData:
                userDetail = mdb.users_list.find({'username' : form_data.username, 'is_valid':0})
                createdMint = mdb.nft_mint.find({"buyerid": i['address'], 'istatus':'Available'})

                auctionData = list(mdb.auction_sell.find({"buyerid": i['address'], 'istatus':'CONFIRM', 'type':'aux'}))
                mintDataAux = mdb.nft_mint.find({"buyerid": i['address'],'istatus':'aux'})
                
                sellData = list(mdb.auction_sell.find({"buyerid": i['address'], 'istatus':'CONFIRM', 'type':'sell'}))
                mintDataSell = mdb.nft_mint.find({"buyerid": i['address'],'istatus':'sell'})          

                for x in userDetail:
                    with open(x['profilephoto'], "rb") as profileimg_file:
                        profileResponse = base64.b64encode(profileimg_file.read())
                    with open(x['coverphoto'], "rb") as coverimg_file:
                        coverResponse = base64.b64encode(coverimg_file.read())
                    userDetailData.append({
                        "_id" : str(x['_id']),
                        "username" : x['username'],
                        "firstname" : x['firstname'],
                        "lastname" : x['lastname'],
                        "description" : x['description'],
                        "address" : x['address'],
                        "is_valid" : x['is_valid'],
                        "ondate" : x['ondate'],
                        "profilephoto" : profileResponse,
                        "coverphoto" : coverResponse,
                    })
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
                    for k in mintDataAux:
                        onauction.append(({
                            "_id": str(j['_id']),
                            "ipfsid": k['ipfsid'],
                            "ipfsimgcid": k['ipfsimgcid'],
                            "name" : k['name'],
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
                    for b in mintDataSell:
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
                    "userDetail": userDetailData,
                    "owned": owned_detail,
                    "onauction" : onauction,
                    "onsell" : onsell
                })
                logger.info("get_userDetail_by_username api successfully")
                return {
                    "code": 200,
                    "status": "success",
                    "data": mainData
                }
        else:
            return {
                    "code": 200,
                    "status": "success",
                    "data": []
                }
    except Exception as e:
        logger.exception("Error {} occurred while get_userDetail_by_username .".format(e))
        return {
            "code": 500,
            "status": "error",
            "message": " Exception {} occurred while get_userDetail_by_username .".format(e)
        }
