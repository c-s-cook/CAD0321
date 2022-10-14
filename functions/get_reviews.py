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




    # reviews = []
        
    ### FOR loop to filter 'response' down to be only those reviews with the submitted 'dealerId'
    ###     >>> Requires a k:v param of 'dealerId' to have been passed with GET, or attached in testing
    ###
    ### !!! Currently throwing errors and stopping :
    ###         KeyError: 'dealership'
    ###
    ###
    ### Testing to confirm access & key names
    # keys = list(response["rows"][0]["doc"].keys())
    # print(keys)
    ###
    ### >>> Sucessfully returns keys and confirms 'dealership' key
    ###
    ###
    ### Testing to confirm access to "dealership" and its Type
    #print("['dealership'] = ", response["rows"][5]["doc"]["dealership"])
    #print("['dealership'] type is: ", type(response["rows"][5]["doc"]["dealership"]))
    ###
    ### >>> Sucessfully returns an Int & confirms type of int
    ###
    ###
    ### var for shortened testing /within/ FOR Loop...
    # i = 0
    
    # for row in response["rows"]:
    
        ### ...Testing access to variables:
        ###     > row["doc"]["dealership"]
        ###     > dict['dealerId']
        # if i < 3: 
        #     print("row['doc']['dealership'] is:", row["doc"]["dealership"], " and dict['dealerId'] is: ", dict["dealerId"])
        # i += 1
        ###
        ### >>> Successfully accesses / prints out the values of both variable without throwing any errors...so, WTF?
        
    #    if row["doc"]["dealership"] == dict['dealerId']:
    #        reviews.append(row["doc"])
    #    reviews.append(row["doc"])



    # reviews_json = json.dumps(reviews)    

'''        
    return {
        "reviews": reviews_json
    }
'''