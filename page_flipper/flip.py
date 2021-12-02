from gpiozero import Motor, Servo
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
	global servo, motor
	servo = Servo(17)
	motorF = Motor(18, 27)
	# motorB = Motor(5, 6)

def main():
	if (left):
		pageturn_forward()
	
	if (right):
		pageturn_backwards()


if __name__=='__main__':
	main()

