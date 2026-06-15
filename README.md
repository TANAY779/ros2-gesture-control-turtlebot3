# ROS2 Gesture Control for TurtleBot3

Real-time hand gesture control of TurtleBot3 Burger in Gazebo using MediaPipe, OpenCV and ROS2 Jazzy.

![Demo](docs/demo.gif)


## Results

The system was successfully validated in Gazebo Harmonic using TurtleBot3 Burger simulation.

### Achievements

- Real-time hand tracking using MediaPipe
- Stable gesture recognition using temporal filtering
- ROS2 TwistStamped command publishing
- Real-time dashboard with FPS monitoring
- End-to-end gesture-to-robot control pipeline
- Gesture-controlled TurtleBot3 navigation in Gazebo

### Performance

- 21-point hand landmark detection
- Low-latency gesture recognition
- Real-time command execution
- Visual feedback dashboard


## Dashboard

The system includes a real-time visual dashboard displaying:

- Hand landmarks
- Detected gesture
- Robot command
- Linear velocity
- Angular velocity
- FPS counter

![Dashboard](docs/dashboard.png)

---

## System Architecture

![Architecture](docs/architecture.png)

The system converts hand gestures into robot motion commands through a ROS2 pipeline.

```text
Webcam
   ↓
MediaPipe Hand Detection
   ↓
Landmark Extraction
   ↓
Gesture Classification
   ↓
ROS2 Gesture Node
   ↓
TwistStamped Commands
   ↓
ros_gz_bridge
   ↓
TurtleBot3 Gazebo
```

---

## Features

- Real-time hand tracking using MediaPipe
- 21-point hand landmark extraction
- Custom gesture classification
- Gesture stabilization using temporal filtering
- ROS2 Jazzy integration
- TurtleBot3 Burger control in Gazebo
- Real-time OpenCV dashboard
- Emergency stop functionality
- TwistStamped command publishing

---

## Supported Gestures

| Gesture | Action |
|----------|----------|
| 👍 Thumb Up | Move Forward |
| 👎 Thumb Down | Move Backward |
| 👈 Point Left | Turn Left |
| 👉 Point Right | Turn Right |
| ✋ Open Palm | Stop |
| ✊ Fist | Emergency Stop |

---

## Technologies Used

- Python
- OpenCV
- MediaPipe
- ROS2 Jazzy
- Gazebo Harmonic
- TurtleBot3 Burger

---

## Skills Demonstrated

- ROS2 Jazzy
- Gazebo Harmonic
- Computer Vision
- MediaPipe
- Human-Robot Interaction
- Robot Teleoperation
- Real-Time Systems
- Python Development
- Robotics Middleware

---

## Installation

### Clone Repository

```bash
git clone https://github.com/TANAY779/ros2-gesture-control-turtlebot3.git

cd ros2-gesture-control-turtlebot3
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Build ROS2 Package

```bash
colcon build --packages-select gesture_control

source install/setup.bash
```

---

## Running the Project

### Launch TurtleBot3 Simulation

```bash
export TURTLEBOT3_MODEL=burger

ros2 launch turtlebot3_gazebo empty_world.launch.py
```

### Run Gesture Control Node

```bash
ros2 launch gesture_control gesture_control.launch.py
```

---

## Project Structure

```text
ros2-gesture-control-turtlebot3/
│
├── gesture_control/
│   ├── hand_detector.py
│   ├── gesture_classifier.py
│   └── gesture_node.py
│
├── docs/
│   ├── demo.gif
│   ├── architecture.png
│   └── dashboard.png
│
├── README.md
├── requirements.txt
├── LICENSE
└── .gitignore
```

---

## Future Improvements

- Dynamic gesture recognition
- Nav2 integration
- Gesture-based waypoint selection
- Real robot deployment
- Gesture-based mode switching

---

## Demo Environment

- Ubuntu 24.04
- ROS2 Jazzy
- Gazebo Harmonic
- TurtleBot3 Burger (Simulation)

---

## Author

**Tanay Baisware**

