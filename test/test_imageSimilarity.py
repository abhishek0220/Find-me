import pytest
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from FindMe.Utils.imageSimilarity import checkSimilar, cvClient


def test_cvClientIsAuthenticated():
    myClient = cvClient()
    assert isinstance(myClient.client, ComputerVisionClient)


def test_check_similar_true():
    imageURL = "http://media.socastsrm.com/wordpress/wp-content/blogs.dir/1297/files/2017/12/traffic-lights.jpg"
    imagePath = "test/testImages/trafficLight.jpg"

    assert checkSimilar(imageURL, imagePath) is True


def test_check_similar_false():
    imageURL = "https://scx2.b-cdn.net/gfx/news/2017/higherconcen.jpg"
    imagePath = "test/testImages/trafficLight.jpg"

    assert checkSimilar(imageURL, imagePath) is False