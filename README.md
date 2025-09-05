# Paletizado-Estropajos
Proyecto creado para la asignatura Proyectos de Sistemas Robóticos donde se ha prototipado un sistema de clasificación y paletizado de estropajos. Realizado en conjunto con Alejandro Gea, Adrián Gea, Daniel Burgos y Martín Cámara.

## Funcionamiento del Proyecto
### Módulo 1
En este primer módulo una cinta principal lleva los estropajos de un color aleatorio hasta el final de la misma, donde un robot mediante una cámara RGB detecta el color del estropajo para clasificarlo y ponerlo en la cinta del color correspondiente. La detección de color para esta simulación se ha hecho mediante un código de python que diferencia los colores de los diferentes estropajos y le comunica al robot mediante sockets el color actual del estropajo en la cinta.
### Módulo 2
En este segundo módulo los estropajos son traídos por las distintas cintas de colores y, una vez haya uno de cada color, estos son transportados al final de la cinta para que el robot los apile y los almacene. 
En esta primera parte, el robot va apilando los estropajos uno por uno en una estación donde se envolverá el paquete, para que después el robot coja todos los estropajos envueltos y los deposite en la caja para su posterior almacenamiento. 

## Instrucciones de Funcionamiento
Se ha creado un entorno de miniconda. Para ello hay que instalar el programa desde la página oficial de [Anaconda](https://www.anaconda.com/docs/getting-started/miniconda/install)
Para configurar el entorno se va utilizar los comandos:
`conda env create -f entorno.yml`
`conda activate proyectos_env`

Una vez instalado el entorno, deberemos abrir los dos Pack&Go en RobotStudio, que contienen las células del robot 1 y el robot 2. Ahora lanzamos la simulación del robot 1 en RobotStudio y, seguidamente, ejecutamos el script de detección de color `detect&sendColor.py` en el entorno de Miniconda. Con esto hecho, nos pedirá que seleccionemos una zona de la pantalla para detectar el color, seleccionamos la zona de la cinta a donde llegan los estropajos y le damos a intro. Con esto, ya se estaría ejecutando la parte 1 de nuestro prototipo, faltaría lanzar la simulación de la célula del robot 2 (Módulo 2) que puede funcionar de manera independiente a la del robot 1 y observar también su funcionamiento.

## Ejemplo de Funcionamiento
### Módulo 1
<video src="https://github.com/user-attachments/assets/961ef0cb-05eb-4429-8b69-a26997508e22" controls width="600"></video>

### Módulo 2
<video src="https://github.com/user-attachments/assets/9ad6f57e-9aa9-4b03-8734-181f6db1b8e9" controls width="600"></video>
