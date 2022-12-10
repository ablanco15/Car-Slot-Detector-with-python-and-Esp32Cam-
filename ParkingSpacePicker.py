import cv2
import pickle


URL = "http://192.168.1.112"
AWB = True

width, heigth = 107, 48

try:
    with open("CarParkPos1" , "rb") as f:
        posList = pickle.load(f)
except:
    posList = []

try:
    cap = cv2.VideoCapture(URL+":81/stream")  
except:
    print("error")



def mouseClick(events,x,y,flags,params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x,y))
        print(posList)
        print(x,y)
    if events == cv2.EVENT_RBUTTONDOWN:
        for i,pos in enumerate(posList):
            x1, y1 = pos
            if  x1 < x < x1+width and y1<y<y1+heigth:
                posList.pop(i)
    
    with open("CarParkPos1" , "wb") as f:
        pickle.dump(posList, f)                

                

while True:
    if cap.isOpened():
            success, img = cap.read()
    #img = cv2.imread("resources/carParkImg.png")    
    for pos in posList:
        cv2.rectangle(img,pos, (pos[0]+width , pos[1]+heigth) ,(255,0,255),2)
        
    cv2.imshow("img1", img)
    cv2.setMouseCallback("img1",mouseClick)
    cv2.waitKey(1)