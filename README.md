# ros2_ws (English)

## Introduction
This repository contains certain packages that I have been developing throughout my learning of ROS2. It includes part of the development of my Bachelor's Thesis on underwater communications and other projects, such as RONA.

## RONA
In this section, you will find packages related to the development of an Autonomous Omnidirectional Navigation Robot (RONA). The idea is to create a physical robot that can perform autonomous navigation using a LIDAR. At the moment, I am focusing on learning how to program simulations and simulating the robot in Gazebo.

### rona_robot
This is the main package for modeling RONA. The Gazebo simulation is already functional with a LIDAR sensor, and the robot can be moved using the keyboard or an Xbox controller (with direct kinematics control). Code for navigation and sensor data collection, which I do not yet have, is yet to be developed.

To run the keyboard control use this command:
`ros2 launch rona_robot complete_gazebo.launch.py`
and
`ros2 run teleop_twist_keyboard teleop_twist_keyboard`

To run the Xbox controller control use this command:
`ros2 launch rona_robot xbox_complete_gazebo.launch.py`

### rona_controller
This package is primarily used for configuring controllers and spawning them.

### rona_communication
This package contains these nodes: 
- keyboard_to_velocity.py: converts keyboard key presses into velocity commands for the robot. It transforms Twist messages from the teleop_twist_keyboard node into Float64MultiArray messages to be sent to the `/simple_velocity_controller/commands` topic, which carries velocity commands to the robot.
- xbox_controller_to_velocity.py: subscribes to the `/joy` topic and converts joy messages into velocity commands. These messages are then published into `/kinematics_controller/command` topic. The velocity commands will be of Float64MultiArray type and will have this structure: [velocity_X_axis, velocity_Y_axis, angular_velocity]. Each of them will range from -1 to 1.
- direct_kinematics_node.py: This node will subscribe to the `/kinematics_controller/command` topic and transform the velocity messages to wheel speeds. This messages NEED to be in the mentioned format [velocity_X_axis, velocity_Y_axis, angular_velocity]. Each of them will range from -1 to 1. After the transformation, the new message is published into `/simple_velocity_controller/commands` topic.

### simple_rona_robot
This package is currently not in use; it was another approach to solve the omnidirectional robot problem without going into the complexity of modeling wheels in detail. Since the first option seems to work correctly, I prefer to continue with that.

## Other Packages

### py_pubsub
I have used this package for testing publishers and subscribers with custom messages. It contains two pairs of publisher/subscriber:
- The first one does not collect information from any external sensor; instead, the publisher provides data based on a variable that increases over time. The publisher is called with `ros2 run py_pubsub talker`, and the subscriber with `ros2 run py_pubsub listener`.
- The second one compiles but has yet to be tested with physical sensors. This one collects information from real sensors and sends it with a custom message. It is designed to work with the sensors from my Bachelor's Thesis. The publisher is called with `ros2 run py_pubsub publisher_sensors`, adding the necessary flags with the file reading data from the echosounder `--device AMA...`. The subscriber is called with `ros2 run py_pubsub subscriber_sensors -f file.log`. In this case, the path of the file where you want to save the read information is indicated.

### tutorial_interfaces
This package contains information on the custom messages mentioned in py_pubsub.

### sensors_modules
This package contains the necessary libraries to correctly read sensors in the py_pubsub publisher. A dependency of py_pubsub on this package has been created, allowing the libraries to be imported without manually modifying the install folder.


# ros2_ws (Español)

## Introducción
Este repositorio contiene ciertos paquetes que he ido desarrollando a lo largo de mi aprendizaje de ROS2. Incluye parte del desarrollo de mi Trabajo de Fin de Grado (TFG) sobre comunicaciones submarinas, además de otros proyectos como RONA.

## RONA
En esta sección se encuentran los paquetes relacionados con el desarrollo de un Robot Omnidireccional de Navegación Autónoma (RONA). La idea es crear un robot físico que, mediante un LIDAR, pueda realizar navegación autónoma. Por el momento, me estoy limitando a aprender a programar simulaciones y a simular el robot en Gazebo.

### rona_robot
Es el paquete principal para el modelado de RONA. La simulación en Gazebo ya funciona, y el robot se puede mover utilizando el teclado. Falta desarrollar código para la navegación y la recolección de datos de sensores que aún no tengo.

### rona_controller
Este paquete se usa principalmente para la configuración de controladores y para spawnearlos.

### rona_communication
Este paquete se utiliza para convertir las pulsaciones de las teclas del teclado en comandos de velocidad para el robot. Transforma mensajes Twist del nodo teleop_twist_keyboard a mensajes Float64MultiArray para enviarlos al topic `/simple_velocity_controller/commands`, que lleva los comandos de velocidad al robot.

### simple_rona_robot
Es un paquete que actualmente no estoy utilizando; era otro enfoque para resolver el problema del robot omnidireccional, sin entrar en la complejidad de modelar las ruedas con detalle. Como la primera opción parece funcionar correctamente, prefiero seguir con esa.

## Otros paquetes 

### py_pubsub
Este paquete lo he utilizado para hacer pruebas sobre publicadores y suscriptores con mensajes personalizados. Contiene dos parejas de publicador/suscriptor:
- La primera de ellas no recoge información de ningún sensor externo; el publicador proporciona datos según una variable que crece con el tiempo. El publicador se llama con `ros2 run py_pubsub talker` y el subscriptor con `ros2 run py_pubsub listener`.
- La segunda compila pero falta por probarla con los sensores físicos. Esta sí recoge la información de los sensores reales y la envía con un mensaje personalizado. Está diseñada para funcionar con los sensores de mi TFG. El publicador se llama con `ros2 run py_pubsub publisher_sensors`, agregando los flags necesarios con la dirección del archivo de lectura de los datos del echosounder `--device AMA...`. Y el subscriptor con `ros2 run py_pubsub subscriber_sensors -f file.log`. En este caso, se indica la ruta del archivo en el que se quiere que se guarde la información leída.
       
### tutorial_interfaces
Este paquete contiene la información de los mensajes personalizados mencionados en py_pubsub.

### sensors_modules
Este paquete contiene las librerías necesarias para leer correctamente los sensores en el publicador de py_pubsub. Se ha generado una dependencia de py_pubsub sobre este paquete, permitiendo la importación de las librerías sin tener que modificar manualmente la carpeta install.