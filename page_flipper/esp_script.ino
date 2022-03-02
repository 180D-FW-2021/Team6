#include <ESP32Servo.h>
#include "BLEDevice.h"
#include "BLEScan.h"

uint8_t gesture = -1;

/*** START BLE ***/
static BLEUUID serviceUUID("180f");
static BLEUUID charUUID("2a19");

static boolean doConnect = false;
static boolean connected = false;
static boolean doScan = false;
static BLERemoteCharacteristic* pRemoteCharacteristic;
static BLEAdvertisedDevice* myDevice;
  static void notifyCallback(
  BLERemoteCharacteristic* pBLERemoteCharacteristic,
  uint8_t* pData,
  size_t length,
  bool isNotify) {
    Serial.print("Notify callback for gesture characteristic ");
    Serial.print(pBLERemoteCharacteristic->getUUID().toString().c_str());
    Serial.print(" of data length ");
    Serial.println(length);
    Serial.print("; data: ");
    Serial.println(*pData);
    gesture = *pData;
  }

class MyClientCallback : public BLEClientCallbacks {
    void onConnect(BLEClient* pclient) {
    }

    void onDisconnect(BLEClient* pclient) {
      connected = false;
      Serial.println("onDisconnect");
    }
};

bool connectToServer() {
  Serial.print("Forming a connection to ");
  // Serial.println(myDevice->getAddress().toString().c_str());

  BLEClient* pClient  = BLEDevice::createClient();
  Serial.println(" - Created client");

  pClient->setClientCallbacks(new MyClientCallback());

  // Connect to the remove BLE Server.
  pClient->connect(myDevice);  // if you pass BLEAdvertisedDevice instead of address, it will be recognized type of peer device address (public or private)
  Serial.println(" - Connected to server");

  // Obtain a reference to the service we are after in the remote BLE server.
  BLERemoteService* pRemoteService = pClient->getService(serviceUUID);
  if (pRemoteService == nullptr) {
    Serial.print("Failed to find our service UUID: ");
    Serial.println(serviceUUID.toString().c_str());
    pClient->disconnect();
    return false;
  }
  Serial.println(" - Found our service");

  pRemoteCharacteristic = pRemoteService->getCharacteristic(charUUID);
  
  if (pRemoteCharacteristic == nullptr) {
    Serial.print("Failed to find our gesture UUID: ");
    Serial.println(charUUID.toString().c_str());
    pClient->disconnect();
  }

  Serial.println(" - Found our characteristic");

  // Read the value of the characteristic.
  if (pRemoteCharacteristic->canRead()) {
    std::string val2 = (pRemoteCharacteristic->readValue());
    Serial.print("The characteristic value was: ");
    Serial.println( val2.c_str() );
  }

  if (pRemoteCharacteristic->canNotify())
    pRemoteCharacteristic->registerForNotify(notifyCallback);
    
  connected = true;
}

class MyAdvertisedDeviceCallbacks: public BLEAdvertisedDeviceCallbacks {
    /**
        Called for each advertising BLE server.
    */
    void onResult(BLEAdvertisedDevice advertisedDevice) {
      Serial.print("BLE Advertised Device found: ");
      Serial.print(advertisedDevice.haveServiceUUID());
      Serial.print(advertisedDevice.isAdvertisingService(serviceUUID));
      Serial.println(advertisedDevice.toString().c_str());

      // We have found a device, let us now see if it contains the service we are looking for.
      if (advertisedDevice.haveServiceUUID() && advertisedDevice.isAdvertisingService(serviceUUID)) {

        BLEDevice::getScan()->stop();
        myDevice = new BLEAdvertisedDevice(advertisedDevice);
        doConnect = true;
        doScan = true;

      } // Found our server
    } // onResult
}; // MyAdvertisedDeviceCallbacks


/*** END BLE ***/

/*** START MOTORS ***/
Servo servo1;
Servo servo2;

/*** END MOTORS ***/

bool turn = false;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

  Serial.println("Starting Arduino BLE Client application...");
  BLEDevice::init("");
  
  BLEScan* pBLEScan = BLEDevice::getScan();
  pBLEScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks());
  pBLEScan->setInterval(1349);
  pBLEScan->setWindow(449);
  pBLEScan->setActiveScan(true);
  pBLEScan->start(5, false);


  servo1.setPeriodHertz(50);
  servo1.attach(12, 500, 2400);
  servo1.write(0);

  servo2.setPeriodHertz(50);
  servo2.attach(13, 500, 2400);
  servo2.write(0);
  
  
  
}

void loop() {
  // put your main code here, to run repeatedly:

  if (doConnect == true) {
    if (connectToServer()) {
      Serial.println("We are now connected to the BLE Server.");
    } else {
      Serial.println("We have failed to connect to the server; there is nothin more we will do.");
    }
    doConnect = false;
  }

  // If we are connected to a peer BLE Server, update the characteristic each time we are reached
  // with the current time since boot.
  if (connected) {
    String newValue = "Time since boot: " + String(millis() / 1000);

     gesture = pRemoteCharacteristic->readUInt8();
     Serial.println(gesture);
 
  } else if (doScan) {
    BLEDevice::getScan()->start(0);  // this is just eample to start scan after disconnect, most likely there is better way to do it in arduino
  }
  
  switch (gesture) {
    case 1:
      Serial.println("forward");
      gesture = -1;
      //break;
    case 16: 
      Serial.println("upwards");
      gesture = -1;
      //break;
    case 17:
      Serial.println("flip page forward");

      for (int pos = 180; pos >= 80; pos -= 1) { // goes from 0 degrees to 180 degrees
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
      
      gesture = -1;
      break;
    default:
      delay(1000);
      break;      
  }
}
