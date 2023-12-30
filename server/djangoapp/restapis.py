import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 \
    import Features, SentimentOptions, EntitiesOptions, KeywordsOptions


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
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
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        # dealers = json_result["rows"]
        # For each dealer object
        for dealer in json_result:
            # Get its content in `doc` object
            # dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)
    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf (url, dealerId):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, **{  'dealerid': dealerId })
    if json_result:
        # Get the row list in JSON as dealers
        # dealers = json_result["rows"]
        # For each dealer object
        for review in json_result:
            # Get its content in `doc` object
            # dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            review_obj = DealerReview(dealership=review['dealership'], name=review['name'], review=review['review'], purchase_date=review.get('purchase_date', None),car_make=review.get('car_make', None),car_model=review.get('car_model', None),car_year=review.get('car_year', None),sentiment=None,review_id=review['id'],purchase=review['purchase'])
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
    try:
        print(text)
        url = 'https://api.eu-de.natural-language-understanding.watson.cloud.ibm.com/instances/27a51923-fa50-4640-8da0-4514410fd13e'
        authenticator = IAMAuthenticator('Jbc6N_Dc8fGHqItUlsoFfPneUH7y3Pb8louc3aXK6ydk')
        natural_language_understanding = NaturalLanguageUnderstandingV1(
            version='2022-04-07',
            authenticator=authenticator
        )
        natural_language_understanding.set_service_url(url)
        response = natural_language_understanding.analyze(
            text=text,
            features=Features(
                entities=EntitiesOptions(emotion=True, sentiment=True, limit=2),
                keywords=KeywordsOptions(emotion=True, sentiment=True,
                                    limit=2))).get_result()
        return response['keywords'][0]['sentiment']['label']
    except:
        # If any error occurs
        print("An error occured while trying to get the NLU response")
        return 'neutral'
    
         


