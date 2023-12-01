import rclpy
from rclpy.node import Node
from tutorial_interfaces.msg import Sensors

import argparse

class MinimalSubscriber(Node):
    #In this innit function, a path for the logger file is shared
    def __init__(self, file_path):
        super().__init__('sensors_msubscriber')

        self.subscription = self.create_subscription(
            Sensors,
            'sensors_info',
            self.listener_callback, #this function will always be called with the message as an argument
            10)
        
        self.subscription #prevent unussed variable warning

        #We create a self.f so that other functions can use this variable, and open it in writing text mode
        #This mode allows us to truncate the file when we open it
        self.f = open(file_path, mode="wt")
        #print(file_path)

    def listener_callback(self, msg):
        self.get_logger().info('I heard: \n Inner temperature: %f\n Temperature: %f\n Pressure: %f\n Temp_Pressure: %f\n Distance: %s\n Confidence: %s\n' % (msg.in_temp, msg.temp_temp, msg.press, msg.press_temp, msg.distance, msg.confidence))
        try:
            self.f.write('I heard: \n Inner temperature: %f\n Temperature: %f\n Pressure: %f\n Temp_Pressure: %f\n Distance: %s\n Confidence: %s\n\n\n' % (msg.in_temp, msg.temp_temp, msg.press, msg.press_temp, msg.distance, msg.confidence))
        except Exception as e:
            self.get_logger().error(f"Error writing to file: {e}")

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