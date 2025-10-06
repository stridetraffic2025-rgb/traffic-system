import cv2
import numpy as np
import imutils
import time
from flask import Flask, render_template, Response

# -------------------
# Load COCO Names
# -------------------
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# -------------------
# Load YOLOv4-Tiny model
# -------------------
yolo_net = cv2.dnn.readNet("yolov4-tiny.weights", "yolov4-tiny.cfg")

layer_names = yolo_net.getLayerNames()
output_layers = [layer_names[i - 1] for i in yolo_net.getUnconnectedOutLayers()]

# -------------------
# Centroid Tracker
# -------------------
class CentroidTracker:
    def __init__(self):
        self.next_object_id = 0
        self.objects = {}
        self.counted_ids = set()

    def update(self, boxes):
        new_objects = {}
        for (startX, startY, endX, endY) in boxes:
            cX = int((startX + endX) / 2.0)
            cY = int((startY + endY) / 2.0)
            new_objects[self.next_object_id] = (cX, cY)
            self.next_object_id += 1
        self.objects = new_objects
        return self.objects

# -------------------
# Flask App
# -------------------
app = Flask(__name__)
cap = cv2.VideoCapture(0)  # webcam
tracker = CentroidTracker()
line_y = 250
object_count = 0
last_count_time = 0

def generate_frames():
    global object_count, last_count_time
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = imutils.resize(frame, width=700)
        height, width = frame.shape[:2]

        # YOLOv4-Tiny blob
        blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
        yolo_net.setInput(blob)
        layer_outputs = yolo_net.forward(output_layers)

        boxes, confidences, class_ids, rects = [], [], [], []
        for output in layer_outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > 0.5 and classes[class_id] == "car":
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        if len(indices) > 0:
            for i in indices.flatten():
                x, y, w, h = boxes[i]
                rects.append((x, y, x + w, y + h))
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, "Car", (x, y - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        # Tracking & Counting
        tracked_objects = tracker.update(rects)
        cv2.line(frame, (0, line_y), (width, line_y), (255, 0, 0), 2)

        for object_id, (cX, cY) in tracked_objects.items():
            cv2.circle(frame, (cX, cY), 4, (0, 0, 255), -1)
            if cY > line_y and object_id not in tracker.counted_ids and time.time() - last_count_time > 0.5:
                object_count += 1
                tracker.counted_ids.add(object_id)
                last_count_time = time.time()
                print(f"✅ Car {object_id} counted! Total: {object_count}")

        # Display Count
        cv2.putText(frame, f"Count: {object_count}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        # Encode for Flask
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
