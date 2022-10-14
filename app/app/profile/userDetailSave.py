import datetime
from bson import ObjectId
import re
import random
import string
import logging
from fastapi import Depends
from shared.db import mdb
from .route import profile
from .forms.userDetailSave_from import UserDetailSaveForm
from ..common.common_function import activity_log, error_log

logger = logging.getLogger(__name__)

@profile.post("/profile/userdetail_save", tags=["profile"])
async def UserDetailSave(form_data: UserDetailSaveForm = Depends()):
    try:
        logger.info("user detail save api == called")
        profile_content = await form_data.profilephoto.read()
        cover_content = await form_data.coverphoto.read()
        store_path = "D:/gaurav/Personal/market_place_project1/backend_market_place_project1/app/app/profile/profile_image/"
        profile_image = store_path + form_data.profilephoto.filename
        cover_image = store_path + form_data.coverphoto.filename
        open(profile_image, 'wb').write(profile_content)
        open(cover_image, 'wb').write(cover_content)

        json = {
            "username" : form_data.username,
            "firstname" : form_data.firstname,
            "lastname" : form_data.lastname,
            "description" : form_data.description,
            "profilephoto" : profile_image,
            "coverphoto" : cover_image,
            "address" : form_data.address,
            "is_valid" : 0,
            "ondate": datetime.datetime.now()
        }

        if mdb.users_list.count({"username": form_data.username, "address": form_data.address, "is_valid":0}) == 0:
            mdb.users_list.insert_one(json)
            userData = mdb.users_list.find()
            # activity_log(userData[0]['_id'], "userDetailSave", json, "user detail save successfully")
            logger.info("user detail save successfully")
            return {
                "code": 200,
                "status": "success",
                "userId": str(ObjectId(userData[0]['_id'])),
                "message": "User Detail Save successfully"
            }
        else:
            # error_log('', "user detail save", json, "username all ready exist")
            logger.error("user detail not found")
            return {
                "code": 404,
                "status": "error",
                "message": "Username all ready exist"
            } 
    except Exception as e: 
        logger.exception("Error {} occurred while user detail save .".format(e))
        return {
            "code": 500,
            "status": "error",
            "message": " Exception {} occurred while user detail save .".format(e)
        }
