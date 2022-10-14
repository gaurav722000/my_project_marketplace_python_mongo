from bson import ObjectId
from fastapi.responses import Response, FileResponse, JSONResponse
import datetime
import logging
from fastapi import Depends
from .route import profile
from shared.db import mdb
from ..common.common_function import activity_log, error_log
import base64

logger = logging.getLogger(__name__)

@profile.post("/profile/alluserlist", tags=["profile"])
async def AllUerList():
    try:
        logger.info("alluserlist api == called")
        user_detail = []
        userData = list(mdb.users_list.find({"is_valid" : 0}))
        print("userData", len(userData))
        for x in userData:
            with open(x['profilephoto'], "rb") as profileimg_file:
                profileResponse = base64.b64encode(profileimg_file.read())
            with open(x['coverphoto'], "rb") as coverimg_file:
                coverResponse = base64.b64encode(coverimg_file.read())

            user_detail.append({
                'id': str(x['_id']),
                'username' : x['username'],
                'firstname': x['firstname'],
                'lastname': x['lastname'],
                'description': x['description'],
                'address' : x['address'],
                'ondate': x['ondate'],
                'profilephoto' : profileResponse,
                'coverphoto' : coverResponse,
            })
        logger.info("alluserlist api successfully")
        return {
            "code": 200,
            "status": "success",
            "data": user_detail
        }
    except Exception as e:
        logger.exception("Error {} occurred while get user detail .".format(e))
        return {
            "code": 500,
            "status": "error",
            "message": " Exception {} occurred while get user detail .".format(e)
        }
