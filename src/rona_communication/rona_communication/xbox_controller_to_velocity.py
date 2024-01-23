import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from std_msgs.msg import Float64MultiArray

class XboxControllerNode(Node):

    def __init__(self):

        super().__init__('xbox_controller_listener')

        self.subscription = self.create_subscription(
            Joy,
            '/joy',
            self.joy_callback,
            10)

        self.raw_vel_publisher = self.create_publisher(
            Float64MultiArray,
            '/kinematics_controller/commands', 
            10)
        
        self.raw_vel_msg = Float64MultiArray()


    def joy_callback(self, joy_msg):
        linear_x = joy_msg.axes[1]  # Left joystick vertical axis. Up is positive and down is negative
        linear_y = joy_msg.axes[3]  # Left joystick horizontal axis. 
        angular_z = joy_msg.axes[0]  # Right joystick horizontal axis.
        # Your logic for mapping joystick values to robot velocities
        # Assuming a 4-wheeled omnidirectional robot with mecanum wheels

        #Filter to avoid the high sensitivity of the controller
        if (linear_x < 0.1) and (linear_x > (-0.1)):
            linear_x = 0.0
        if linear_y < 0.1 and linear_y > (-0.1):
            linear_y = 0.0
        if angular_z < 0.1 and angular_z > (-0.1):
            angular_z = 0.0
          
        # Assuming mecanum wheel configuration (front-left, front-right, rear-right, rear-left)
        # Using direct kinematics, the angular velocity for each wheel should be as follows
        velocities = [
            linear_x ,  # Velocity in the X axis
            linear_y ,  # Velocity in the Y axis
            angular_z ,  # Angular velocity (Z axis)
        ]
        
        #Here the final velocities are published to the correct topic and printed in a terminal
        self.raw_vel_msg.data = velocities
        self.raw_vel_publisher.publish(self.raw_vel_msg)

def main(args=None):
    rclpy.init(args=args)
    xbox_controller_node = XboxControllerNode()
    rclpy.spin(xbox_controller_node)
    xbox_controller_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
