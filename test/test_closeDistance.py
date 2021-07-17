import sys
sys.path.append("/Users/samarthsingh/Find-me/")
import os
os.environ["COCKROACHDB"]= "cockroachdb://findadmin:findmlh2021iitj@free-tier5.gcp-europe-west1.cockroachlabs.cloud:26257/abhishek-605.findme?sslmode=require"
os.environ['JWT_SECRET'] = "mlhsecretforfindmeproj"
os.environ['SUBSCRIPTION_KEY']= "0bf8962f04a84f7aaecb166bc0463ab5"
os.environ['IMAGE_SIMILARITY_ENDPOINT'] = "https://abhisproj.cognitiveservices.azure.com"
import pytest
from FindMe.APIs.tasks import isClose

def test_isCloseEvaluatesTrue():
    # IIT Jammu Volleyball Court
    lat1 = 32.801327378634554
    long1 = 74.89640421112314
    # IIT Jammu BasketBall Court
    lat2 = 32.801328595317045
    long2  = 74.89622208882155

    assert isClose(lat1, long1, lat2, long2) == True

def test_isCloseEvaluatesFalse():
    # IIT Jammu Volleyball Court
    lat1 = 32.801327378634554
    long1 = 74.89640421112314
    # Maggi Point
    lat2 = 32.807139869187786
    long2 = 74.89683075592777

    assert isClose(lat1, long1, lat2, long2) == False