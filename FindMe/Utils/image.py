from FindMe.Utils.gstorage import cloud_storage
from io import BytesIO
from PIL import Image
import base64
import uuid
import os


def save_image_locally(img_b64: str, file_prefix: str = ''):
    file_name = file_prefix + ''.join(str(uuid.uuid4()).split()) + '.jpg'
    image_data = bytes(img_b64, encoding="ascii")
    im = Image.open(BytesIO(base64.b64decode(image_data)))
    im = im.convert("RGB")
    file_loc = os.path.join(os.getcwd(), file_name)
    im.save(file_loc)
    return file_loc, file_name


def save_img_to_cloud(img_b64: str, file_prefix: str = ''):
    file_loc, file_name = save_image_locally(img_b64, file_prefix)
    public_url = cloud_storage.upload(file_loc, file_name)
    os.remove(file_loc)
    return public_url
