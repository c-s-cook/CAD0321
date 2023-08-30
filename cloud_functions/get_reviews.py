#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
# requires a 'dealerId' int param to be submitted
#
#
import sys
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core import ApiException
from requests import RequestException
#import json



def main(dict):
    
    authenticator = IAMAuthenticator(dict["CLOUDANT_API_KEY"])
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(dict["CLOUDANT_URL"])
        
    try:
        # response1 = service.post_all_docs(
        #      db='reviews',
        #      include_docs=True
        #    ).get_result()

        response = service.post_find(
                db='reviews',
                selector={'dealership': {'$eq': int(dict['dealerId'])}},
            ).get_result()
        
        result= {
            'headers': {'Content-Type':'application/json'}, 
            'body': {'data':response} 
            }
        return result

    except ApiException as ae:
        return { "error": ae.messsage }
    except RequestException as err:
        return { "error": err }
