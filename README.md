
# TCS230 based Bluetooth color picker

This is [TCS230](https://ams.com/documents/20143/36005/ColorSensors_AN000518_1-00.pdf) based Bluetooth color picker prototype which we build to test the concept. In here the idea is to extract color from any physical object and transfer it to PC / mobile. To test this concept, we use low cost TCS230 color sensor. 

TCS230 is programmable color light-to-frequency convert IC. This chip produces square wave output with frequency directly proportional to the light intensity. To drive this sensor and capture its output we used PIC16F628A microcontroller. The processed output is then transfer to the host using HC-05 Bluetooth SPP (*Serial Port Protocol*) module.
![Schematic of TCS230 based color picker](https://github.com/dilshan/tcs230-color-picker/raw/master/schematic/color-picker.png)
In PC we wrote small Python script to display captured value and color in a Window. 

In this design we drive TCS230 sensor with 20% frequency scaling. The entire circuit is build using commonly available modules and components. For color sensor we use 8-pin TCS230 sensor module which is commonly found in *eBay* and other online electronic component stores. This module comes with 4 white LEDs and because of that we don’t need separate circuit for LEDs. 

Due to small number of components this circuit is quite easy to assemble. To build our prototype we used 46mm × 36mm breadboard. Connections to the TCS230 sensor module is made using couple of jumper wires. 

Before connecting this circuit with PC or host device make sure to configure HC-05 Bluetooth module with proper name and with baud rate of 9600. To configure this module, we used [HC-06 configuration utility](https://github.com/dilshan/hc6-config) which we developed couple of months back. Also make sure to configure "*config.py*" file with correct COM port name. 

