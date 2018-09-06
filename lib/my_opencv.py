# -*- coding: utf-8 -*-

import cv2
import sys
import time
import datetime
import os

class My_OpenCV:
	def __init__(self, cascade_path):
		self.c = cv2.VideoCapture(0)
		self.cascade = cv2.CascadeClassifier(cascade_path)
		if not self.c.isOpened():
			print("カメラとの接続に失敗しました")
			sys.exit()
		
	#顔を四角で囲む
	def infomation(self, image, facerect):
		color = (255, 255, 255)
		for rect in facerect:
			cv2.rectangle(image, tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]), color, thickness=2)#検出した顔を囲む矩形の作成
		image = cv2.flip(image, 1)#反転
		cv2.imshow("face", image)
		cv2.waitKey(1)

	def detection(self):
		sum_of_detection = 0
		start = time.time()
		while sum_of_detection<10 and (time.time()-start)<2:
			r, image = self.c.read()
			image = cv2.resize(image, None, fx = 0.5, fy = 0.5)#アスペクト比を維持してリサイズする
			image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)#グレースケール変換
			facerect = self.cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=1, minSize=(50, 50), maxSize=(100, 100))
			self.infomation(image, facerect)

			if len(facerect) > 0:
				sum_of_detection = sum_of_detection + 1
		self.image = image

	def face_tracking(self):
		while True:
			start = time.time()
			self.detection()
			elapsed_time = time.time() - start
			if elapsed_time < 1:
				cv2.imwrite("face_image.jpg", self.image)
				return True

	#FaceAPIレスポンスのfaceRectangleで写真を切り取る
	def faceAPI_add_face(self, detect_result, identify_result):
		
		today = datetime.date.today()

		now = datetime.datetime.today()
		time = datetime.time(now.hour,now.minute,now.second)

		if identify_result[0]["candidates"] == []:
			personId = "unknown"
		else:
			personId = identify_result[0]["candidates"][0]["personId"]


			if not os.path.isdir("./face/"+personId):
				os.system("mkdir "+"./face/"+personId)

			left = detect_result[0]["faceRectangle"]["left"]
			top = detect_result[0]["faceRectangle"]["top"]
			width = detect_result[0]["faceRectangle"]["width"]
			height = detect_result[0]["faceRectangle"]["height"]

			path ="./face/"+personId+"/"+str(today)+"_"+str(time)+".jpg"
			face_image = cv2.imread('face_image.jpg')
			face_image = face_image[top:top+height,left:left+width]
			cv2.imwrite(path, face_image)
				
				
	#表情認識ための表情を撮影する
	def video_capture(self, frame=50):
		fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
		video = cv2.VideoWriter('./video.avi', fourcc, 10.0, (640, 480))
		for i in range(1, frame):
			r, image = self.c.read()
			img = cv2.resize(image, (640,480))
			video.write(img)
			cv2.putText(img, str(i/10.0), (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), thickness=2)
			cv2.imshow("face",img)
			cv2.waitKey(1)

if __name__ == '__main__':
	path = "../haarcascade_frontalface_default.xml"
	mo = My_OpenCV(path)
	# r = mo.face_tracking()
	# print(r)
	mo.video_capture(frame=80)