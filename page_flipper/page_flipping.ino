#include <Servo.h>

Servo servo1; 
Servo servo2; 
int pos = 180;
void setup() {
  // put your setup code here, to run once:
  servo1.attach(2); 
  servo2.attach(3); 
}

void loop() {
  // put your main code here, to run repeatedly:
  for (pos = 180; pos >= 80; pos -= 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    servo2.write(pos);              // tell servo to go to position in variable 'pos'
    delay(100);                       // waits 15ms for the servo to reach the position
  }
  servo1.write(70); 
  delay(1000); 

  servo2.write(180); 
  delay(1000); 
  
  servo1.write(180);
  delay(1000);

  servo1.write(0); 
  delay(1000);

}
