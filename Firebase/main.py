import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime


# Link to database
cred = credentials.Certificate("vito-application-ec538-firebase-adminsdk-ypubk-36e5c5da9e.json")
firebase_admin.initialize_app(cred,{
    "databaseURL" : "https://vito-application-ec538-default-rtdb.firebaseio.com/",
    "storageBucket":"gs://vito-application-ec538.appspot.com"
})

#=========================================================================================================
# Account information
ref = db.reference("Users")

def update_data(ID, name, height, weight, type="free", turns=10):
    '''
    Arguments:
        + ID: id của mỗi tài khoản
        + name: tên chủ tài khoản
        + heihgt, weight: chiều cao và cân nặng
        + type: gói dịch vụ. Mặc định là free
        + turns: số lượt thử. Mặc định là 1o lần/ngày
        '''
    data = {
            ID : {
                "name" : name,
                "height" : height,
                "weight" : weight,
                "type" : type,
                "turns" : turns
        }}
    try:
        ref.child(ID).set(data[ID])
        print("Successfully updated!")
    except:
        print("Update failed!")
        
#===========================================================================================================
# Account images
def upload_images(ID: str, img_human, img_clothes, img_result):
    bucket = storage.bucket()  
    user_folder = f'users/{ID}' 

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    new_folder = f'{user_folder}/{timestamp}/'

    files_to_upload = {
        'human': img_human,
        'clothes': img_clothes,
        'result': img_result
    }
    
    for _, path in files_to_upload.items():
        blob = bucket.blob(f"{new_folder}{path}")
        blob.upload_from_filename(path)
    print("Upload successful!")

#===================================INFERENCE========================================
if __name__=="__main__":
    update_data("YOUR ID", name="Huy", height="165", weight="60")
    upload_images("YOUR ID", "1.png", "2.png", "3.png")
