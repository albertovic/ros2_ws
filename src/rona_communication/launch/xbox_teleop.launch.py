from launch import LaunchDescription
from launch_ros.actions import Node

import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    joy_params = os.path.join(get_package_share_directory('rona_communication'),'config','xbox_teleop.yaml')

    joy_node = Node(
            package='joy',
            executable='joy_node',
            parameters=[joy_params],
         )

    xbox_to_vel = Node(
        package="rona_communication",
        executable="xbox_controller_to_velocity",
    )

    direct_kinematics = Node(
        package="rona_communication",
        executable="direct_kinematics_node",
    )            

    return LaunchDescription([
        joy_node,
        xbox_to_vel,
        direct_kinematics    
    ])