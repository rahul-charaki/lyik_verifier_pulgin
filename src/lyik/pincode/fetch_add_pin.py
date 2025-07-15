import apluggy as pluggy
from lyikpluginmanager import getProjectName, VerifyHandlerSpec, VerifyHandlerResponseModel, VERIFY_RESPONSE_STATUS, ContextModel
from ..model.partneronboardapplicationform import RootCenterInfoPartnerAddressProof
import requests
import logging

logger = logging.getLogger(__name__)
impl = pluggy.HookimplMarker(getProjectName())

def fetch_pincode_info(pincode: str):
    """
    Validates and fetches city, district, state for a given Indian PIN code.
    Returns dict or None if invalid.
    """
    if not pincode.isdigit() or len(pincode) != 6:
        return {"message": "Invalid pincode format"}

    try:
        url = f"https://api.postalpincode.in/pincode/{pincode}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)

        if response.status_code != 200:
            return None

        data = response.json()
        post_offices = data[0].get("PostOffice", [])

        if data[0]["Status"] != "Success" or not post_offices:
            return None

        # Extract values from first post office
        first = post_offices[0]
        state = first.get("State")
        district = first.get("District")
        cities = first.get("Division")

        return {
            "state": state,
            "district": district,
            "cities": cities
        }

    except Exception as e:
        logger.error(f"Exception during pincode validation: {e}")
        return None

class PincodeVerification(VerifyHandlerSpec):
    @impl
    async def verify_handler(self, context: ContextModel, payload: RootCenterInfoPartnerAddressProof) -> VerifyHandlerResponseModel:
        info = fetch_pincode_info(payload.pincode)

        if info:
            return VerifyHandlerResponseModel(
                status=VERIFY_RESPONSE_STATUS.SUCCESS,
                message="Pincode verification successful",
                data=info
            )
        else:
            return VerifyHandlerResponseModel(
                status=VERIFY_RESPONSE_STATUS.FAILURE,
                message="Invalid or non-existent pincode"
            )
