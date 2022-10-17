import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

load_dotenv()


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))


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



# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list


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

def get_dealer_by_id(url, dealerId):
    results = get_dealers_from_cf(url, dealerId=dealerId)
    
    return results

def get_dealers_by_state(url, state):
    ## "state" needs to be the 2-letter abbr. of the state for the CFunct to return values
    results = get_dealers_from_cf(url, state=state)
    
    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerReview object list

def get_dealer_reviews_from_cf(dealerId):
    results = []
    get_review_url = os.getenv('get_review_url')
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
                sentiment = None
            )
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)
            
    
    return results




# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative

def analyze_review_sentiments(dealerreview):
    nlu_url = os.getenv('nlu_url')
    nlu_api_key = os.getenv('nlu_api_key')

    params = dict()
    params["text"] = dealerreview
    params["version"] = "2022-04-07"
    params["features"] = "sentiment"
    params["return_analyzed_text"] = False


    try:
        response = requests.get(
                    nlu_url,
                    params=params,
                    headers={
                        'Content-Type': 'application/json', 
                        #'apikey': api_key
                        },
                    auth=HTTPBasicAuth('apikey', nlu_api_key)
                    )
    except:
        # If any error occurs
        print("Network exception occured in get_request()")
        status_code = response.status_code
        print("With status {}".format(status_code))

    results = json.loads(response.text)
    print("results = ", results)


    if "keywords" in results:
        sentiment = results["keywords"]["sentiment"]["score"]
        print('sentiment = ', sentiment)
    else:
        sentiment = None
    
    return sentiment 




