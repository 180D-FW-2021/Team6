# https://pypi.org/project/pygatt/

import pygatt
from binascii import hexlify

import time 
import RPi.GPIO as GPIO
import pigpio

adapter = pygatt.GATTToolBackend()

servo = 17 

pwm = pigpio.pi()
pwm.set_mode(servo, pigpio.OUTPUT)

def toggle_action(data):

    if(data != 0x00):
        pwm.set_PWM_frequency( servo, 50 )
        print( "0 deg" )

        pwm.set_servo_pulsewidth( servo, 500 ) ;
        time.sleep( 3 )

        print( "90 deg" )
        pwm.set_servo_pulsewidth( servo, 1500 ) ;
        time.sleep( 3 )

        print( "180 deg" )
        pwm.set_servo_pulsewidth( servo, 2500 ) ;
        time.sleep( 3 )

        # turning off servo
        pwm.set_PWM_dutycycle(servo, 0)
        pwm.set_PWM_frequency( servo, 1 )


def handle_data(handle, value):
    """
        handle -- integer, characteristic read handle the data was received on
        value -- bytearray, the data returned in the notification
        """
        print("Received data: %s" % hexlify(value))
        end = hexlify(value)
        toggle_action(send)


def main(): 
    adapter.start()
    while(1):
        try:
            device = adapter.connect('91:2a:70:0e:41:e3')
                device.subscribe("84dfdb6a-8a51-8afd-5425-17c7f94d8199",callback=handle_data)
        except:
            print("Cannnot subscribe")

    time.sleep(1)

if __name__=="__main__":
    main()
