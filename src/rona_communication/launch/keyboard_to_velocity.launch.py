from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    keyboard_to_velocity = Node(
        package="rona_communication",
        executable="keyboard_to_velocity"
    )

    return LaunchDescription([
        keyboard_to_velocity
    ])