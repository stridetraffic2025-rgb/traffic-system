import cv2
import numpy as np
import imutils
import time

try:    
    with open("coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
except FileNotFoundError:
    print("Error: coco.names file not found.")
    exit()

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

try:
    yolo_net = cv2.dnn.readNet("yolov4.weights", "yolov4.cfg")
except cv2.error as e:
    print(f"Error loading YOLOv4 model: {e}")
    exit()

layer_names = yolo_net.getLayerNames()
try:
    output_layers = [layer_names[i[0] - 1] for i in yolo_net.getUnconnectedOutLayers()]
except IndexError:
    output_layers = [layer_names[i - 1] for i in yolo_net.getUnconnectedOutLayers()]

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

cv2.namedWindow("Car Counter", cv2.WINDOW_NORMAL)

screen_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
screen_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
if screen_width == 0 or screen_height == 0:  
    screen_width, screen_height = 1920, 1080  
cv2.resizeWindow("Car Counter", screen_width, screen_height)


line_y = 250
object_count = 0
last_count_time = 0
tracker = CentroidTracker()

while True:
    start_time = time.time()
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break

    frame = imutils.resize(frame, width=700)
    height, width = frame.shape[:2]

    # Create a blob and do a forward pass
    blob = cv2.dnn.blobFromImage(frame, 1/255.0, (320, 320), swapRB=True, crop=False)
    yolo_net.setInput(blob)
    layer_outputs = yolo_net.forward(output_layers)

    boxes = []
    confidences = []
    class_ids = []

    # Extract bounding boxes and confidences
    for output in layer_outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5 and classes[class_id] == "car":  # Filter for cars only
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
    rects = []

    if len(indices) > 0:
        for i in indices.flatten():
            x, y, w, h = boxes[i]
            rects.append((x, y, x + w, y + h))
            label = f"Car: {confidences[i]:.2f}"
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, label, (x, y - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    # Update tracker and count objects
    tracked_objects = tracker.update(rects)
    cv2.line(frame, (0, line_y), (width, line_y), (255, 0, 0), 2)

    for object_id, (cX, cY) in tracked_objects.items():
        cv2.circle(frame, (cX, cY), 4, (0, 0, 255), -1)
        if cY > line_y and object_id not in tracker.counted_ids and time.time() - last_count_time > 0.5:
            object_count += 1
            tracker.counted_ids.add(object_id)
            last_count_time = time.time()
            print(f"✅ Car {object_id} counted! Total: {object_count}")

    # Display count and FPS
    fps = 1 / (time.time() - start_time)
    cv2.putText(frame, f"Count: {object_count}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    cv2.putText(frame, f"FPS: {fps:.2f}", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    # Show the frame
    cv2.imshow("Car Counter", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
