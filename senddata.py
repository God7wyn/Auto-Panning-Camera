# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 19:09:11 2019

@author: Godwyn James William
"""

import serial

ser = serial.Serial("COM7", 9600, timeout=1)
x = input("Enter the degree: ")
y = bytes(x, 'UTF-8')
ser.write(y)
print(y)
ser.close()
print("COM7 Closed successfully")

