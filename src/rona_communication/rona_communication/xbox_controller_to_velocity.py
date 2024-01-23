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

        self.vel_publisher = self.create_publisher(
            Float64MultiArray,
            '/simple_velocity_controller/commands', 
            10)
        
        self.vel_msg = Float64MultiArray()


    def joy_callback(self, joy_msg):
        linear_x = joy_msg.axes[1]  # Left joystick vertical axis. Up is positive and down is negative
        linear_y = joy_msg.axes[3]  # Left joystick horizontal axis. 
        angular_z = joy_msg.axes[0]  # Right joystick horizontal axis.
        # Your logic for mapping joystick values to robot velocities
        # Assuming a 4-wheeled omnidirectional robot with mecanum wheels

        #These values need to be parameters but are variables for now
        linear_vel = 0.6
        angular_vel = 2
        lenght = 0.15
        width = 0.09
        radius = 0.05

        #Filter to avoid the high sensitivity of the controller
        if (linear_x < 0.1) and (linear_x > (-0.1)):
            linear_x = 0.0
        if linear_y < 0.1 and linear_y > (-0.1):
            linear_y = 0.0
        if angular_z < 0.1 and angular_z > (-0.1):
            angular_z = 0.0
          
        #Here I multiply the desired velocity with the controller input, to have the correct spin direction of the wheels
        v_x = linear_vel*linear_x  # Forward/backward motion
        v_y = linear_vel*linear_y  # Sideways motion
        v_rot = angular_vel*angular_z  # Rotation in place

        # Assuming mecanum wheel configuration (front-left, front-right, rear-right, rear-left)
        # Using direct kinematics, the angular velocity for each wheel should be as follows
        velocities = [
            ((-(lenght)-width)*v_rot + v_x - v_y)/radius ,  # Front left wheel
            ((lenght + width)*v_rot + v_x + v_y)/radius ,  # Front right wheel
            ((lenght + width)*v_rot + v_x - v_y)/radius ,  # Rear right wheel
            ((-(lenght)-width)*v_rot + v_x + v_y)/radius    # Rear left wheel
        ]
        
        #Here the final velocities are published to the correct topic and printed in a terminal
        self.vel_msg.data = velocities
        self.get_logger().info(f'Published Velocities: {self.vel_msg.data}')
        self.vel_publisher.publish(self.vel_msg)

def main(args=None):
    rclpy.init(args=args)
    xbox_controller_node = XboxControllerNode()
    rclpy.spin(xbox_controller_node)
    xbox_controller_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
