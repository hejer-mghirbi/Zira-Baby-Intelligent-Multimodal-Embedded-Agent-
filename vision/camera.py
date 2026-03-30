import cv2
import time


class Camera:
    def __init__(self):
        # =========================
        # CAMERA INIT
        # =========================
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        # =========================
        # MODEL LOAD
        # =========================
        self.net = cv2.dnn.readNetFromCaffe(
            "models/MobileNetSSD_deploy.prototxt",
            "models/MobileNetSSD_deploy.caffemodel"
        )

        self.classes = [
            "background", "aeroplane", "bicycle", "bird", "boat",
            "bottle", "bus", "car", "cat", "chair", "cow",
            "diningtable", "dog", "horse", "motorbike", "person",
            "pottedplant", "sheep", "sofa", "train", "tvmonitor"
        ]

        self.indoor_objects = [
            "person", "chair", "sofa", "tvmonitor",
            "bottle", "diningtable", "pottedplant"
        ]

        # =========================
        # MEMORY (IMPORTANT)
        # =========================
        self.last_frame = None
        self.last_objects = []
        self.last_update_time = 0

        self.fps_delay = 1.0  # 1 frame per second (good for Raspberry Pi)

    # =========================
    # CAPTURE FRAME ONLY
    # =========================
    def get_frame(self):
        ret, frame = self.cap.read()

        if not ret:
            return None

        self.last_frame = frame
        return frame

    # =========================
    # CORE DETECTION ENGINE
    # =========================
    def detect_objects(self, force=False):
        """
        Lightweight detection function
        Can be called safely in a loop/thread
        """

        current_time = time.time()

        # FPS CONTROL (VERY IMPORTANT)
        if not force and (current_time - self.last_update_time) < self.fps_delay:
            return self.last_objects

        frame = self.get_frame()
        if frame is None:
            return []

        h, w = frame.shape[:2]

        blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)
        self.net.setInput(blob)
        detections = self.net.forward()

        detected_objects = []

        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            if confidence > 0.5:
                class_id = int(detections[0, 0, i, 1])

                if class_id >= len(self.classes):
                    continue

                label = self.classes[class_id]

                if label in self.indoor_objects:
                    detected_objects.append(label)

                    # Draw box (optional visual debug)
                    box = detections[0, 0, i, 3:7] * [w, h, w, h]
                    (x1, y1, x2, y2) = box.astype("int")

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(
                        frame,
                        label,
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 255, 0),
                        2
                    )

        # Update memory
        self.last_objects = list(set(detected_objects))
        self.last_update_time = current_time

        # Show (optional)
        cv2.imshow("AI Vision", frame)
        cv2.waitKey(1)

        return self.last_objects

    # =========================
    # SIMPLE IMAGE CAPTURE
    # =========================
    def capture_image(self):
        frame = self.get_frame()

        if frame is not None:
            cv2.imshow("Camera", frame)
            cv2.waitKey(1)
            return frame

        return None

    # =========================
    # SAFE ACCESSOR (IMPORTANT FOR AI)
    # =========================
    def get_last_objects(self):
        return self.last_objects

    # =========================
    # CLEANUP
    # =========================
    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()