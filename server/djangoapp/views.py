from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect

from .models import CarModel, CarMake
from .restapis import get_dealers_from_cf, get_dealer_by_id, get_dealers_by_state, get_dealer_reviews_from_cf, post_request

from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Creating views here...

#
#   `about` view to render a static about page
# 

def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)



#
#   `contact` view to return a static contact page
#

def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)



#
#   `login_request` view to handle sign in requests
#

def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)



#
#   `logout_request` view to handle sign out requests
#

def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')



#
#   `registration_request` view to handle sign up requests
#

def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/user_registration_bootstrap.html', context)



#
# `get_dealerships` view renders the index page with a list of dealerships
#

def get_dealerships(request):
    context = {}
    if request.method == "GET":
        
        get_dealership_url = os.getenv('GET_DEALERSHIP_API')
        
        if 'state' in request.GET:
            ###  "state" needs to be the 2-letter abbr. of the state for the cloud function to return values
            dealerships = get_dealers_by_state(get_dealership_url, request.GET['state'])
        elif 'dealerId' in request.GET:
            dealerships = get_dealer_by_id(get_dealership_url, request.GET['dealerId'])
        else:
            dealerships = get_dealers_from_cf(get_dealership_url)

        context['dealerships'] = dealerships
        
        return render(request, 'djangoapp/index.html', context)


#
#   `get_dealer_details` view renders the reviews of a dealer
#

def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        get_dealership_url = os.getenv('GET_DEALERSHIP_API')

        ###     expects to receive an <array> of DealerReview objects
        dealer_reviews = get_dealer_reviews_from_cf(dealerId=dealer_id)

        ###     expects to recieve a <list> containing 1 CarDealer obj
        dealership = get_dealer_by_id(get_dealership_url, dealer_id)

        context["dealer_id"] = dealer_id
        context["reviews"] = dealer_reviews
        context['dealer'] = dealership[0]

        return render(request, 'djangoapp/dealer_details.html', context)



#
#   `add_review` view to submit a review
#

def add_review(request, dealer_id):
    context = {}
    
    if request.method == 'GET':
        cars = CarModel.objects.all()
        get_dealership_url = os.getenv('GET_DEALERSHIP_API')
        dealership = get_dealer_by_id(get_dealership_url, dealer_id)

        context["dealer_id"] = dealer_id
        context["cars"] = cars
        context['dealer'] = dealership[0]

        return render(request, 'djangoapp/add_review.html', context)


    if request.method == 'POST':
        user = request.user

        post_review_url = os.getenv("POST_REVIEW_API")

        review = {}
        review["time"] = datetime.utcnow().isoformat()
        review["id"] = user.id
        review["dealership"] = dealer_id
        review["review"] = request.POST["review"]
        review["name"] = user.first_name + " " + user.last_name
        
        if "purchasecheck" in request.POST:
            review["purchase"] = True
            if "car" in request.POST:
                car = get_object_or_404(CarModel, pk=request.POST["car"])
                review["car_year"] = car.year.strftime("%Y")
                review["car_make"] = car.make.name
                review["car_model"] = car.name
            if "purchasedate" in request.POST:
                review["purchase_date"] = request.POST["purchasedate"]
        else:
            review["purchase"] = False
        
        json_payload = {}
        json_payload["review"] = review

        response = post_request(post_review_url, json_payload, dealerId=dealer_id)
        print(response.text)


    return redirect("djangoapp:dealer_details", dealer_id=dealer_id)


