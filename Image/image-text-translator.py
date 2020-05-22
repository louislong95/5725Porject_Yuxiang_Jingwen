import cv2 
import pytesseract
from picamera.array import PiRGBArray
from picamera import PiCamera
import os, requests, uuid, json

'''args = {
 
        'client_id': '2909465536@qq.com',#your client id here
 
        'client_secret': 'louislong1995',#your azure secret here

        'scope': '',
 
 
        'grant_type': 'client_credentials'
 
}'''

camera = PiCamera()
camera.resolution = (1024, 768)
camera.framerate = 30

rawCapture = PiRGBArray(camera, size=(1024, 768))

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF
    
    rawCapture.truncate(0)

    if key == ord("s"):
        text = pytesseract.image_to_string(image).encode('utf-8','ignore')
        print(text)
        cv2.imshow("Frame", image)
        cv2.waitKey(0)
        break


key_var_name = 'TRANSLATOR_TEXT_SUBSCRIPTION_KEY'
if not key_var_name in os.environ:
    raise Exception('Please set/export the environment variable: {}'.format(key_var_name))
subscription_key = os.environ[key_var_name]

endpoint_var_name = 'TRANSLATOR_TEXT_ENDPOINT'
if not endpoint_var_name in os.environ:
    raise Exception('Please set/export the environment variable: {}'.format(endpoint_var_name))
endpoint = os.environ[endpoint_var_name]

path = '/translate?api-version=3.0'
params = '&to=zh'
constructed_url = endpoint + path + params

headers = {
    'Ocp-Apim-Subscription-Key': subscription_key,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}
text = text.replace('\n','')
body = [{
    'text': text
}]

request = requests.post(constructed_url, headers=headers, json=body)
response = request.json()

json_string = json.dumps(response, sort_keys=True, indent=4,
                 ensure_ascii=False, separators=(',', ': '))
json_string = json_string.encode('utf-8')
print(json_string)

cv2.destroyAllWindows()