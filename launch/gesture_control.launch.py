from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    return LaunchDescription([
        Node(
            package='gesture_control',
            executable='gesture_node',
            name='gesture_control_node',
            output='screen'
        )
    ])
