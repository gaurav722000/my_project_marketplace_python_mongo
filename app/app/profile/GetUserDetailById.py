
# from bson import ObjectId
# from fastapi.responses import Response, FileResponse, JSONResponse
# import datetime
# from fastapi import Depends
# from .route import profile
# from shared.db import mdb
# from ..common.common_function import activity_log, error_log
# import base64

# @profile.get("/profile/get_userdetail")
# async def GetUserDataById(id):
#     try:
#         userData = list(mdb.users_list.find({"_id": ObjectId(id), "is_valid":0}))
#         if len(userData):
#             user_detail = []
#             for i in userData:
#                 with open(i['profilephoto'], "rb") as profileimg_file:
#                     profileResponse = base64.b64encode(profileimg_file.read())
#                 with open(i['coverphoto'], "rb") as coverimg_file:
#                     coverResponse = base64.b64encode(coverimg_file.read())

#                 user_detail.append({
#                     '_id': str(i['_id']),
#                     'username' : i['username'],
#                     'firstname': i['firstname'],
#                     'description': i['description'],
#                     'profilephoto' : profileResponse,
#                     'coverphoto' : coverResponse,
#                     'ondate': i['ondate']
#                 })
#             # activity_log('', "UserDetailGetById", '', "Get user detail data by id")
#             return {
#                 "code": 200,
#                 "status": "success",
#                 "data": user_detail
#             }
#         else:
#             # error_log('', "UserDetailById", '', "No Data Available For User Detail Id")
#             return {
#                 "code": 404,
#                 "status": "error",
#                 "message": "No Data Available"
#             } 
#     except Exception as e:
#         return {
#             "code": 500,
#             "status": "error",
#             "message": " Exception {} occurred while user get detail .".format(e)
#         }




from bson import ObjectId
from fastapi.responses import Response, FileResponse, JSONResponse
import datetime
import logging
from fastapi import Depends
from .route import profile
from shared.db import mdb
from ..common.common_function import activity_log, error_log
import base64
from .forms.get_userdetail_form import GetUserDetailForm

logger = logging.getLogger(__name__)

@profile.post("/profile/get_userdetail", tags=["profile"])
async def GetUserDataById(form_data: GetUserDetailForm = Depends()):
    try:
        logger.info("get_userdetail api == called")
        userData = list(mdb.users_list.find({"address": form_data.address, "is_valid":0}))
        if len(userData):
            user_detail = []
            for i in userData:
                with open(i['profilephoto'], "rb") as profileimg_file:
                    profileResponse = base64.b64encode(profileimg_file.read())
                with open(i['coverphoto'], "rb") as coverimg_file:
                    coverResponse = base64.b64encode(coverimg_file.read())

                user_detail.append({
                    '_id': str(i['_id']),
                    'username' : i['username'],
                    'firstname': i['firstname'],
                    'lastname': i['lastname'],
                    'description': i['description'],
                    'address' : i['address'],
                    'ondate': i['ondate'],
                    'profilephoto' : profileResponse,
                    'coverphoto' : coverResponse, 
                })
            # activity_log('', "UserDetailGetById", '', "Get user detail data by id")
            logger.info("get_userdetail api successfully")
            return {
                "code": 200,
                "status": "success",
                "data": user_detail
            }
        else:
            # error_log('', "UserDetailById", '', "No Data Available For User Detail Id")
            logger.error("get user detail not found")
            return {
                "data": [],
                "code": 'ND',
                # "status": "error",
                # "message": "No Data Found"
            } 
    except Exception as e:
        logger.exception("Error {} occurred while get user detail .".format(e))
        return {
            "code": 500,
            "status": "error",
            "message": " Exception {} occurred while get user detail .".format(e)
        }
