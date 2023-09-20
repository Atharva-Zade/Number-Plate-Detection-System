import cv2
import pytesseract
import threading

# Ensure the path to the Tesseract executable is in your system's PATH or specify it explicitly
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Modify this path accordingly

def detect_and_recognize_plate(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Load the license plate cascade from OpenCV
    plate_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_russian_plate_number.xml")
    
    plates = plate_cascade.detectMultiScale(gray, 1.1, 10)
    
    for (x, y, w, h) in plates:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        plate = gray[y:y+h, x:x+w]
        
        # Recognize text with Tesseract
        text = pytesseract.image_to_string(plate, config='--psm 8')
        print("Detected license plate:", text)
        
        cv2.imshow("License Plate", plate)
    
    return frame

def process_camera(camera_link, window_name):
    cap = cv2.VideoCapture(camera_link)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print(f"Failed to grab frame for {window_name}")
            break
        
        processed_frame = detect_and_recognize_plate(frame)
        cv2.imshow(window_name, processed_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()

camera_links = [
    "rtsp://admin:Admin%40123@192.168.1.16:554/cam/realmonitor?channel=6&subtype=0",
    "rtsp://admin:Admin%40123@192.168.1.16:554/cam/realmonitor?channel=8&subtype=0",
    "rtsp://admin:Admin%40123@192.168.1.16:554/cam/realmonitor?channel=9&subtype=0",
]

threads = []

for idx, link in enumerate(camera_links):
    thread = threading.Thread(target=process_camera, args=(link, f"Camera Feed {idx+1}"))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

cv2.destroyAllWindows()
