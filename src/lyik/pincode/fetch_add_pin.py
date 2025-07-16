import apluggy as pluggy
from lyikpluginmanager import getProjectName, VerifyHandlerSpec, VerifyHandlerResponseModel, VERIFY_RESPONSE_STATUS, ContextModel
from ..model.partneronboardapplicationform import RootCenterInfo
import requests
import logging

logger = logging.getLogger(__name__)
impl = pluggy.HookimplMarker(getProjectName())

def fetch_pincode_info(pincode: int):
    """
    Validates and fetches city, district, state for a given Indian PIN code.
    Returns dict or None if invalid.
    """
    if not isinstance(pincode, int) or len(str(pincode)) != 6:
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
            "city": cities, "state": state, "region": district, "pincode": pincode
        }

    except Exception as e:
        logger.error(f"Exception during pincode validation: {e}")
        return None

class PincodeVerification(VerifyHandlerSpec):
    @impl
    async def verify_handler(self, context: ContextModel, payload: RootCenterInfo) -> VerifyHandlerResponseModel:
        try:
            pincode_int = int(payload.pincode)
        except (ValueError, TypeError):
            return VerifyHandlerResponseModel(
            status=VERIFY_RESPONSE_STATUS.FAILURE,
            message="Pincode must be a 6-digit number"
            )
        info = fetch_pincode_info(pincode_int)

        if info:
            # Add address fields from payload to the response
            info.update({
            "address_line_1": getattr(payload, "address_line_1", None),
            "address_line_2": getattr(payload, "address_line_2", None),
            "address_line_3": getattr(payload, "address_line_3", None),
            "landmark": getattr(payload, "landmark", None),
            })
            return VerifyHandlerResponseModel(
            status=VERIFY_RESPONSE_STATUS.SUCCESS,
            message="Pincode verification successful",
            response=info
            )
        else:
            return VerifyHandlerResponseModel(
                status=VERIFY_RESPONSE_STATUS.FAILURE,
                message="Invalid or non-existent pincode"
            )
