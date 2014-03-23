// 
//   FILE:  dht_test.pde
// PURPOSE: DHT library test sketch for Arduino
//

#include <dht.h>
#include <XBee.h>
#include <SoftwareSerial.h>

dht DHT;

#define DHT11_PIN 2//put the sensor in the digital pin 2
#define LENGTH 8

// create the XBee object
XBee xbee = XBee();

// MAX data payload: 32*7 + 19 = 243  bytes
uint8_t payload[LENGTH];

// SH + SL Address of receiving XBee
XBeeAddress64 addr64 = XBeeAddress64(0x0013a200, 0x40b41039);
ZBTxRequest zbTx = ZBTxRequest(addr64, payload, sizeof(payload));
ZBTxStatusResponse txStatus = ZBTxStatusResponse();

// Define NewSoftSerial TX/RX pins
// Connect Arduino pin 9 to TX of usb-serial device
uint8_t ssRX = 10;
// Connect Arduino pin 10 to RX of usb-serial device
uint8_t ssTX = 11;
// Remember to connect all devices to a common Ground: XBee, Arduino and USB-Serial device
SoftwareSerial mySerial(ssRX, ssTX);

void humidity_func(double humidity)
{
  //humidity conditions
  if(humidity > 0 && humidity < 40)
  {
    // increase
    mySerial.println("\t humidity increase");
  }
  else if(humidity >= 40 && humidity < 80)
  {
    // ok
    mySerial.println("\t humidity ok");
  }
  else if(humidity >= 80 && humidity < 100)
  {
    //decrease
    mySerial.println("\t humidity decrease");
  }
  else
  {
    // error
    mySerial.println("\t humidity error");
  }
}

void temperature_func(double temperature)
{
  //temperature conditions
  if(temperature < 10)
  {
    // increase
    mySerial.println("\t temperature increase");
  }
  else if(temperature >= 10 && temperature < 30)
  {
    // ok
    mySerial.println("\t temperature ok");
  }
  else if(temperature >= 30)
  {
    //decrease
    mySerial.println("\t temperature decrease");
  }
  else
  {
    // error
    mySerial.println("\t temperature error");
  }
}

void setup()
{
    Serial.begin(9600);
  xbee.setSerial(Serial);
  
  while (!Serial) {
    ; // wait for serial port to connect. Needed for Leonardo only
  }
  // set the data rate for the SoftwareSerial port
  mySerial.begin(9600);
  mySerial.println("DHT TEST PROGRAM for Fast Planting System");
  mySerial.print("LIBRARY VERSION: ");
  mySerial.println(DHT_LIB_VERSION);
  mySerial.println();
  mySerial.println("Type,\tstatus,\tHumidity (%),\tTemperature (C)");
   mySerial.println("SW serial debug.");
  
}

void loop()
{

  // READ DATA
  mySerial.print("DHT21, \t");
 int chk = DHT.read22(DHT11_PIN);
  switch (chk)
  {
    case 0:  mySerial.print("OK,\t"); break;
    case -1: mySerial.print("Checksum error,\t"); break;
    case -2: mySerial.print("Time out error,\t"); break;
    default: mySerial.print("Unknown error,\t"); break;
  }
 // DISPLAT DATA
  mySerial.print(DHT.humidity,1);
  mySerial.print(",\t");
  mySerial.println(DHT.temperature,1);
  
  payload[0]=DHT.humidity;
  payload[1]='1';
  payload[2]=DHT.temperature;
  payload[3]='\n';
  xbee.send(zbTx);
  
  humidity_func(DHT.humidity);
  temperature_func(DHT.temperature);

  delay(2000);
}
//
// END OF FILE
//

