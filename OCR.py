import urllib
import cv2
import numpy as np
import ssl
import requests
import io
import simplejson as json
tot = []

#haha this is a change

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'use ip address of the camera, i have used IP webcam in my phone'

while True:
    imgResp = urllib.request.urlopen(url)
    imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
    img = cv2.imdecode(imgNp, -1)
    
    cv2.rectangle(img,(520,0),(900,1050),(0,0,255),10)
    cv2.imshow('temp',cv2.resize(img,(1000,800)))
    q = cv2.waitKey(1)
    if q == ord("q"):
        break;            #press q to close.
        
    elif q%256 == 32:
        # SPACE pressed to take a picture
        img_name = "test.jpg"
        cv2.imwrite(img_name, img)
        print("{} written!".format(img_name))
        roi = cv2.imread("test.jpg")
        roi = roi[0:1050, 520:900]
        cv2.imshow("test", cv2.resize(roi,(100,500)))

        url_api = "https://api.ocr.space/parse/image"
        _, compressedimage = cv2.imencode(".jpg", roi, [1,90])
        file_bytes = io.BytesIO(compressedimage)

        result = requests.post(url_api, 
                      files={"C:/Users/Souvik_2/Desktop/test.jpg": file_bytes},
                      data={"apikey":"get your free api key from ocr.space", "OCREngine":"2"})


        result=result.content.decode()
        result = json.loads(result)
        result = (result.get("ParsedResults")[0].get("ParsedText"))

        op=result.split("\n")
        for i in op:
            tot.append(i)
        tot = list(map(float,tot))


        
        

cv2.destroyAllWindows()
print(tot)
print(sum(tot))
