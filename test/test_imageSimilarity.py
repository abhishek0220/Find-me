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