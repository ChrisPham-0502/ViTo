import HairStyle
import Size_recommend
from Tryons.main import Vito_model

from firebase_admin import storage

from Firebase.main import upload_image
from PIL import Image
import numpy as np
import cv2, os

def VitoClothes(linkFirebaseHuman: str, linkFirebaseCloth: str): 
    # return linkFirebaseResult: str   
    bucket = storage.bucket()
    blob = bucket.get_blob(linkFirebaseHuman)
    body_img = np.frombuffer(blob.download_as_string(), np.uint8)
    
    blob = bucket.get_blob(linkFirebaseCloth)
    cloth_img = np.frombuffer(blob.download_as_string(), np.uint8)
    
    body_img = cv2.imdecode(body_img, cv2.COLOR_BGRA2BGR)
    cloth_img = cv2.imdecode(cloth_img, cv2.COLOR_BGRA2BGR)
    
    body_img = cv2.resize(body_img, (768, 1024))    
    cloth_img = cv2.resize(cloth_img, (768, 1024))
    
    path = Vito_model(model_img=body_img, cloth_img=cloth_img)
    img_path = os.path.basename(path)
    
    root_dir = linkFirebaseHuman.split("/")
    result = upload_image(ID=root_dir[1], image=img_path)
    return result
    
        

def VitoHair():
    pass

def VitoSize(weight: str, height: str):
    #return size: str
    pass

if __name__=="__main__":
    body_path = upload_image(ID=12345, image="body.jpg")
    garment = upload_image(ID=None, image='garment.jpg')
    
    linkFirebaseResult = VitoClothes(body_path, garment)
