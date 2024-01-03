"""IBM Cloud Function that gets all reviews for a dealership

Returns:
    List: List of reviews for the given dealership
"""
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import requests


def main(param_dict):
    """Main Function

    Args:
        param_dict (Dict): input paramater

    Returns:
        _type_: _description_ TODO
    """

    try:
        authenticator = IAMAuthenticator(param_dict["IAM_API_KEY"])
        service = CloudantV1(authenticator=authenticator)
        service.set_service_url(param_dict["COUCH_URL"])

    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": "Something went wrong on the server"}

    response = service.put_document(
      db='reviews',
      doc_id=param_dict['review']['id'],
      document=param_dict['review']
    ).get_result()

    return {"body": response}

