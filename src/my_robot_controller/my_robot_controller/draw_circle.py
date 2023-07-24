#!/usr/bin/python3.8
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class DrawCircleNode(Node):
    def __init__(self):
        super().__init__("draw_circle")
        self.get_logger().info("Draw circle node has been started")
        #First we state the message type, then, the name of the topic we are publishing to and, lastly the queue size
        self.cmd_vel_pub_=self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.timer = self.create_timer(0.5, self.send_velocity_command)

    def send_velocity_command(self):
        msg = Twist() #First we create a message
        #Then we give values to the message
        msg.linear.x = 2.0
        msg.angular.z = 1.0
        #Then we publish the message
        self.cmd_vel_pub_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = DrawCircleNode()
    rclpy.spin(node)
    rclpy.shutdown()