# ros2_ws (English)

## Introduction
This repository contains certain packages that I have been developing throughout my learning of ROS2. It includes part of the development of my Bachelor's Thesis on underwater communications.

## RONA
In this section, you will find packages related to the development of an Autonomous Omnidirectional Navigation Robot (RONA). The idea is to create a physical robot that can perform autonomous navigation using a LIDAR. At the moment, I am focusing on learning how to program simulations and simulating the robot in Gazebo.

### rona_robot
This is the main package for modeling RONA. The Gazebo simulation is already functional, and the robot can be moved using the keyboard. Code for navigation and sensor data collection, which I do not yet have, is yet to be developed.

### rona_controller
This package is primarily used for configuring controllers and spawning them.

### rona_communication
This package is used to convert keyboard key presses into velocity commands for the robot. It transforms Twist messages from the teleop_twist_keyboard node into Float64MultiArray messages to be sent to the `/simple_velocity_controller/commands` topic, which carries velocity commands to the robot.

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

##Introducción
Este repositorio contiene ciertos paquetes que he ido desarrollando a lo largo de mi aprendizaje de ROS2. Contiene parte del desarrollo de mi TFG sobre comunicaciones submarinas

##RONA
En esta sección se encuentran los paquetes relacionados con el desarollo de un Robot Omindireccional de Navegación Autónoma (RONA). La idea es hacer un robot físico que, mediante un LIDAR, pueda realizar navegación autónoma. Por el momento, me estoy limitando a aprender a programar las simulaciones y a simular el robot en Gazebo.

###rona_robot
Es el paquete principal para el modelado de RONA. Ya funciona la simulación en gazebo y se puede mover el robot utilizando el teclado. Falta por desarrollar código para navegación y recolección de datos de sensores que aún no tengo.

###rona_controller
Este paquete se usa principalmente para configuración de controladores y para spawnearlos.

###rona_communication
Este paquete se usa para convertir las pulsaciones de las teclas del teclado en comandos de velocidad para el robot. Pasa de un mensaje Twist del nodo teleop_twist_keyboard a un mensaje Float64MultiArray para poder mandarlo al topic 
/simple_velocity_controller/commands, el cual es el que lleva los comandos de velocidad al robot.

###simple_rona_robot
Es un paquete que ahora mismo no estoy usando, era otro enfoque para resolver el problema del robot omnidireccional, sin entrar en la complejidad de modelar las ruedas con detalle, pero como la primera opción parece funcionar correctamente prefiero seguir con esa

##Otros paquetes 

###py_pubsub
Este paquete lo he utilizado para hacer pruebas sobre publicadores y suscriptores con mensajes personalizados. Contiene dos parejas de publicador/suscriptor:
- La primera de ellas no recoge información de ningún sensor externo, sino que el publicador va dando datos según una variable que crece con el tiempo. El publicador se llama con </ros2 run py_pubsub talker> y el subscriptor con </ros2 run py_pubsub listener>.
- La segunda compila pero falta por probarla con los sensores físicos. Esta sí recoge la información de los sensores reales y la manda con un mensaje personalizado. Está hecho para que funcione con los sensores de mi TFG. El prublicador se llama con </ros2 run py_pubsub publisher_sensors> añadiendo los flags necesarios con la dirección del archivo de lectura de los datos del echosounder </--device AMA...>. Y el subscriptor con </ros2 run py_pubsub subscriber_sensors -f file.log>. En este caso se indica el path del archivo en el que se quiere que se guarde la información leída.
       
###tutorial_interfaces
Este paquete contiene la información de los mensajes personalizados mencionados en py_pubsub.

###sensors_modules
Este paquete contiene las librerías necesarias para leer correctamente los sensores en el publicador de py_pubsub. Se ha generado una dependencia de py_pubsub sobre este paquete y así se ha conseguido hacer la importación de las librerías sin tener que modificar a mano la carpeta install.