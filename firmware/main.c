/*------------------------------------------------------------------------------
TCS230 based Bluetooth color picker - firmware for PIC16F628A.

Copyright © 2019 Dilshan R Jayakody. [jayakody2000lk@gmail.com]

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
------------------------------------------------------------------------------*/

#include "main.h"

void main(void) 
{
    unsigned int redVal, greenVal, blueVal, clrVal;
    
    // Initialize system by disabling analog comparator module and enabling
    // UART module in MCU.
    initSystem();
    
    while(1)
    {
        // Read red, green, blue and clear values from TCS230 sensor.
        redVal = readColorValue(COLOR_RED_CHANNEL);
        __delay_us(50);
        blueVal = readColorValue(COLOR_BLUE_CHANNEL);
        __delay_us(50);
        greenVal = readColorValue(COLOR_GREEN_CHANNEL);
        __delay_us(50);
        clrVal = readColorValue(COLOR_CLEAR_CHANNEL);
        
        // Write captured values to UART to send to host over Bluetooth.
        // Due to 20% frequency scaling we don't need to send whole 16bit
        // integer to the host.
        sendByte(HEADER_SIGNATURE);
        sendByte(redVal);
        sendByte(greenVal);
        sendByte(blueVal);
        sendByte(clrVal);
        sendByte(TAIL_SIGNATURE);
        
        __delay_ms(10);
    }
}

void initSystem()
{
    CMCON = 0x07;
    TRISA = 0x04;
    PORTA = 0x00;
    
    initUART(9600);
}

void initUART(const long int baudRate)
{
    unsigned int baudRemainder = (_XTAL_FREQ - baudRate * 64)/(baudRate * 64);  
    if(baudRemainder > 255)
    {
        BRGH = 1;
        baudRemainder = (_XTAL_FREQ - baudRate*16)/(baudRate * 16);
    }
    
    if(baudRemainder < 256)
    {
        SPBRG = baudRemainder;
        SYNC = 0;
        SPEN = 1;
        TRISB1 = 1;
        TRISB2 = 1;
        CREN = 1;
        TXEN = 1;
    }
}

void sendByte(char data)
{
  while(!TRMT);
  TXREG = data;
}

unsigned int readColorValue(unsigned char colorComponent)
{
    unsigned int cycleCount = 0;
    
    // Update color channel.
    PORTA = (PORTA & 0xFC) | colorComponent;
    __delay_us(250);
    
    // Waiting to finish current pulse cycle.
    while((PORTA & 0x04) == 0x04);
    while((PORTA & 0x04) == 0x00);
    
    // Start capturing pulse width received from sensor.
    while((PORTA & 0x04) == 0x04)
    {
        cycleCount++;
    }
    
    return cycleCount;
}
