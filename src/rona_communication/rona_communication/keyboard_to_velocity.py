#This node has a subscriptor to the /cmd_vel topic (message type = Twist).
#The Twist messages from that topic are then converted to Float64MultiArray messages and sent to another
# topic via a publisher. The new topic is the one that sends info to the robot so it can move.

#Recap: This node receives certain info from keyboard input and transforms it to velocity commands for the robot.

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64MultiArray

import argparse

class KeyboardNode(Node):


    #In the inicialization function, a subscriber and a publisher are created, as well as a variable called vel_msg.
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

    #This function is the main one, in charge of receiveing a message from the keyboard input and publish it to a 
    # topic in charge of sending velocity commands to the actuators
    def keyboard_to_velocity(self, keyboard_msg):


        linear_x = keyboard_msg.linear.x
        abs_linear_x = abs(linear_x)
        linear_y = keyboard_msg.linear.y
        abs_linear_y = abs(linear_y)
        angular_z = keyboard_msg.angular.z
        abs_angular_z = abs(angular_z)

        self.get_logger().info(f'Twist Values: linear_x={linear_x}, linear_y={linear_y}, angular_z={angular_z}')
        #Movement forward/backward
        if linear_x != 0.0 and linear_y == 0.0 and angular_z == 0.0:
            velocities = [linear_x, linear_x, linear_x, linear_x]     
        #Movement to the right
        elif linear_x == 0.0 and linear_y > 0.0 and angular_z == 0.0:
            velocities = [-abs_linear_y, abs_linear_y, abs_linear_y, -abs_linear_y]
        #Movement to the right
        elif linear_x == 0.0 and linear_y < 0.0 and angular_z == 0.0:
            velocities = [abs_linear_y, -abs_linear_y, -abs_linear_y, abs_linear_y]
        #Turn anti-clockwise
        elif linear_x == 0.0 and linear_y == 0.0 and angular_z > 0.0:
            velocities = [-abs_angular_z, abs_angular_z, -abs_angular_z, abs_angular_z]
        #Turn clockwise
        elif linear_x == 0.0 and linear_y == 0.0 and angular_z < 0.0:
            velocities = [abs_angular_z, -abs_angular_z, abs_angular_z, -abs_angular_z]
        #Movement up to the left
        elif linear_x > 0.0 and linear_y == 0.0 and angular_z > 0.0:
            velocities = [abs_linear_x, 0.0, 0.0, abs_linear_x]
        #Movement up to the right
        elif linear_x > 0.0 and linear_y == 0.0 and angular_z < 0.0:
            velocities = [0.0, abs_linear_x, abs_linear_x, 0.0]
        #Complete stop
        else:
            velocities = [0.0, 0.0, 0.0, 0.0]


        self.vel_msg.data = velocities

        self.get_logger().info(f'Published Velocities: {self.vel_msg.data}')

    #This function is the callback for the subscriber. It calls the transformation function and then publishes the 
    # transformed message to another topic
    def listener_callback(self, msg):
        #self.get_logger().info(f'I heard: {msg.linear.x}, {msg.linear.y}, {msg.linear.z}, {msg.angular.x}, {msg.angular.y}, {msg.angular.z}')
        self.keyboard_to_velocity(msg)
        self.vel_publisher_.publish(self.vel_msg)


def main(args=None):
    rclpy.init(args=args)
    keyboard_node = KeyboardNode()
    rclpy.spin(keyboard_node)
    keyboard_node.destroy_node()
    rclpy.shutdown()