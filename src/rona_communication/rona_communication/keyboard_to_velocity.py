import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64MultiArray

import argparse

class KeyboardNode(Node):
    #In this innit function, a path for the logger file is shared
    
    def __init__(self):
        super().__init__('keyboard_listener')

        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.listener_callback, #this function will always be called with the message as an argument
            10)

        self.vel_publisher_ = self.create_publisher(
            Float64MultiArray, 
            '/simple_velocity_controller/commands', 
            10)
        self.vel_msg = Float64MultiArray()

        self.subscription #prevent unussed variable warning

    def keyboard_to_velocity(self, keyboard_msg):


        linear_x = keyboard_msg.linear.x
        linear_y = keyboard_msg.linear.y
        abs_linear_y = abs(linear_y)
        angular_z = keyboard_msg.angular.z
        abs_angular_z = abs(angular_z)

        self.get_logger().info(f'Twist Values: linear_x={linear_x}, linear_y={linear_y}, angular_z={angular_z}')

        if linear_x != 0.0 and angular_z == 0.0:
            velocities = [linear_x, linear_x, linear_x, linear_x]
        elif linear_x == 0.0 and linear_y > 0.0 and angular_z == 0.0:
            velocities = [-abs_linear_y, abs_linear_y, abs_linear_y, -abs_linear_y]
        elif linear_x == 0.0 and linear_y < 0.0 and angular_z == 0.0:
            velocities = [abs_linear_y, -abs_linear_y, -abs_linear_y, abs_linear_y]
        #Turn anti-clockwise
        elif linear_x == 0.0 and linear_y == 0.0 and angular_z > 0.0:
            velocities = [-abs_angular_z, abs_angular_z, -abs_angular_z, abs_angular_z]
        #Turn clockwise
        elif linear_x == 0.0 and linear_y == 0.0 and angular_z < 0.0:
            velocities = [abs_angular_z, -abs_angular_z, abs_angular_z, -abs_angular_z]
        #Complete stop
        else:
            velocities = [0.0, 0.0, 0.0, 0.0]

        # Define a dictionary to map conditions to velocities
        # conditions_to_velocities = {
        #     (linear_x > 0.0, linear_y == 0.0, angular_z == 0.0): [linear_x, linear_x, linear_x, linear_x],  # Move forward
        #     (linear_x < 0.0, linear_y == 0.0, angular_z == 0.0): [linear_x, linear_x, linear_x, linear_x],  # Move backward
        #     # (linear_x == 0.0, linear_y == 0.0, angular_z > 0.0): [0.0, 0.0, angular_z, 0.0],  # Rotate clockwise
        #     # (linear_x == 0.0, linear_y == 0.0, angular_z < 0.0): [0.0, 0.0, angular_z, 0.0],  # Rotate counterclockwise
        #     (True, True, True): [0.0, 0.0, 0.0, 0.0],  # Default (stop)
        # }          

        # self.get_logger().info(f'Conditions: {(linear_x > 0.0, linear_y == 0.0, angular_z == 0.0)}')

        # matched_condition = next((cond for cond, vel in conditions_to_velocities.items() if cond), None)
        # self.get_logger().info(f'Matched Condition: {matched_condition}')

        # velocities = conditions_to_velocities.get(matched_condition, [0.0, 0.0, 0.0, 0.0])


        self.vel_msg.data = velocities

        self.get_logger().info(f'Published Velocities: {self.vel_msg.data}')

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: {msg.linear.x}, {msg.linear.y}, {msg.linear.z}, {msg.angular.x}, {msg.angular.y}, {msg.angular.z}')
        self.keyboard_to_velocity(msg)
        self.vel_publisher_.publish(self.vel_msg)


def main(args=None):
    rclpy.init(args=args)
    keyboard_node = KeyboardNode()
    rclpy.spin(keyboard_node)
    keyboard_node.destroy_node()
    rclpy.shutdown()