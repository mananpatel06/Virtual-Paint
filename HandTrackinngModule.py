import cv2
import mediapipe as mp
import time

class handDetector():

    def __init__(self , mode = False , numberOfHands = 2 ,modelComplexity =1 ,detectionConfidence=0.5,trackingConfidence = 0.5):
        self.mode = mode
        self.numberOfHands =numberOfHands
        self.modelComplexity=modelComplexity
        self.detectionConfidence=detectionConfidence
        self.trackingConfidence=trackingConfidence

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.numberOfHands,self.modelComplexity,
                                        self.detectionConfidence,self.trackingConfidence)
        self.mpDraw = mp.solutions.drawing_utils

        self.tipIds = [4, 8, 12, 16, 20]


    def findHands(self,img,draw =True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, hand_landmarks, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self,img,handNumber=0,draw =True):

        self.lmList = []

        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNumber]

            for id, lm in enumerate(myHand.landmark):
                # print(id,lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id , cx , cy])
                if draw:
                    cv2.circle(img,(cx,cy),10,(255,0,0),-1)

        return self.lmList

    def fingersUp(self):
        fingers = []
        # Thumb
        if self.lmList[self.tipIds[0]][1] < self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Fingers
        for id in range(1, 5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

            # totalFingers = fingers.count(1)

        return fingers


def main() :
    cap = cv2.VideoCapture(0)
    detector = handDetector()

    pTime = 0
    cTime = 0
    # cap.set(3, 960)

    while True:
        sucess, img = cap.read()

        # print(img.shape)
        img = detector.findHands(img)
        lmList = detector.findPosition(img,draw=False)
        # print(lmList)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 3)

        cv2.imshow("video", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    main()