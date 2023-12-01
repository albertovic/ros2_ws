# ros2_ws

## Introducción
Este repositorio contiene ciertos paquetes que he ido desarrollando a lo largo de mi aprendizaje de ROS2. Contiene parte del desarrollo de mi TFG sobre comunicaciones submarinas

## my_robot_controller
Este paquete lo utilicé para aprender un poco las cosas básicas de ROS2, como la creación de nodos y la comunicación con mensajes.

## rona_robot
Este paquete está a medias. Se supone que es un paquete de un Robot Omindireccional de Navegación Autónoma (RONA). Aquí falta por conseguir que los URDF funcionen en Gazebo y desarrollar código para navegación y recolección de datos de sensores que aún no tengo.

## py_pubsub
Este paquete lo he utilizado para hacer pruebas sobre publicadores y suscriptores con mensajes personalizados. Contiene dos parejas de publicador/suscriptor:
- La primera de ellas no recoge información de ningún sensor externo, sino que el publicador va dando datos según una variable que crece con el tiempo.

  El publicador se llama con:
  ```ruby
  ros2 run py_pubsub talker
  ```
  y el subscriptor con:
  ```ruby
  ros2 run py_pubsub listener
  ```
  
- La segunda compila pero falta por probarla con los sensores físicos. Esta sí recoge la información de los sensores reales y la manda con un mensaje personalizado. Está hecho para que funcione con los sensores de mi TFG.
  El prublicador se llama con:
  ```ruby
  ros2 run py_pubsub publisher_sensors
  ```
  añadiendo los flags necesarios con la dirección del archivo de lectura de los datos del echosounder --device AMA...

  y el subscriptor con:
  ```ruby
  ros2 run py_pubsub subscriber_sensors -f file.log
  ```
  En este caso se indica el path del archivo en el que se quiere que se guarde la información leída.
       
## tutorial_interfaces
Este paquete contiene la información de los mensajes personalizados mencionados en py_pubsub.

## sensors_modules
Este paquete contiene las librerías necesarias para leer correctamente los sensores en el publicador de py_pubsub. Se ha generado una dependencia de py_pubsub sobre este paquete y así se ha conseguido hacer la importación de las librerías sin tener que modificar a mano la carpeta install.
