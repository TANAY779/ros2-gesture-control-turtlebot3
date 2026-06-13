import os
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Tuple

import cv2
from mediapipe.tasks.python import vision as mp_vision
from mediapipe.tasks.python.vision.core import image as mp_image

MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task"
)
MODEL_DIR = Path(__file__).resolve().parent.parent / ".mediapipe_models"
MODEL_PATH = MODEL_DIR / "hand_landmarker.task"
CAMERA_INDICES = [1, 0, 2, 3]


class HandDetector:
    def __init__(self, camera_indices: List[int] = None):
        self.camera_indices = camera_indices or CAMERA_INDICES
        self.model_path = self._ensure_model()
        self.hand_landmarker = mp_vision.HandLandmarker.create_from_model_path(
            str(self.model_path)
        )
        self.cap = self._open_camera()

    def _download_model(self, destination: Path) -> None:
        destination.parent.mkdir(parents=True, exist_ok=True)
        print(f"Downloading MediaPipe model to {destination}...")
        urllib.request.urlretrieve(MODEL_URL, destination)
        print("Download complete.")

    def _ensure_model(self) -> Path:
        if not MODEL_PATH.exists():
            self._download_model(MODEL_PATH)
        return MODEL_PATH

    def _open_camera(self) -> cv2.VideoCapture:
        for index in self.camera_indices:
            cap = cv2.VideoCapture(index)
            if not cap.isOpened():
                cap.release()
                continue

            for _ in range(5):
                success, frame = cap.read()
                if success and frame is not None:
                    print(f"Using camera index {index}")
                    return cap

            cap.release()

        raise RuntimeError(
            "Unable to open a working webcam. Try changing camera indices or grant camera permission."
        )

    def detect(self, frame: cv2.Mat) -> mp_vision.HandLandmarkerResult:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = mp_image.Image(mp_image.ImageFormat.SRGB, rgb)
        return self.hand_landmarker.detect(image)

    @staticmethod
    def extract_landmarks(
        frame: cv2.Mat,
        hand_landmarks: Any,
    ) -> Tuple[List[List[int]], Dict[int, Tuple[int, int]]]:
        height, width, _ = frame.shape
        lm_list: List[List[int]] = []
        landmarks: Dict[int, Tuple[int, int]] = {}

        for idx, landmark_point in enumerate(hand_landmarks):
            x = int(landmark_point.x * width)
            y = int(landmark_point.y * height)
            lm_list.append([idx, x, y])
            landmarks[idx] = (x, y)

        return lm_list, landmarks

    @staticmethod
    def draw_landmarks(
        frame: cv2.Mat,
        hand_landmarks: Any,
        landmarks: Dict[int, Tuple[int, int]],
    ) -> None:
        for connection in mp_vision.HandLandmarksConnections.HAND_CONNECTIONS:
            start = hand_landmarks[connection.start]
            end = hand_landmarks[connection.end]
            start_pt = (int(start.x * frame.shape[1]), int(start.y * frame.shape[0]))
            end_pt = (int(end.x * frame.shape[1]), int(end.y * frame.shape[0]))
            cv2.line(frame, start_pt, end_pt, (0, 255, 0), 2)

        for idx, (x, y) in landmarks.items():
            cv2.circle(frame, (x, y), 4, (0, 0, 255), -1)
            cv2.putText(
                frame,
                str(idx),
                (x + 4, y - 4),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                1,
            )

    def close(self) -> None:
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def __enter__(self) -> "HandDetector":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()
