#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
import sys
from ibmcloudant.cloudant_v1 import CloudantV1, Document
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core import ApiException
from requests import RequestException
import json



def main(dict):
    
    authenticator = IAMAuthenticator(dict["CLOUDANT_API_KEY"])
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(dict["CLOUDANT_URL"])
    
    
    review_doc = Document(
        ID=dict["id"],
        name=dict["name"],
        dealership=dict["dealership"],
        review=dict["review"],
        purchase=dict["purchase"],
        another=dict["another"],
        purchase_date=dict["purchase_date"],
        car_make=dict["car_make"],
        car_model=dict["car_model"],
        car_year=dict["car_year"]
        )

    
    try:
        review = service.post_document(
              db='reviews',
              document=review_doc
            ).get_result()
            
    except ApiException as ae:
        return { "API Error": json.dumps(ae.message) }
        
    except RequestException as err:
        return { "Request Error2": err }
    

    return {"review":review}