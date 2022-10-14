from bson import ObjectId
from fastapi.responses import Response, FileResponse, JSONResponse
import datetime
import logging
from fastapi import Depends
from .route import account
from shared.db import mdb
from ..common.common_function import activity_log, error_log
import base64
from .forms.GetTokenDetailByTokenId_From import GetTokenDetailByIdForm

logger = logging.getLogger(__name__)

@account.post("/account/get_nft_detail_by_tokenid", tags=["account"])
async def GetNftDetailByTokenId(form_data : GetTokenDetailByIdForm = Depends()):
    try:
        logger.info("get_nft_detail_by_tokenid api == called")
        nftData = list(mdb.nft_mint.find({"tokenid": form_data.tokenid, "is_valid":0}))
        bidData = mdb.tbl_nftbid.find({'tokenid': form_data.tokenid})
        auxData = mdb.auction_sell.find({'tokenid': form_data.tokenid , 'istatus':'CONFIRM'})

        if len(nftData):
            nft_detail = []
            bidDatalist = []
            auxDatalist = []
            for a in bidData:
                userData = mdb.users_list.find({'address': a['address'], "is_valid": 0})
                for b in userData:
                    with open(b['profilephoto'], "rb") as profileimg_file:
                        profileimage = base64.b64encode(profileimg_file.read())
                    bidDatalist.append({
                        "bidprofilepic":profileimage,
                        "username" : b['username'],
                        "bidprice" : a['bidprice'],
                        "bidtranhash" : a['tranhash'],
                        "bidondate" : a['ondate'],
                        # "userdata": b,
                        # "biddatalist" : a
                    })
            for b in auxData:
                auxDatalist.append({
                    'auxid': str(b['_id']),
                    'auxselltype': b['type'],
                    'auxprice': b['price'],
                    'auxstartdate': b['startdate'],
                    'auxenddate': b['enddate'],
                    'auxtokenid': b['tokenid'],
                    'auxlastprice': b['lastprice']
                })
            for i in nftData:
                userData = mdb.users_list.find({'address' : i['account'] , "is_valid":0 })
                for j in userData:
                    with open(j['profilephoto'], "rb") as profileimg_file:
                        profileimage = base64.b64encode(profileimg_file.read())
                    nft_detail.append({
                        'id' : str(i['_id']),
                        'name' : i['name'],
                        'description': i['description'],
                        'tranhash' : i['tranhash'],
                        'tokenid': i['tokenid'],
                        'type': i['type'],
                        'account': i['account'],
                        'mintfile': i['ipfsid'],
                        'thumbnil': i['thumbnil'],
                        'mintauxtype': i['auxtype'],
                        'is_valid': i['is_valid'],
                        'ondate': i['ondate'],
                        'username' : j['username'],
                        'auxData' : auxDatalist,
                        "bidData": bidDatalist,
                        'profilephoto': profileimage,
                    })
            logger.info("get_nft_detail_by_tokenid api == get successfully")
            return {
                "code": 200,
                "status": "success",
                "data": nft_detail
            }
        else:
            # error_log('', "UserDetailById", '', "No Data Available For User Detail Id")
            logger.error("get_nft_detail_by_tokenid not found")
            return {
                "code": 404,
                "status": "error",
                "message": "No Data Found"
            } 
    except Exception as e:
        logger.exception("Error {} occurred while get detail by tokenid .".format(e))
        return {
            "code": 500,
            "status": "error",
            "message": " Exception {} occurred while get detail by tokenid .".format(e)
        }
