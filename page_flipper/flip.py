from gpiozero import Motor, Servo, LED
from time import sleep

# pageturn_right / backwards hardware is not yet implemented
# TODO: replace sleep with polling or interrupts

def pageturn_backwards():
	print('turning backwards not yet implemented')
	return
	# motorB.forward()
	# sleep(300)
	# motorB.stop()
	# servo.min()
	# sleep(100)

def pageturn_forward():
	motorF.forward()
	sleep(300)
	motorF.stop()
	servo.max()
	sleep(100)
	servo.min()

def init():
	global servo, motor, led
	servo = Servo(17)
	motorF = Motor(18, 27)
	led = LED(7)
	# motorB = Motor(5, 6)

def main():
	led.on()
	while(1):
		if (left):
			pageturn_forward()
	
		if (right):
			pageturn_backwards()


if __name__=='__main__':
	main()

