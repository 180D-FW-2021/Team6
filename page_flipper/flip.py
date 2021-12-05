from gpiozero import Motor, Servo, LED
from time import sleep
from rpi_hardware_pwm import HardwarePWM

servo=None
motorF=None
led=None
left=True
right=False

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
    motorF.forward(0.5)
    sleep(0.3)
    motorF.stop()
    servo.change_duty_cycle(100)
    sleep(0.1)
    servo.change_duty_cycle(0)
    print('turning page forward')

def init():
    global servo, motorF, led
    servo = HardwarePWM(0, hz=60)
    servo.start(0)
    motorF = Motor(17, 27)
    led = LED(7)
    print( 'hardware initialized' )
    # motorB = Motor(5, 6)

def main():
    global servo, motorF, led, left, right
    init()
    led.on()
    if (left):
        pageturn_forward()


if __name__=='__main__':
        main()

