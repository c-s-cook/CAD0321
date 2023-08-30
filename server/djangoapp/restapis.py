import requests
import json
import time
import os
from dotenv import load_dotenv
load_dotenv()

# importing Django models
from .models import CarDealer, DealerReview

# importing IBM Cloud / Watson modules
from requests.auth import HTTPBasicAuth
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1, ApiException
from ibm_watson.natural_language_understanding_v1 import Features,SentimentOptions, KeywordsOptions



#
#   get_request():
#       - reusable method to make HTTP GET requests
#       - e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                         auth=HTTPBasicAuth('apikey', api_key))
#

def get_request(url, **kwargs):
    #print("get_request() kwargs = ", kwargs)
    #print("GET from {} ".format(url))
    
    try:
        if "api_key" in kwargs:
            ###  Basic authentication GET
            print('restapis.py >> within get_request() "if api_key"...')
            response = requests.get(
                url,
                params=kwargs, 
                headers={'Content-Type': 'application/json'}, 
                auth=HTTPBasicAuth('apikey', kwargs["api_key"])
            )
        else:
            ###  no authentication GET
            #print('restapis.py >> within get_request ELSE...')
            response = requests.get(
                url,
                params=kwargs, 
                headers={'Content-Type': 'application/json'}, 
            )
    except:
        # If any error occurs
        print("Network exception occured in get_request()")
        status_code = response.status_code
        print("With status {}".format(status_code))

    json_data = json.loads(response.text)
    return json_data



#
#   post_request():
#       - resuable method to make HTTP POST requests
#       - e.g., response = requests.post(url, params=kwargs, json=payload)
#

def post_request(url, json_payload, **kwargs):

    response = requests.post(url, params=kwargs, json=json_payload)

    return response



# 
#   get_dealers_from_cf():
#       - method to get dealers from a cloud function
#       - calls get_request() with specified arguments
#       - parses JSON results into a CarDealer object list
#

def get_dealers_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url, **kwargs)
    if json_result:
        dealers = json_result["dealerships"]

        for dealer in dealers:
            dealer_doc = dealer["row"]["doc"]
            dealer_obj = CarDealer(
                address = dealer_doc["address"],
                city = dealer_doc["city"],
                full_name = dealer_doc["full_name"],
                id = dealer_doc["id"],
                lat = dealer_doc["lat"],
                long = dealer_doc["long"],
                short_name = dealer_doc["short_name"],
                st = dealer_doc["st"],
                zip = dealer_doc["zip"]
            )
            results.append(dealer_obj)
    
    return results



#
#   get_dealer_by_id():
#

def get_dealer_by_id(url, dealerId):
    results = get_dealers_from_cf(url, dealerId=dealerId)
    
    return results



#
#   get_dealers_by_state():
#

def get_dealers_by_state(url, state):
    ###  "state" needs to be the 2-letter abbr. of the state for the Cloud Function to return values
    results = get_dealers_from_cf(url, state=state)
    
    return results



#
#   get_dealer_by_id_from_cf(dealerId):
#       - method to get reviews by dealer id from a cloud function
#       - calls the get_request() with specified arguments
#       - parses JSON results into a DealerReview object list
#

def get_dealer_reviews_from_cf(dealerId):
    results = []
    get_review_url = os.getenv('GET_REVIEW_API')
    json_result = get_request(get_review_url, dealerId=dealerId)
    if json_result:
        reviews = json_result["data"]["docs"]

        for review_doc in reviews:
            doc = review_doc
            
            if not "purchase_date" in doc.keys():
                doc["purchase_date"] = None
                
            if not "car_make" in doc.keys():
                doc["car_make"] = None

            if not "car_model" in doc.keys():
                doc["car_model"] = None

            if not "car_year" in doc.keys():
                doc["car_year"] = None

            review_obj = DealerReview(
                dealership = doc["dealership"],
                name = doc["name"],
                purchase = doc["purchase"],
                review = doc["review"],
                id = doc["id"],
                purchase_date = doc["purchase_date"],
                car_make = doc["car_make"],
                car_model = doc["car_model"],
                car_year = doc["car_year"],
                sentiment = {}
            )
            
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            # print("sentiment label >>", review_obj.sentiment['label'])
            results.append(review_obj)
            
    
    return results



#
#   analyze_review_sentiments():
#       - method calls Watson NLU instance and analyzes submitted text
#       - Successful call returns sentiment label such as Positive, Neutral, or Negative
#

def analyze_review_sentiments(dealerreview):
    nlu_url = os.getenv('NLU_API')
    nlu_api_key = os.getenv('NLU_KEY')

    authenticator = IAMAuthenticator(nlu_api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-04-07',
        authenticator=authenticator)

    natural_language_understanding.set_service_url(nlu_url)

    try:
        response = natural_language_understanding.analyze(
            text=dealerreview,
            features=Features(
                keywords=KeywordsOptions(emotion=False, sentiment=True,
                                        limit=2))).get_result()
    except ApiException as ex:
        response = ex
        print("analyze_review_sentiments Error >> ", response)
        sentiment = {}
        sentiment["score"] = 0
        sentiment["label"] = "neutral"
        return sentiment

    if ("keywords" in response) & (len(response["keywords"]) > 0):
        #print("response['keywords'] = ", response["keywords"])

        ###  assigns 'sentiment' a <dict> value with keys: 'score': <int>, 'label': <str>
        sentiment = response["keywords"][0]["sentiment"]
                
    else:
        sentiment = {}
        sentiment["score"] = 0
        sentiment["label"] = "neutral"
    
    return sentiment 
