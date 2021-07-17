from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import os


class _CvClient:
    def __init__(self):
        subscription_key = os.environ.get('SUBSCRIPTION_KEY')
        endpoint = os.environ.get('IMAGE_SIMILARITY_ENDPOINT')
        self.client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

    def get_top_tags_from_url(self, img_url: str, top_n: int):
        """
        Return topN tags for the imageURL as a List
        """
        tag_results = self.client.tag_image(img_url).tags
        tag_names = [x.name for x in tag_results]
        return tag_names[:top_n]
    
    def get_top_tags_from_stream(self, img_path: str, top_n: int):
        """
        Return topN tags for the imageStream as a List
        """
        img = open(img_path, 'r+b')
        tag_results = self.client.tag_image_in_stream(img).tags
        tag_names = [x.name for x in tag_results]
        return tag_names[:top_n]

    def check_similar(self, img1_url: str, img2_path: str):
        tag_names1 = self.get_top_tags_from_url(img1_url, 5)
        tag_names2 = self.get_top_tags_from_stream(img2_path, 5)
        print(tag_names1, tag_names2)
        if(
                len(set(tag_names1).intersection(set(tag_names2))) >= min(max(len(tag_names1), len(tag_names2)), 4)
        ):
            return True
        else:
            return False

cv_client = _CvClient()
