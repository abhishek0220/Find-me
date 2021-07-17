import sys
sys.path.append("/Users/samarthsingh/Find-me/")
import os
os.environ["COCKROACHDB"]= "cockroachdb://findadmin:findmlh2021iitj@free-tier5.gcp-europe-west1.cockroachlabs.cloud:26257/abhishek-605.findme?sslmode=require"
os.environ['JWT_SECRET'] = "mlhsecretforfindmeproj"
os.environ['SUBSCRIPTION_KEY']= "0bf8962f04a84f7aaecb166bc0463ab5"
os.environ['IMAGE_SIMILARITY_ENDPOINT'] = "https://abhisproj.cognitiveservices.azure.com"
import pytest
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from FindMe.Utils.imageSimilarity import _CvClient


def test_cvClientIsAuthenticated():
    myClient = _CvClient()
    assert isinstance(myClient.client, ComputerVisionClient)


def test_check_similar_true():
    myClient = _CvClient()
    imageURL = "http://media.socastsrm.com/wordpress/wp-content/blogs.dir/1297/files/2017/12/traffic-lights.jpg"
    imagePath = "test/testImages/trafficLight.jpg"

    assert myClient.check_similar(imageURL, imagePath) is True


def test_check_similar_false():
    myClient = _CvClient()
    imageURL = "https://scx2.b-cdn.net/gfx/news/2017/higherconcen.jpg"
    imagePath = "test/testImages/trafficLight.jpg"

    assert myClient.check_similar(imageURL, imagePath) is False