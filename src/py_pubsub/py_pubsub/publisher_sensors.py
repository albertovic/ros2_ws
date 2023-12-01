#IMPORTS BEGIN
#-------------------------------
#Imports for temperature sensor
from sensors_modules import tsys01

#Imports for pressure sensor
#import sensor_codes.multiple_sensors_pkg.examples.ms5837 as ms5837
from sensors_modules import ms5837
#Imports for echosounder sensor (altimeter)
from brping import Ping1D

#Sometimes these commands are needed
# pip uninstall bluerobotics-ping
# pip install bluerobotics-ping



#Common imports
import rclpy
from rclpy.node import Node
from tutorial_interfaces.msg import Sensors
import argparse 
#-------------------------------
#IMPORTS END

#We create a class thath inherits from (or is a subclass of) the Node class.
class MinimalPublisher(Node):

    def __init__(self, args, temp_sensor, press_sensor, echo_sensor):

        self.arguments = args
        self.temp_sensor = temp_sensor
        self.press_sensor = press_sensor
        self.echo_sensor = echo_sensor

        #This calls the Node class constructor and gives the node a name
        super().__init__('sensor_publisher')
        #This line creates and configures the publisher. Declares that the node publishes messages of tipe String over a topic named topic
        # and that the queue size is 10. This limits the amount of queued messages if a subscriber is not receiving them fast enough
        self.publisher_ = self.create_publisher(Sensors, 'sensors_info', 10)

        #Next a timer is created witb a callback to execute every 0.5 seconds
        timer_period = 1 #seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    #The next step is creating the timer callback, which creates a message and publishes it
    def timer_callback(self):

        msg = Sensors()

        #Opens the file containing the temperature
        f = open('/sys/class/thermal/thermal_zone0/temp', 'r')
        #Reads the temperature in milicelsius
        temp_int = float(f.read().strip())
        #Converts temperature to Celsius
        msg.in_temp = temp_int / 1000.0


        #Temperature sensor reading
        if not self.temp_sensor.read():
            print("Error reading temperature sensor")
            exit(1)
        else:
            msg.temp_temp = self.temp_sensor.temperature()

        #Pressure sensor reading
        if not self.press_sensor.read():    #he cambiado a grados C por defecto en el sensor pressure, si queremos otra unidad sensor.pressure(UNITS_psi)
            print("Error reading pressure sensor")
            exit(1)
        else:
            msg.press_temp = self.press_sensor.temperature()
            msg.press = self.press_sensor.pressure()

        #Echosounder sensor reading
        data = self.echo_sensor.get_distance()
        if data:
            msg.distance = data["distance"]
            msg.confidence = data["confidence"]
        else:
            print("Error reading echosounder sensor")
        

        self.publisher_.publish(msg)

        #This shows the message at the console
        self.get_logger().info('Publishing: "%d"' % self.i)
        self.i += 1


def parse_arguments():
    parser = argparse.ArgumentParser(description="Ping python library example.")
    parser.add_argument('--device', action="store", required=False, type=str, help="Ping device port. E.g: /dev/ttyUSB0")
    parser.add_argument('--baudrate', action="store", type=int, default=115200, help="Ping device baudrate. E.g: 115200")
    parser.add_argument('--udp', action="store", required=False, type=str, help="Ping UDP server. E.g: 192.168.2.2:9090")
    args = parser.parse_args()
    if args.device is None and args.udp is None:
        parser.print_help()
        exit(1)
    return parser.parse_args()
    

def main(args=None):
    rclpy.init(args=args)

    parsed_args = parse_arguments()

    #CREATION OF THE SENSORS OBJECTS BEGIN
    #-------------------------------
    temp_sensor = tsys01.TSYS01(6) #We need to specify the rapberry bus (6). 
    #The bus number can be obtained using the command i2cdetect -y 6

    press_sensor = ms5837.MS5837_30BA(6) #This object creation lets us specify the model and the bus number

    echo_sensor = Ping1D()
    if parsed_args.device is not None:
        echo_sensor.connect_serial(parsed_args.device, parsed_args.baudrate)
    elif parsed_args.udp is not None:
        (host, port) = parsed_args.udp.split(':')
        echo_sensor.connect_udp(host, int(port))
    #-------------------------------
    #END OF SENSORS OBJECTS CREATION

    #OBJECT CREATION ERROR TREATMENT BEGIN
    #-------------------------------
    if not temp_sensor.init():
        print("Temperature sensor could not be initialized")
        exit(1)

    if not press_sensor.init():
        print("Pressure sensor could not be initialized")
        exit(1)

    if echo_sensor.initialize() is False:
        print("Echosounder sensor could not be initialized")
        exit(1)
    #-------------------------------
    #END OF OBJECT CREATION ERROR TREATMENT

    minimal_publisher = MinimalPublisher(parsed_args, temp_sensor, press_sensor, echo_sensor)

    rclpy.spin(minimal_publisher)

    minimal_publisher.destroy_node()
    rclpy.shutdown()
