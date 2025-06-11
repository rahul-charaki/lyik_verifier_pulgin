import apluggy as pluggy
from lyikpluginmanager import getProjectName, VerifyHandlerSpec, VerifyHandlerResponseModel, VERIFY_RESPONSE_STATUS, ContextModel
from lyikpluginmanager.annotation import RequiredEnv
import logging
from ..model.jobapplicationform import RootPersonalInfoPerInfoCard

logger = logging.getLogger(__name__)

impl = pluggy.HookimplMarker(getProjectName())

class UserVerification(VerifyHandlerSpec):
    @impl
    async def verify_handler(self, context:ContextModel, payload:RootPersonalInfoPerInfoCard) -> VerifyHandlerResponseModel:
        """
        Verify user details such as name and email.
        """
        if payload.first_name and payload.email:
            return VerifyHandlerResponseModel(
                status=VERIFY_RESPONSE_STATUS.SUCCESS,
                message="User verification successful",
                data={"name": payload.first_name, "email": payload.email},
            )
        else:
            return VerifyHandlerResponseModel(
                status=VERIFY_RESPONSE_STATUS.FAILURE,
                message="User verification failed: Name or Email is missing",
            )
        