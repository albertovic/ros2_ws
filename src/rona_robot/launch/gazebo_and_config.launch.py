#This file launches the gazebo related launchfile "gazebo.launch.py" and the spawner launchfile 
#"controller.launch.py" from the rona_controller package. The spawn of the controllers configures them thanks to the code
#from "rona_gazebo.xacro"

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
import os
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource



def generate_launch_description():

    config_launch_file = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(get_package_share_directory("rona_controller"), "launch", "controller.launch.py")
    ))

    gazebo_launch = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(get_package_share_directory("rona_robot"), "launch", "gazebo.launch.py")
    ))

    return LaunchDescription([
        gazebo_launch,
        config_launch_file
    ])