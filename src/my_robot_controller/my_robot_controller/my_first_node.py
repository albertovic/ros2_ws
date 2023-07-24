#!/usr/bin/python3.8
import rclpy

from rclpy.node import Node

#We define a class MyNode that inherits from the Node class of rclpy
class MyNode(Node):
    #Create a constructor
    def __init__(self):
        #we call the constructor of the upper class (Node). In here we need to provide the node name we are going to be
        #using outside the programming environment (rqt_graph, for example)
        super().__init__("first_node")
        self.get_logger().info("Hello from ROS2")
        self.create_timer(1.0, self.timer_callback)
        self.counter_ = 0

    def timer_callback(self):
        self.get_logger().info("Hello " + str(self.counter_))
        self.counter_ += 1


def main(args=None):
    #Inicialize the communications
    rclpy.init(args=args)
    #We will create a node INSIDE the main function. We need a class that is inherited from the node class of rclpy
    node = MyNode()
    #When you make a node spin, the node will run indefinitely until we kill it
    rclpy.spin(node)
    #This has to be the last line of the function. It will destroy the node and shut down the communications
    rclpy.shutdown()

#This basically makes possible to run the code directly from the terminal. If we call it from the terminal, the if
# condition will be validated and whatever is below it will be executed

if __name__ == '__main__':
    main()