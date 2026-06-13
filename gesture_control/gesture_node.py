import threading
from collections import deque

import cv2
import rclpy
from geometry_msgs.msg import TwistStamped
from rclpy.node import Node

from gesture_control.hand_detector import HandDetector
from gesture_control.gesture_classifier import GestureClassifier

import time


class GestureControlNode(Node):

    def __init__(self):
        super().__init__("gesture_control_node")

        self.current_velocity = (0.0, 0.0)

        self.current_fps = 0.0

        self.prev_frame_time = time.time()

        self.publisher = self.create_publisher(
            TwistStamped,
            "/cmd_vel",
            10
        )

        self.current_gesture = "STOP"

        self.detector = HandDetector()
        self.classifier = GestureClassifier()

        self.gesture_buffer = deque(maxlen=10)

        self.gesture_thread = threading.Thread(
            target=self.gesture_loop,
            daemon=True
        )
        self.gesture_thread.start()

        self.timer = self.create_timer(
            0.1,
            self.publish_cmd
        )

        self.get_logger().info(
            "Gesture Control Node Started"
        )

    def gesture_loop(self):
        while True:

            success, frame = self.detector.cap.read()

            if not success or frame is None:
                continue

            frame = cv2.flip(frame, 1)

            current_time = time.time()
            self.current_fps = (
                1.0 / max(current_time - self.prev_frame_time, 0.001)
            )
            self.prev_frame_time = current_time

            result = self.detector.detect(frame)

            if result.hand_landmarks:

                for hand_landmarks in result.hand_landmarks:

                    lm_list, landmarks = self.detector.extract_landmarks(
                        frame,
                        hand_landmarks
                    )

                    self.detector.draw_landmarks(
                        frame,
                        hand_landmarks,
                        landmarks
                    )

                    fingers = self.classifier.get_finger_states(
                        lm_list
                    )

                    gesture = self.classifier.classify(
                        fingers,
                        landmarks
                    )

                    self.gesture_buffer.append(gesture)

                    if self.gesture_buffer.count(gesture) > 7:

                        if gesture != self.current_gesture:

                            self.current_gesture = gesture

                            self.get_logger().info(
                                f"Gesture changed to: {gesture}"
                            )

                    break

            overlay = frame.copy()

            cv2.rectangle(
                overlay,
                (10, 10),
                (500, 260),
                (40, 40, 40),
                -1
            )

            cv2.addWeighted(
                overlay,
                0.6,
                frame,
                0.4,
                0,
                frame
            )

            gesture_color = {
                "FORWARD": (0, 255, 0),
                "BACKWARD": (255, 0, 0),
                "LEFT": (0, 255, 255),
                "RIGHT": (0, 255, 255),
                "STOP": (0, 165, 255),
                "EMERGENCY STOP": (0, 0, 255)
            }.get(self.current_gesture, (255, 255, 255))

            cv2.putText(
                frame,
                f"Gesture: {self.current_gesture}",
                (20, 45),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                gesture_color,
                2
            )

            command_text = {
                "FORWARD": "MOVE FORWARD",
                "BACKWARD": "MOVE BACKWARD",
                "LEFT": "TURN LEFT",
                "RIGHT": "TURN RIGHT",
                "STOP": "STOP",
                "EMERGENCY STOP": "EMERGENCY STOP"
            }.get(self.current_gesture, "UNKNOWN")

            cv2.putText(
                frame,
                f"Command: {command_text}",
                (20, 85),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            cv2.putText(
                frame,
                f"Linear Velocity: {self.current_velocity[0]:.2f} m/s",
                (20, 125),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"Angular Velocity: {self.current_velocity[1]:.2f} rad/s",
                (20, 165),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"FPS: {self.current_fps:.1f}",
                (20, 205),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 0, 255),
                2
            )

            cv2.putText(
                frame,
                "ROS2 Gesture Control",
                (20, 245),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            cv2.imshow(
                "Gesture Control Dashboard",
                frame
            )

            if cv2.waitKey(1) & 0xFF == 27:
                break


    def publish_cmd(self):
        msg = TwistStamped()

        msg.header.stamp = (
            self.get_clock().now().to_msg()
        )

        if self.current_gesture == "FORWARD":

            msg.twist.linear.x = 0.2

        elif self.current_gesture == "BACKWARD":

            msg.twist.linear.x = -0.2

        elif self.current_gesture == "LEFT":

            msg.twist.angular.z = 0.8

        elif self.current_gesture == "RIGHT":

            msg.twist.angular.z = -0.8

        elif self.current_gesture == "STOP":

            msg.twist.linear.x = 0.0
            msg.twist.angular.z = 0.0

        elif self.current_gesture == "EMERGENCY STOP":

            msg.twist.linear.x = 0.0
            msg.twist.angular.z = 0.0

        self.current_velocity = (
            msg.twist.linear.x,
            msg.twist.angular.z
        )

        self.publisher.publish(msg)



    def destroy_node(self):
        self.detector.close()
        cv2.destroyAllWindows()
        super().destroy_node()


def main(args=None):

    rclpy.init(args=args)

    node = GestureControlNode()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        node.get_logger().info(
            "Shutting down Gesture Control Node..."
        )

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()