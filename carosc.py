#!/usr/bin/env python

from OSC import OSCServer,OSCClient, OSCMessage
import types
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.cleanup()

# SERVO PANEO
GPIO.setup(18, GPIO.OUT)
p = GPIO.PWM(18,100)
p.start(0)

# SERVO TILDEO
GPIO.setup(16, GPIO.OUT)
t = GPIO.PWM(16,100)
t.start(0)

# MOTORES
GPIO.setup(11, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)

server = OSCServer( ("192.168.10.1", 8000) )#Change it to your Raspberry Pi’s IP
client = OSCClient()

#Timeout indicates no signal is been received by TouchOSC
def handle_timeout(self):
	print "IDLE"  
server.handle_timeout = types.MethodType(handle_timeout, server)

# SERVOS CÁMARA
def pan(path, tags, args, source): 
    value=int(args[0]) #Gets pan servo value and changes it to pwm
    print "Pan Value:", value
    pan = float(value) / 10.0 + 2.5 
    p.ChangeDutyCycle(pan)

def tilt(path, tags, args, source):
    value=int(args[0]) #Gets tilt servo value and changes it to pwm
    print "Tilt Value:", value
    tilt = float(value) / 10.0 + 2.5
    t.ChangeDutyCycle(tilt)




# XY PAD
def xypad(path, tags, args, source):
    xx=int(args[0]) #Gets X value from XY pad
    yy=int(args[1]) #Gets Y value from XY pad

    if yy>130:
        GPIO.output(12, True)
        GPIO.output(13, True)
	print "Moving Forward", yy

    if yy<70:
	GPIO.output(11, True)
        GPIO.output(15, True)
	print "Moving Backwards", yy

    if xx<70:
	GPIO.output(11, True)
	GPIO.output(13, True)
	print "Turning Left", xx

    if xx>130:
	GPIO.output(12, True)
	GPIO.output(15, True)
	print "Turning Right", xx

    if xx<70 and yy<100:
        GPIO.output(12, True)
        GPIO.output(15, True)
        print "Reverse-Left", xx, ",", yy

    if xx>130 and yy<100:
        GPIO.output(11, True)
        GPIO.output(13, True)
        print "Reverse-Right", xx, ",", yy

    if yy>70 and yy<130:
      if xx>70 and xx<130:
        GPIO.output(11, False)
        GPIO.output(12, False)
        GPIO.output(15, False)
        GPIO.output(13, False)
        print "Stop", xx, ",", yy


server.addMsgHandler("/1/pan", pan)
server.addMsgHandler("/1/tilt", tilt)
server.addMsgHandler("/1/xyPad", xypad)
server.addMsgHandler("/1/xyPad/z", touch)


while True:
	server.handle_request()

server.close()
