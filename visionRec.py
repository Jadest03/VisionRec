import cv2 as cv

video = cv.VideoCapture(0)

if not video.isOpened():
    print("카메라를 열지 못했습니다. 연결을 확인해주세요.")
    exit()
    
while True:
    is_read, img = video.read()
    
    if not is_read:
        print("영상을 가져오는데 실패했습니다.")
        break
    
    cv.imshow('VisionRec', img)
    key = cv.waitKey(1)
    if key == 27: # ESC
        print("VisionRec을 종료합니다.")
        break

video.release()
cv.destroyAllWindows()