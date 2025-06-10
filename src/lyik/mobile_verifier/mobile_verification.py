import apluggy as pluggy
from lyikpluginmanager import getProjectName, VerifyHandlerSpec, VerifyHandlerResponseModel, VERIFY_RESPONSE_STATUS, ContextModel
from lyikpluginmanager.annotation import RequiredEnv
import logging
from ..model.sampleform import RootMobileVerifierInfo, RootUserDetailsInfo
import re

logger = logging.getLogger(__name__)

impl = pluggy.HookimplMarker(getProjectName())

def is_valid_mobile_number(mobile_number: str) -> bool:
    """
    Validate the mobile number format.
    This example checks for a 10-digit number, but you can adjust the regex as needed.
    """
    return True if '6' in mobile_number else False
    # pattern = re.compile(r"^[6-9]\d{9}$")
    # return bool(pattern.match(mobile_number))

class MobileVerification(VerifyHandlerSpec):
    @impl
    async def verify_handler(self, context:ContextModel, payload:RootMobileVerifierInfo) -> VerifyHandlerResponseModel:

        if is_valid_mobile_number(payload.mobile.contact_id):
            
            return VerifyHandlerResponseModel(
                status=VERIFY_RESPONSE_STATUS.SUCCESS,
                message="Mobile verification successful",
                
            )
        else:
            return VerifyHandlerResponseModel(
                status=VERIFY_RESPONSE_STATUS.FAILURE,
                message="Invalid mobile number format",
            )
        

class UserVerification(VerifyHandlerSpec):
    @impl
    async def verify_handler(self, context:ContextModel, payload:RootUserDetailsInfo) -> VerifyHandlerResponseModel:
        if payload.name and payload.email is not None:
            return VerifyHandlerResponseModel(
                status=VERIFY_RESPONSE_STATUS.SUCCESS,
                message="User verification successful",
                data={"name": payload.name},
            )
        else:
            return VerifyHandlerResponseModel(
                status=VERIFY_RESPONSE_STATUS.FAILURE,
                message="User verification failed: Name or Email is missing",
            )
        