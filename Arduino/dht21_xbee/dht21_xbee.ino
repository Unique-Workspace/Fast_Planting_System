// 
//   FILE:  dht_test.pde
// PURPOSE: DHT library test sketch for Arduino
//

#include <dht.h>
#include <XBee.h>
#include <SoftwareSerial.h>
#include <stdlib.h> // for dtostrf()

dht DHT;

#define DHT11_PIN 2 //put the sensor in the digital pin 2
#define HUMI_CTRL_PIN 3  
#define TIME_DELAY  30
#define LENGTH 20

// create the XBee object
XBee xbee = XBee();

// MAX data payload: 32*7 + 19 = 243  bytes
uint8_t payload[LENGTH];
uint8_t str_temperature[7];
uint8_t str_humidity[7];

uint8_t humi_delay = 0;

// SH + SL Address of receiving XBee
XBeeAddress64 addr64 = XBeeAddress64(0x0013a200, 0x40b41039);
ZBTxRequest zbTx = ZBTxRequest(addr64, payload, sizeof(payload));
ZBTxStatusResponse txStatus = ZBTxStatusResponse();

// create reusable response objects for responses we expect to handle 
ZBRxResponse rx = ZBRxResponse();

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
  if(humidity > 0 && humidity < 99)
  {
    // increase
    mySerial.println("\t need to increase humidity");
    digitalWrite(HUMI_CTRL_PIN, HIGH);    // trun on humidity relay control
    humi_delay = 0;
  }
  else if(humidity >= 99)
  {
    // ok
    mySerial.println("\t humidity >=99");
    if(humi_delay > TIME_DELAY)
    {
      mySerial.println("\t TURN OFF humidity.");
      digitalWrite(HUMI_CTRL_PIN, LOW); 
      humi_delay = 0;
    }
    else
    {
      humi_delay++;
    }
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
  
  pinMode(HUMI_CTRL_PIN, OUTPUT);
}

void loop()
{
  int i, j;
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
  
  dtostrf(DHT.humidity, 3, 2, (char *)str_humidity);
  dtostrf(DHT.temperature, 3, 2, (char *)str_temperature);
  //mySerial.println(String((char *)str_humidity) + String((char *)str_temperature));
  i=0;
  payload[i++] = 'H';
  payload[i++] = ':';
  for(j=0; i<7 && str_humidity[j]!=0; i++, j++)
  {
    payload[i]=str_humidity[j];
  }
  payload[i++] = 'T';
  payload[i++] = ':';
  for(j=0; j<7 && str_temperature[j]!=0; i++,j++)
  {
    payload[i] = str_temperature[j];
  }
  //mySerial.print((char *)payload);
  xbee.send(zbTx);

  delay(200);
  // after sending a tx request, we expect a status response
  // wait up to half second for the status response
  if (xbee.readPacket(500)) {
    // got a response!
    mySerial.print("got a response!\n");
    // should be a znet tx status            	
    if (xbee.getResponse().getApiId() == ZB_TX_STATUS_RESPONSE) {
      xbee.getResponse().getZBTxStatusResponse(txStatus);

      // get the delivery status, the fifth byte
      if (txStatus.getDeliveryStatus() == SUCCESS) {
        // success.  time to celebrate
        mySerial.print("success.\n");
      } else {
        // the remote XBee did not receive our packet. is it powered on?
        mySerial.print("the remote XBee did not receive our packet\n");
      }
    }
    else if(xbee.getResponse().getApiId() == ZB_RX_RESPONSE) {
        // got a zb rx packet
        // now fill our zb rx class
        xbee.getResponse().getZBRxResponse(rx);
      
        mySerial.println("Got an rx packet!");
        if (rx.getOption() == ZB_PACKET_ACKNOWLEDGED) {
            // the sender got an ACK
            mySerial.println("packet acknowledged");
        } else {
          mySerial.println("packet not acknowledged");
        }
        
        mySerial.print("checksum is ");
        mySerial.println(rx.getChecksum(), HEX);

        mySerial.print("packet length is ");
        mySerial.println(rx.getPacketLength(), DEC);
        
         for (int i = 0; i < rx.getDataLength(); i++) {
          mySerial.print("payload [");
          mySerial.print(i, DEC);
          mySerial.print("] is ");
          mySerial.println(rx.getData()[i], HEX);
        }
        
       for (int i = 0; i < xbee.getResponse().getFrameDataLength(); i++) {
        mySerial.print("frame data [");
        mySerial.print(i, DEC);
        mySerial.print("] is ");
        mySerial.println(xbee.getResponse().getFrameData()[i], HEX);
      }
    }
  } else if (xbee.getResponse().isError()) {
    mySerial.print("Error reading packet.  Error code: ");  
    mySerial.println(xbee.getResponse().getErrorCode());
  } else {
    // local XBee did not provide a timely TX Status Response -- should not happen
    mySerial.print("local XBee did not provide a timely TX Status Response\n");
  
  }

  humidity_func(DHT.humidity);
  temperature_func(DHT.temperature);

  delay(1000);
}
//
// END OF FILE
//

