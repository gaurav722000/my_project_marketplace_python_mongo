
from bson import ObjectId
import datetime
from fastapi import Depends
from .route import profile
from shared.db import mdb
import logging
from .forms.updateUserDetailByIdForm import UpdateUserDetailByIdForm
from ..common.common_function import activity_log, error_log

logger = logging.getLogger(__name__)

@profile.put("/profile/update_userdetail", tags=["profile"])
async def UpdateUserDetail(
    form_data: UpdateUserDetailByIdForm = Depends()
):
    try:
        logger.info("user detail update api == called")
        userData = list(mdb.users_list.find({"address": form_data.address, "is_valid":0}))
        if len(userData):
            profile_content = await form_data.profilephoto.read()
            cover_content = await form_data.coverphoto.read()
            store_path = "D:/gaurav/Testing_Project/Python_Fastapi_Test_Project/project1_fastapi/app/app/profile/profile_image/"
            profile_image = store_path + form_data.profilephoto.filename
            cover_image = store_path + form_data.coverphoto.filename
            open(profile_image, 'wb').write(profile_content)
            open(cover_image, 'wb').write(cover_content)

            json = {
                'username' : form_data.username,
                'firstname' : form_data.firstname,
                'description' : form_data.description,
                "address" : form_data.address,
                "is_valid" : 0,
                'ondate' : datetime.datetime.now(),
                "profilephoto" : profile_image,
                "coverphoto" : cover_image,
            }

            if mdb.users_list.count({"username": form_data.username, "is_valid":0}) == 0:
                mdb.users_list.update_one({ "address": form_data.address },{'$set': json})
                logger.info("user detail update successfully")
                return {
                    "code": 200,
                    "status": "success",
                    "message": "Updated Successfully"
                }
            else:
                logger.error("username all ready exist")
                return {
                    "code": 404,
                    "status": "error",
                    "message": "Username all ready exist"
                }
        else:
            logger.error("user detail not update")
            return {
                "code": 404,
                "status": "error",
                "message": "No Data Available"
            }

        # profile_content = await form_data.profilephoto.read()
        # cover_content = await form_data.coverphoto.read()
        # store_path = "D:/gaurav/Testing_Project/Python_Fastapi_Test_Project/project1_fastapi/app/app/profile/profile_image/"
        # profile_image = store_path + form_data.profilephoto.filename
        # cover_image = store_path + form_data.coverphoto.filename
        # open(profile_image, 'wb').write(profile_content)
        # open(cover_image, 'wb').write(cover_content)
        #
        # json = {
        #     'username': form_data.username,
        #     'firstname': form_data.firstname,
        #     'description': form_data.description,
        #     "address": form_data.address,
        #     "is_valid": 0,
        #     'ondate': datetime.datetime.now(),
        #     "profilephoto": profile_image,
        #     "coverphoto": cover_image,
        # }
        #
        # if mdb.users_list.count({"username": form_data.username, "is_valid": 0}) == 0:
        #     mdb.users_list.update_one({"address": form_data.address}, {'$set': json})
        #     logger.info("user detail update successfully")
        #     return {
        #         "code": 200,
        #         "status": "success",
        #         "message": "Updated Successfully"
        #     }
        # else:
        #     logger.error("username all ready exist")
        #     return {
        #         "code": 404,
        #         "status": "error",
        #         "message": "Username all ready exist"
        #     }

    except Exception as e:
            logger.exception("Error {} occurred while user detail update .".format(e))
            return {
                "code": 500,
                "status": "error",
                "message": " Exception {} occurred while user detail update .".format(e)
            }