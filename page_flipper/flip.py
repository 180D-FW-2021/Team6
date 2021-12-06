from gpiozero import Motor, AngularServo, LED
from time import sleep

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
    sleep(0.6)
    motorF.stop()
    servo.angle = 180
    sleep(1)
    servo.angle = 0
    sleep(1)
    servo.max()
    print('turning page forward')

def init():
    global servo, motorF, led
    #servo = HardwarePWM(0, hz=60)
    #servo.start(0)
    servo = AngularServo(18, min_angle=0, max_angle=180, min_pulse_width=0.0006, max_pulse_width=0.0024)
    servo.angle = 180
    sleep(1)
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
