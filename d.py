from skimage import io
import numpy as np
from sklearn.externals import joblib
from serial import Serial
import time
import cv2
import requests
from PIL import Image
from io import BytesIO
import time
import uuid
#from urllib import urlretrieve

arduino = Serial('COM3', 250000)
time.sleep(2)

arduino.write(b'forward_on\n')
time.sleep(0.1)
arduino.write(b'forward_off\n')
time.sleep(0.1)
arduino.write(b'backward_on\n')
time.sleep(0.1)
arduino.write(b'backward_off\n')
time.sleep(0.1)
arduino.write(b'left_on\n')
time.sleep(0.1)
arduino.write(b'left_off\n')
time.sleep(0.1)
arduino.write(b'right_on\n')
time.sleep(0.1)
arduino.write(b'right_off\n')

CAMERA_URL = 'http://192.168.43.1:8080/shot.jpg'
ARDUINO_SERVER = 'http://localhost:5000'

clf = joblib.load('m1all-1.pkl')
#scaler = joblib.load('trail.pkl')
#scaler_stop = joblib.load('stop/scaler.pkl')
#is_stop = joblib.load('stop/model.pkl')
print('model loaded')

def send_command(result):
    if result == '0':
        arduino.write(b'forward_on\n')
        time.sleep(0.12)
        print (result)
        arduino.write(b'forward_off\n')
    if result == '1':
        arduino.write(b'left_on\n')
        time.sleep(0.5)
        print (result)
        arduino.write(b'forward_on\n')
        time.sleep(0.12)
        arduino.write(b'forward_off\n')
        time.sleep(0.5)
        arduino.write(b'left_off\n')
    if result == '2':
        arduino.write(b'right_on\n')
        time.sleep(0.5)
        print (result)
        arduino.write(b'forward_on\n')
        time.sleep(0.17)
        print (result)
        arduino.write(b'forward_off\n')
        time.sleep(0.5)
        arduino.write(b'right_off\n')

def drive():
    #img = cv2.imread('C:/Users/John Doe/d-ff/Desktop/self-driving-rc-car-master/data_temp/a.jpg')
    #print (img)
    #response = requests.get(CAMERA_URL)
    #img = Image.open(BytesIO(response.content)).convert('L')
    #img = cv2.imread(CAMERA_URL)
    #urlretrieve(CAMERA_URL, "img.jpg")
    #url_response = urllib.urlopen(CAMERA_URL)
    response = requests.get(CAMERA_URL)
    print ("image send")
    Image.open(BytesIO(response.content)).convert('L').save('C:/Users/John Doe/d-ff/Desktop/self-driving-rc-car-master/img.jpg')
    img = cv2.imread('img.jpg')
    print ('succes')
    
    cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.blur(img, (5, 5))
    retval, img = cv2.threshold(img, 210, 255, cv2.THRESH_BINARY)
    img = cv2.resize(img, (24, 24))
    retval, img = cv2.threshold(img, 210, 255, cv2.THRESH_BINARY)
    image_as_array = np.ndarray.flatten(np.array(img))
    result = clf.predict([image_as_array])[0]
    print(result)

    send_command(result)

    time.sleep(0.5)
    drive()

print('start driving')

drive()
