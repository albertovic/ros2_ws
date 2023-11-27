import rclpy
from rclpy.node import Node
from rclpy.logging import get_logger
from std_msgs.msg import String
import logging


class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback, #this function will always be called with the message as an argument
            10)
        self.subscription #prevent unussed variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)

def main(args=None):
    rclpy.init(args=args)

    logging_file_path = 'file.log'

    minimal_subscriber = MinimalSubscriber()
    minimal_subscriber.get_logger().set_handler_by_name('file', filename=logging_file_path) #logging.INFO es para ajustar el nivel de registro
    #puede ser logging.INFO, logging.WARNING, logging.ERROR, etc.    
    rclpy.spin(minimal_subscriber)

    minimal_subscriber.destroy_node()
    rclpy.shutdown()