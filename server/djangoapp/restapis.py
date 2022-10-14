import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))


def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
    except:
        # If any error occurs
        print("Network exception occured")
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

def get_dealer_reviews_from_cf(url, dealerId=dealer_id):
    results = []
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        reviews = json_result["docs"]

        for review_doc in reviews:
            doc = review_doc
            review_obj = DealerReview(
                dealership = doc["dealership"],
                name = doc["name"],
                purcahse = doc["purchase"],
                review = doc["review"],
                purchase_date = doc["purchase_date"],
                car_make = doc["car_make"],
                car_model = doc["car_model"],
                car_year = doc["car_year"],
                id = doc["id"]
            )
            results.append(review_obj)
    
    return results




# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



