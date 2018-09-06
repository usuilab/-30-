# -*- coding: utf-8 -*-
import os
import time
import requests

#カスケード分類器
haarcascade_path = "./haarcascade_frontalface_default.xml"
# westus regional Base URL
BASE_URL = "https://westus.api.cognitive.microsoft.com/face/v1.0/"
#個人認識に使う写真
img_url = './face_image.jpg'
#apikeyを取り出す
from apikey import *
#docomoAPIを使うためライブラリ
from lib.docomo import Docomo
docomo = Docomo(DOCOMOAPI)
#データベースを使うためのライブラリ
from lib.db import DB
db = DB()
#OpenCVを使うためのライブラリ
from lib.my_opencv import My_OpenCV
my_opencv = My_OpenCV(haarcascade_path)
#個人認識を行うためのライブラリ
from lib.identification import Identification
id = Identification(BASE_URL,FACEAPI,img_url)

# 必要なフォルダの存在を確認する
if not os.path.isdir("./cache"):
	os.system("mkdir ./cache")
	if not os.path.isdir("./cache/audio"):
		os.system("mkdir ./cache/audio")
# 必要なフォルダの存在を確認する
if not os.path.isdir("./face/"):
	os.system("mkdir "+"./face/")

while True:
	my_opencv.face_tracking()
	personId = id.identification(display_status=True)
	print(personId)
	time.sleep(3)

# #db.emotion_1(detect_result, identify_result[0]["candidates"][0]["personId"])
# name = db.get_name(identify_result[0]["candidates"][0]["personId"])

# message = name["last_kana"]+name["first_kana"]+"さん、こんにちは"
# docomo.talk(message)
# my_opencv.faceAPI_add_face(detect_result, identify_result)

# docomo.talk("5秒間お待ちください")
# my_opencv.video_capture()

# docomo.talk("完了しました")
# url = "http://10.12.156.150:8000/emotion"
# file = "video.avi"
# r = requests.post(url, data=open(file, "rb"))

# print("{}".format(json.dumps(r.json(),indent=4)))
# db.emotion_2(r.json(), identify_result[0]["candidates"][0]["personId"])
# time.sleep(2)