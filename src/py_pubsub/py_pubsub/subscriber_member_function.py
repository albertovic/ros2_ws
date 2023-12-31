import rclpy
from rclpy.node import Node
from tutorial_interfaces.msg import Num
import logging
import argparse

class MinimalSubscriber(Node):
    #In this innit function, a path for the logger file is shared
    def __init__(self, file_path):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            Num,
            'topic',
            self.listener_callback, #this function will always be called with the message as an argument
            10)
        self.subscription #prevent unussed variable warning

        #We create a self.f so that other functions can use this variable, and open it in writing text mode
        #This mode allows us to truncate the file when we open it
        self.f = open(file_path, mode="wt")
        #print(file_path)

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%d"' % msg.num)
        self.f.write('I heard: "%d"' % msg.num + "\n")

#This function takes the arguments the script is called with and returns them
def parse_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-f', '--file_path', help='logger file name', default='file.log')
    return arg_parser.parse_args()


def main(args=None):
    rclpy.init(args=args)

    #Here, the arguments are parsed and then the ones needed are selected
    parsed_args = parse_args()
    logging_file_path = parsed_args.file_path

    #After selecting the needed arguments, they are passed to the Node constructor. This way, the file is opened in the __init__ function
    minimal_subscriber = MinimalSubscriber(logging_file_path)

    rclpy.spin(minimal_subscriber)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()