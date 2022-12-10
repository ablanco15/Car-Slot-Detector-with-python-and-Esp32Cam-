import cv2
import numpy as np
import pickle
import cvzone
import requests

URL = "http://192.168.1.112"
AWB = True

with open("CarParkPos1" , "rb") as f:
    posList = pickle.load(f)


width, heigth = 107, 48

try:
    cap = cv2.VideoCapture(URL+":81/stream")  
except:
    print("error")

def set_resolution(url: str, index: int=1, verbose: bool=False):
    try:
        if verbose:
            resolutions = "10: UXGA(1600x1200)\n9: SXGA(1280x1024)\n8: XGA(1024x768)\n7: SVGA(800x600)\n6: VGA(640x480)\n5: CIF(400x296)\n4: QVGA(320x240)\n3: HQVGA(240x176)\n0: QQVGA(160x120)"
            print("available resolutions\n{}".format(resolutions))

        if index in [10, 9, 8, 7, 6, 5, 4, 3, 0]:
            requests.get(url + "/control?var=framesize&val={}".format(index))
        else:
            print("Wrong index")
    except:
        print("SET_RESOLUTION: something went wrong")    

if __name__ == '__main__':
    set_resolution(URL, index=8)
    
    


def checkParkingSpace(imgPro):
    spaceCounter=0
    
    for pos in posList:
        x,y = pos

        imgCrop = imgPro[y:y+heigth,x:x+width]
        count = cv2.countNonZero(imgCrop)
        cvzone.putTextRect(img,str(count),(x,y+heigth-3),scale=1,thickness=1,offset=0)

        if count <400:
            color = (0,255,0)
            thickness=5
            spaceCounter+=1
        else:
            color = (0,0,255)
            thickness=2
        cv2.rectangle(img,pos, (pos[0]+width , pos[1]+heigth) ,color,thickness)

    cvzone.putTextRect(img,f'Free:{spaceCounter}/{len(posList)}', (100,50), scale=3,
                        thickness=5,offset=20, colorR = (0,200,0))


while True:
    if cap.isOpened():
            success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur =cv2.GaussianBlur(imgGray,(3,3),1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV,25,16)  
    imgMedian = cv2.medianBlur(imgThreshold,5)
    kernel = np.ones((3,3),np.uint8)    
    imgDilate = cv2.dilate(imgMedian,kernel,iterations=1)                                      

    checkParkingSpace(imgDilate)
    
        
    cv2.imshow("Image", img)
    #cv2.imshow("ImageBlur", imgBlur)
    #cv2.imshow("ImageThres", imgThreshold)
    #cv2.imshow("ImageMed", imgMedian)
    #cv2.imshow("ImageDilate", imgDilate)

    cv2.waitKey(1)