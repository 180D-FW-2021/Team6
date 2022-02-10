#include <ArduinoBLE.h>

#include <Arduino_LSM9DS1.h>
 
#include <TensorFlowLite.h>
#include <tensorflow/lite/micro/all_ops_resolver.h>
#include <tensorflow/lite/micro/micro_error_reporter.h>
#include <tensorflow/lite/micro/micro_interpreter.h>
#include <tensorflow/lite/schema/schema_generated.h>
#include <tensorflow/lite/version.h>

#include "model.h" //tensorflow data

BLEByteCharacteristic* gestureCharacteristic = nullptr;
BLEService* bleService = nullptr;

long previousMillis = 0;

const float accelerationThreshold = 2.5; // threshold of significant in G's
const int numSamples = 119;

int samplesRead = numSamples;

// global variables used for TensorFlow Lite (Micro)
tflite::MicroErrorReporter tflErrorReporter;

// pull in all the TFLM ops, you can remove this line and
// only pull in the TFLM ops you need, if would like to reduce
// the compiled size of the sketch.
tflite::AllOpsResolver tflOpsResolver;

const tflite::Model* tflModel = nullptr;
tflite::MicroInterpreter* tflInterpreter = nullptr;
TfLiteTensor* tflInputTensor = nullptr;
TfLiteTensor* tflOutputTensor = nullptr;

// Create a static memory buffer for TFLM, the size may need to
// be adjusted based on the model you are using
constexpr int tensorArenaSize = 8 * 1024;
byte tensorArena[tensorArenaSize] __attribute__((aligned(16)));

// array to map gesture index to a name
const char* GESTURES[] = {
  "punch", 
  "flex", 
  "wave", };

#define NUM_GESTURES (sizeof(GESTURES) / sizeof(GESTURES[0]))

int a=0; // count

void setup() {

 bleService = new BLEService("180F");
 gestureCharacteristic = new BLEByteCharacteristic("2A19", BLERead | BLEWrite);

 Serial.begin(9600);
  if (!IMU.begin()) {
    Serial.println("LSM9DS1 failed!");
    while (1);
  }

  if (!BLE.begin()) {
    Serial.println("starting BLE failed!");
    while (1);
  }

  // set advertised local name and service UUID:
  BLE.setAdvertisedService(*bleService); // add the service UUID
  bleService->addCharacteristic(*gestureCharacteristic);
  BLE.addService(*bleService);
  // start advertising
  BLE.setLocalName("yschul");
  // set the initial value for the characeristic:
  gestureCharacteristic->writeValue(0);
  // start advertising
  BLE.advertise();
  Serial.println("BLE LED Peripheral");
 
  // print out the samples rates of the IMUs
  Serial.print("Accelerometer sample rate = ");
  Serial.print(IMU.accelerationSampleRate());
  Serial.println(" Hz");
  Serial.print("Gyroscope sample rate = ");
  Serial.print(IMU.gyroscopeSampleRate());
  Serial.println(" Hz");
  Serial.println();

  // get the TFL representation of the model byte array
  tflModel = tflite::GetModel(model);
  if (tflModel->version() != TFLITE_SCHEMA_VERSION) {
    Serial.println("Model schema mismatch!");
    while (1);
  }
  // Create an interpreter to run the model
  tflInterpreter = new tflite::MicroInterpreter(tflModel, tflOpsResolver, tensorArena, tensorArenaSize, &tflErrorReporter);
 
  // Allocate memory for the model's input and output tensors
  tflInterpreter->AllocateTensors();
 
  // Get pointers for the model's input and output tensors
  tflInputTensor = tflInterpreter->input(0);
  tflOutputTensor = tflInterpreter->output(0);
}

//String Level_String;
float aX, aY, aZ, gX, gY, gZ;

boolean active = false;

void loop() {

  // listen for BLE peripherals to connect:
  BLEDevice central = BLE.central();
  // if a central is connected to peripheral:
  if (central)
  {
    Serial.println("Bluetooth connected");
    while (central.connected())
    {
      // bluetooth device is connected
      
      // wait for significant motion
      if(active == false && samplesRead == numSamples) {
        if (IMU.accelerationAvailable()) {
          // read the acceleration data
          IMU.readAcceleration(aX, aY, aZ);
    
          // sum up the absolutes
          float aSum = fabs(aX) + fabs(aY) + fabs(aZ);
    
          // check if it's above the threshold
          if (aSum >= accelerationThreshold) {
            // reset the sample read count
            samplesRead = 0;
            active = true;
          }
        }

         if(central.connected()){
               // write to bluetooth
               gestureCharacteristic->writeValue((byte)0x00);
         }
         delay(10);
      }
      
      // check if the all the required samples have been read since
      // the last time the significant motion was detected
      if (active == true && samplesRead < numSamples) {
        // check if new acceleration AND gyroscope data is available
        if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable()) {
          // read the acceleration and gyroscope data
          IMU.readAcceleration(aX, aY, aZ);
          IMU.readGyroscope(gX, gY, gZ);
    
          // normalize the IMU data between 0 to 1 and store in the model's
          // input tensor
          tflInputTensor->data.f[samplesRead * 6 + 0] = (aX + 4.0) / 8.0;
          tflInputTensor->data.f[samplesRead * 6 + 1] = (aY + 4.0) / 8.0;
          tflInputTensor->data.f[samplesRead * 6 + 2] = (aZ + 4.0) / 8.0;
          tflInputTensor->data.f[samplesRead * 6 + 3] = (gX + 2000.0) / 4000.0;
          tflInputTensor->data.f[samplesRead * 6 + 4] = (gY + 2000.0) / 4000.0;
          tflInputTensor->data.f[samplesRead * 6 + 5] = (gZ + 2000.0) / 4000.0;
    
          samplesRead++;
    
          if (samplesRead == numSamples) {
            active = false;
            // Run inferencing
            TfLiteStatus invokeStatus = tflInterpreter->Invoke();
            if (invokeStatus != kTfLiteOk) {
              Serial.println("Invoke failed!");
              while (1);
              return;
            }

            // Counts if accuracy is 0.7 or higher
           if(tflOutputTensor->data.f[0] >= 0.7){
             // do something
             Serial.println("punch");
             if(central.connected()){
               // write to bluetooth
               gestureCharacteristic->writeValue((byte)0x01);
             }
           }
           else if(tflOutputTensor->data.f[1] >= 0.7){
             // do something
             Serial.println("flex");
             if(central.connected()){
               // write to bluetooth
               gestureCharacteristic->writeValue((byte)0x10);
             }
           }
           else if(tflOutputTensor->data.f[2] >= 0.7){
             // do something
             Serial.println("wave");
             if(central.connected()){
               // write to bluetooth
               gestureCharacteristic->writeValue((byte)0x11);
             }
           }
           else 
           {
               if(central.connected()){
               // write to bluetooth
               gestureCharacteristic->writeValue((byte)0x00);
             }
            
           }
            delay(1000); 
            // Loop through the output tensor values from the model
            Serial.print(GESTURES[1]); // GESTURES[0] = flex
            Serial.print(": ");
            Serial.println(tflOutputTensor->data.f[1], 6);       
            Serial.println();
          }
        }
      }     
    }
    Serial.println("Bluetooth disconnected");
  }
}
