import cv2 as cv
import os
from datetime import datetime
import time

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
        exit()
    
    # get frames
    width, height, fps = get_frames(video)
    
    # path
    os.makedirs('videos', exist_ok=True)
    os.makedirs('captures', exist_ok=True)
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    video_path = f"videos/recorded_video_{current_time}.avi"
    
    # codec
    codec = cv.VideoWriter_fourcc(*'XVID')
    writer = cv.VideoWriter(video_path, codec, fps, (width, height))

    is_recording = False
    capture_msg_end_time = 0
    active_filters = []
    
    while True:
        is_read, img = video.read()  
        if not is_read:
            break
        
        # Horizontal & Vertical 
        has_horizontal = 'Horizontal' in active_filters
        has_flip = 'Vertical' in active_filters
        if has_horizontal and has_flip:
            img = cv.flip(img, -1) 
        elif has_horizontal:
            img = cv.flip(img, 1) 
        elif has_flip:
            img = cv.flip(img, 0)  
        
        # prevent red circle in recorded video
        display_img = img.copy()
        
        # UI
        cv.rectangle(display_img, (10, 10), (width - 10, height - 10), (255, 255, 255), 2)
        cv.putText(display_img, "VISION REC", (20, 40), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), thickness=4)
        cv.putText(display_img, "VISION REC", (20, 40), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), thickness=2)
        current_display_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv.putText(display_img, current_display_time, (20, height - 20), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Horizontal & Vertical UI
        filter_x = 20
        filter_y = 70 
        for filter_name in active_filters:
            text_size = cv.getTextSize(filter_name, cv.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
            cv.putText(display_img, filter_name, (filter_x, filter_y), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), thickness=4)
            cv.putText(display_img, filter_name, (filter_x, filter_y), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 200, 0), thickness=2)
            filter_x += text_size[0] + 15
        
        # Capture UI
        if time.time() < capture_msg_end_time:
            text = "Captured"
            text_size = cv.getTextSize(text, cv.FONT_HERSHEY_SIMPLEX, 1.5, 3)[0]
            text_x = (width - text_size[0]) // 2 
            text_y = height - 100
            cv.putText(display_img, text, (text_x, text_y), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), thickness=6)
            cv.putText(display_img, text, (text_x, text_y), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), thickness=3)
            
        # Recording UI
        if is_recording:
            writer.write(img)
            cv.circle(display_img, (width - 30, 30), 10, (0, 0, 255), -1)
            cv.putText(display_img, "REC", (width - 80, 35), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), thickness=4)
            cv.putText(display_img, "REC", (width - 80, 35), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), thickness=2)
        else:
            cv.putText(display_img, "STBY", (width - 80, 35), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), thickness=4)
            cv.putText(display_img, "STBY", (width - 80, 35), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), thickness=2)
        cv.imshow('VisionRec', display_img)
        
        # Input Keys
        key_raw = cv.waitKey(1)
        key = key_raw & 0xFF # erase remaining last 8bits
        if key == 27: # ESC
            break
        elif key == 32: # space
            if is_recording:
                is_recording = False
            else:
                is_recording = True
        elif key == 67 or key == 99:
            cap_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            cap_path = f"captures/capture_{cap_time}.jpg"
            cv.imwrite(cap_path, img) 
            capture_msg_end_time = time.time() + 1.0
        elif key == ord('h') or key == ord('H'):
            if 'Horizontal' in active_filters:
                active_filters.remove('Horizontal') 
            else:
                active_filters.append('Horizontal') 
        elif key == ord('v') or key == ord('V'):
            if 'Vertical' in active_filters:
                active_filters.remove('Vertical')      
            else:
                active_filters.append('Vertical')

    video.release()
    writer.release()
    cv.destroyAllWindows()