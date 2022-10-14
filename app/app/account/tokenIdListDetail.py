
import logging
from shared.db import mdb
from .route import account
from .forms.tokenIdListDetailForm import tokenIdListDetailForm
from fastapi import File, UploadFile, Depends
import base64
import time

logger = logging.getLogger(__name__)

@account.post("/account/tokenidListDetail")
async def tokenidListDetail(form_data : tokenIdListDetailForm = Depends()):
    try:
        logger.info("tokenidListDetail api == called")
        listconvert = form_data.tokenidList.split(",")
        auxlist = []
        selllist = []
        mainData = []
        convertint = [int(x) for x in listconvert]
        ts = time.time()
        for i in convertint:
            mintData = mdb.nft_mint.find({ 'tokenid' : i })
            auxData = mdb.auction_sell.find({ 'tokenid' : i ,'type':'aux', 'istatus':'CONFIRM', 'enddate':{'$gt': str(ts)}, 'startdate' : {'$lt': str(ts)}})

            sellData = mdb.auction_sell.find({'tokenid' : i, 'type':'sell', 'istatus':'CONFIRM'})

            for j in mintData:
                for k in auxData:
                    if k['nftid'] == str(j['_id']):
                        userData = mdb.users_list.find({'address' : k['address']})
                        for l in userData:
                            if l['address'] == k['buyerid'] :
                                with open(l['profilephoto'], "rb") as profileimg_file:
                                    profileimage = base64.b64encode(profileimg_file.read())
                                auxlist.append({
                                    "username" : l['username'],
                                    "profilephoto" : profileimage,
                                    "mintid" : str(j['_id']),
                                    "thumbnil" : j['thumbnil'],
                                    "ipfsid": j['ipfsid'],
                                    "ipfsimgcid": j['ipfsimgcid'],
                                    "name": j['name'],
                                    "description": j['description'],
                                    "minttranhash": j['tranhash'],
                                    "tokenid": j['tokenid'],
                                    "type": j['type'],
                                    "account": j['account'],
                                    "mintauxtype": j['auxtype'],
                                    "auxid" : k['nftid'],
                                    "auxtranhash" : k['tranhash'],
                                    "auxselltype" : k['type'],
                                    "auxprice": k['price'],
                                    "auxstartdate": k['startdate'],
                                    "auxenddate": k['enddate'],
                                    "auxtokenid": k['tokenid'],
                                    "auxaddress" : k['address'],
                                    "auxlastprice" : k['lastprice'],
                                })

                for a in sellData:
                    if a['nftid'] == str(j['_id']):
                        userData = mdb.users_list.find({'address' : a['buyerid']})
                        for l in userData:
                            with open(l['profilephoto'], "rb") as profileimg_file:
                                profileimage = base64.b64encode(profileimg_file.read())
                            selllist.append({
                                "username" : l['username'],
                                "profilephoto" : profileimage,
                                "mintid" : str(j['_id']),
                                "thumbnil" : j['thumbnil'],
                                "ipfsid": j['ipfsid'],
                                "ipfsimgcid": j['ipfsimgcid'],
                                "name": j['name'],
                                "description": j['description'],
                                "minttranhash": j['tranhash'],
                                "tokenid": j['tokenid'],
                                "type": j['type'],
                                "account": j['account'],
                                "mintauxtype": j['auxtype'],
                                "auxid" : a['nftid'],
                                "auxtranhash" : a['tranhash'],
                                "auxselltype" : a['type'],
                                "auxprice": a['price'],
                                "auxstartdate": a['startdate'],
                                "auxenddate": a['enddate'],
                                "auxtokenid": a['tokenid'],
                                "auxaddress" : a['address'],
                                "auxlastprice" : a['lastprice'],
                            })

        mainData.append({
            "AuxData" : auxlist,
            "SellData" : selllist
        })
        logger.info("tokenidListDetail == get successfully")
        return {
            "code": 200,
            "status": "success",
            "data": mainData
        }

    except Exception as e:
        logger.exception("Error {} occurred while user mint nft .".format(e))
        return {
            "code": 500,
            "status": "error",
            "message": " Exception {} occurred while user mint nft .".format(e)
        }
