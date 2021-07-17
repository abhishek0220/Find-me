from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import os

class cvClient:
    def __init__(self):
        subscription_key = os.environ.get('SUBSCRIPTION_KEY')
        endpoint = os.environ.get('IMAGE_SIMILARITY_ENDPOINT')
        self.client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
    
    def getTopTagsFromURL(self, imgURL: str,topN: int):
        '''
        Return topN tags for the imageURL as a List
        '''
        tagResults = self.client.tag_image(imgURL).tags
        tagNames = [x.name for x in tagResults]
        return tagNames[:topN]  
    
    def getTopTagsFromStream(self, imgPath: str, topN: int):
        '''
        Return topN tags for the imageStream as a List
        '''
        img = open(imgPath, 'r+b')
        tagResults = self.client.tag_image_in_stream(img).tags
        tagNames = [x.name for x in tagResults]
        return tagNames[:topN]

def checkSimilar(img1URL: str, img2Path: str):
    myclient = cvClient()
    tagNames1 = myclient.getTopTagsFromURL(img1URL,5)
    tagNames2 = myclient.getTopTagsFromStream(img2Path, 5)
    print(tagNames1, tagNames2)
    if(len(set(tagNames1).intersection(set(tagNames2))) >= min(max(len(tagNames1), len(tagNames2)),4)):
        return True
    else:
        return False





