import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
# This node transforms the desired movement from velocity in X axis, velocity in Y axis and angular velocity to the 
# individual velocity of each wheel and send that to the velocity controller of RONA
class DirectKinematicsController(Node):

    def __init__(self):

        super().__init__('direct_kinematics_controller')

        self.subscription = self.create_subscription(
            Float64MultiArray,
            '/kinematics_controller/commands',
            self.kinematics_callback,
            10)

        self.vel_publisher = self.create_publisher(
            Float64MultiArray,
            '/simple_velocity_controller/commands', 
            10)
        
        self.vel_msg = Float64MultiArray()

    def kinematics_callback(self, kinematics_msg):
        linear_x = kinematics_msg.data[0]
        linear_y = kinematics_msg.data[1]
        angular_z = kinematics_msg.data[2]

        #These values need to be parameters but are variables for now
        linear_vel = 0.6
        angular_vel = 2
        lenght = 0.15
        width = 0.09
        radius = 0.05

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

        self.vel_msg.data = velocities
        self.vel_publisher.publish(self.vel_msg)

def main(args=None):
    rclpy.init(args=args)
    kinematics_controller_node = DirectKinematicsController()
    rclpy.spin(kinematics_controller_node)
    kinematics_controller_node.destroy_node()
    rclpy.shutdown()