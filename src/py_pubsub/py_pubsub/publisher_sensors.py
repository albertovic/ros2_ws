import rclpy
from rclpy.node import Node

from tutorial_interfaces.msg import Sensors

#We create a class thath inherits from (or is a subclass of) the Node class.
class MinimalPublisher(Node):

    def __init__(self):
        #This calls the Node class constructor and gives the node a name
        super().__init__('minimal_publisher')
        #This line creates and configures the publisher. Declares that the node publishes messages of tipe String over a topic named topic
        # and that the queue size is 10. This limits the amount of queued messages if a subscriber is not receiving them fast enough
        self.publisher_ = self.create_publisher(Sensors, 'topic', 10)

        #Next a timer is created witb a callback to execute every 0.5 seconds
        timer_period = 0.5 #seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    #The next step is creating the timer callback, which creates a message and publishes it
    def timer_callback(self):
        msg = Sensors()
        msg.in_temp = float(self.i + 1)
        msg.temp_temp = float(self.i + 2)
        msg.press = float(self.i + 0.5)
        msg.press_temp = float(self.i + 2*self.i)
        msg.distance = 'Distancia'
        msg.confidence = 'Confiante'
        self.publisher_.publish(msg)

        #This shows the message at the console
        self.get_logger().info('Publishing: "%d"' % self.i)
        self.i += 1
    
    
def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    minimal_publisher.destroy_node()
    rclpy.shutdown()
