#/usr/bin/python3
import RPi.GPIO as GPIO
import pigpio
import time
 
servo = 17
servo2 =18 
# more info at http://abyz.me.uk/rpi/pigpio/python.html#set_servo_pulsewidth

 
pwm = pigpio.pi() 
pwm.set_mode(servo, pigpio.OUTPUT)
pwm.set_PWM_frequency( servo, 50 )

pwm.set_mode(servo2, pigpio.OUTPUT) 
pwm.set_PWM_frequency( servo2, 50 )

while True:  
	#print( "0 deg" )
	
    #for x in reversed(range(900, 1900, 10)): 
    #    pwm.set_servo_pulsewidth( servo, x )
    #    time.sleep(0.1)
 
    pwm.set_servo_pulsewidth( servo2, 1500 )
    time.sleep(1)
    print("700") 
    #pwm.set_servo_pulsewidth( servo, 1900 )
    #time.sleep(1)

    pwm.set_servo_pulsewidth( servo2, 2500 ) 
    time.sleep(1)
    print("1900")

    pwm.set_servo_pulsewidth( servo2, 500 ) 
    time.sleep(1)
    print("0")
	#print( "180 deg" )
	#pwm.set_servo_pulsewidth( servo, 2500 ) ;
	#time.sleep( 3 )
 
# turning off servo
#pwm.set_PWM_dutycycle(servo, 0)
#pwm.set_PWM_frequency( servo, 0 )
