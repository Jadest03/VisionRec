# VisionRec

This is a simple video recorder built with Python and OpenCV.   
It features real-time recording, video filters, and image capture.

## Features

* **Real-time Recording**: Toggle recording and standby modes easily with the `Space` bar.   
Videos are saved in `.avi` format.
* **Video Filters**:
  * `H` Key: Horizontal Flip
  * `V` Key: Vertical Flip
  * Active filters are displayed on the screen and applied directly to the recorded video.
* **Image Capture**: 
  * Press `C` to instantly capture the current frame without UI as a `.jpg` image. 
  * Shows a 1-second "Captured" visual feedback on the screen.


## Shortcuts

| Key | Description |
| :---: | --- |
| `Space` | Toggle Record & Stanby |
| `C` | Capture current frame |
| `H` | Toggle Horizontal Flip |
| `V` | Toggle Vertical Flip |
| `ESC` | Exit the program |  

## How to Run

It is recommended to use a python virtual environment 'venv'

1. Clone the repository
   ```bash
   git clone <your-repository-url>
   cd <your-project-folder>
   ```
2. Create a virtual environment
    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    venv\Scripts\activate
    ```
3. Install the libraries
    ```bash
    pip install -r requirements.txt
    ```
4. Run the code
    ```bash
    python visionRec.py
    ```

## Demo
![VisionRec Test Video](/recorded_video_20260315_143301.avi)