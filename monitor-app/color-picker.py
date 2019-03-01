# ------------------------------------------------------------------------------
# TCS230 based Bluetooth color picker - monitoring console.
# 
# Copyright © 2019 Dilshan R Jayakody. [jayakody2000lk@gmail.com]
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ------------------------------------------------------------------------------

from graphics import *;
import serial;
import time;
import config;

# Function to convert TCS230 color value to standard 0x00..0xFF color range.
def convertToColor(sensorVal):
	colorVal = int((sensorVal - config.SENSORMIN) * (0 - 255) / (config.SENSORMAX - config.SENSORMIN) + 255);
	
	# clamp values between the valid range.
	if colorVal > 255:
		colorVal = 255;
		
	if colorVal < 0:
		colorVal = 0;
		
	return colorVal;

# Open Bluetooth serial connection with specified parameters.
bluetoothCon = serial.Serial();
bluetoothCon.baudrate = config.BAUD;
bluetoothCon.port = config.PORT;

try:
	bluetoothCon.open();
except:
	print("Unable to establish connection with Bluetooth color picker.");
	print("Make sure that device is power on and all configuration parameters are correct.");
	exit();

# Create graphic view to display captured color.
outputView = GraphWin('Sensor Preview', 400, 400);
outputView.setBackground('black');

# Create text to display current color value.
textPosition = Point(100, 50);
colorValue = Text(textPosition, "#00000");
colorValue.draw(outputView);
colorValue.setSize(14);
colorValue.setStyle("bold");

while(1):
	try:
		# Read serial data stream and try to identify header byte.
		headerData = bluetoothCon.read();
		if(headerData[0] == 0xD0):
			# Read red, green and blue values captured from TCS230 sensor.
			sensorRed = bluetoothCon.read();
			sensorGreen = bluetoothCon.read();
			sensorBlue = bluetoothCon.read();
			
			# Convert captured values to standard 0x00..0xFF range.
			trueRed = convertToColor(sensorRed[0]);
			trueGreen = convertToColor(sensorGreen[0]);
			trueBlue = convertToColor(sensorBlue[0]);
			
			# Update background color of preview window with decoded color.
			outputView.setBackground(color_rgb(trueRed, trueGreen, trueBlue));
			
			# Calculate color for fonts.
			fontRed = 255 - trueRed;
			fontGreen = 255 - trueGreen;
			fontBlue = 255 - trueBlue;
			
			# Update color value and text color with calculated values.
			colorStr = "#%0.2X%0.2X%0.2X" % (trueRed, trueGreen, trueBlue);
			colorValue.setText(colorStr);
			colorValue.setTextColor(color_rgb(fontRed, fontGreen, fontBlue));
			
			# Ignore CLEAR value and trail signature byte.
			bluetoothCon.read(2);
			
	except GraphicsError:
		bluetoothCon.close();
		exit();
