import cv2
import glob
import numpy as np
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR/tesseract'
from googletrans import Translator
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from random import randint 
translator  = Translator()
writer  = None
path_to_images = r"./images/*.jpg"
files = glob.glob(path_to_images) 
while(True):
	for f in files:
		image = cv2.imread(f, cv2.IMREAD_COLOR)
		image = cv2.resize(image, (640, 640))
		im  =  Image.new("RGB", (640, 640), (255,255,255))
		draw  =  ImageDraw.Draw(im)
		unicode_font = ImageFont.truetype("DejaVuSans.ttf", 15)
		(H, W) = image.shape[:2]
		board = np.zeros((H, W,3), np.uint8)
		board[:] = 255
		text = pytesseract.image_to_string(image, config="-l eng --oem 1 --psm 3")
		random_text =text.splitlines()
		for i in range(len(random_text)):
			text = translator.translate(random_text[i], dest='tr').text
			text= u'%s'%(text)
			draw.text ( (20,20*(i+1)), text, font=unicode_font, fill=(0,0,0) )
		final_version = np.concatenate((im,image), axis=1)
		cv2.imshow("Result", final_version)
		key = cv2.waitKey(1) & 0xFF
		if key == 27:
			break
		
		if writer is None:
			fourcc = cv2.VideoWriter_fourcc(*"MJPG")
			writer = cv2.VideoWriter("text_recognition.avi", fourcc, 1,
				(final_version.shape[1], final_version.shape[0]), True)
		if writer is not None:
			writer.write(final_version)	
		
cv2.destroyAllWindows()
cap.release()

if writer is not None:
	writer.release()
