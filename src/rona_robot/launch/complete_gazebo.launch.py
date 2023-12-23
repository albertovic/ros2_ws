from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
import os
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node



def generate_launch_description():

    gazebo_and_config = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(get_package_share_directory("rona_robot"), "launch", "gazebo_and_config.launch.py")
    ))

    keyboard_to_velocity = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(get_package_share_directory("rona_communication"), "launch", "keyboard_to_velocity.launch.py")
    ))


    return LaunchDescription([
        gazebo_and_config,
        keyboard_to_velocity
    ])