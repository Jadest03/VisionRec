import cv2 as cv
import os
from datetime import datetime

# functions
def get_frames(video):
    w = round(video.get(cv.CAP_PROP_FRAME_WIDTH))
    h = round(video.get(cv.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv.CAP_PROP_FPS)
    if fps == 0.0:
        fps = 30.0
        
    return (w, h, fps)

if __name__ == '__main__':
    video = cv.VideoCapture(0)
    if not video.isOpened():
        print("카메라를 열지 못했습니다. 연결을 확인해주세요.")
        exit()
    
    # get frames
    width, height, fps = get_frames(video)
    
    # path
    os.makedirs('videos', exist_ok=True)
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    video_path = f"videos/recorded_video_{current_time}.avi"
    
    # codec
    codec = cv.VideoWriter_fourcc(*'XVID')
    writer = cv.VideoWriter(video_path, codec, fps, (width, height))

    is_recording = False

    while True:
        is_read, img = video.read()  
        if not is_read:
            print("영상을 가져오는데 실패했습니다.")
            break
        
        # prevent red circle in recorded video
        display_img = img.copy()
        
        # UI
        cv.rectangle(display_img, (10, 10), (width - 10, height - 10), (255, 255, 255), 2)
        cv.putText(display_img, "VISION REC", (20, 40), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), thickness=4)
        cv.putText(display_img, "VISION REC", (20, 40), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), thickness=2)
        current_display_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv.putText(display_img, current_display_time, (20, height - 20), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Recording
        if is_recording:
            writer.write(img)
            cv.circle(display_img, (width - 30, 30), 10, (0, 0, 255), -1)
            cv.putText(display_img, "REC", (width - 80, 35), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), thickness=4)
            cv.putText(display_img, "REC", (width - 80, 35), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), thickness=2)
        # Not Recording
        else:
            cv.putText(display_img, "STBY", (width - 80, 35), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), thickness=4)
            cv.putText(display_img, "STBY", (width - 80, 35), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), thickness=2)
        cv.imshow('VisionRec', display_img)
        
        # Input Keys
        key = cv.waitKey(1)
        if key == 27: # ESC
            print("VisionRec을 종료합니다.")
            break
        elif key == 32: # space
            if is_recording:
                is_recording = False
                print("녹화가 일시정지되었습니다.")
            else:
                is_recording = True
                print("녹화가 시작되었습니다.")

    video.release()
    writer.release()
    cv.destroyAllWindows()