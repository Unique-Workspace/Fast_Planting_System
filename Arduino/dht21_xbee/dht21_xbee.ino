// 
//   FILE:  dht_test.pde
// PURPOSE: DHT library test sketch for Arduino
//

#include <dht.h>
#include <XBee.h>
#include <SoftwareSerial.h>
#include <stdlib.h> // for dtostrf()

#include <OneWire.h>
#include <DallasTemperature.h>


/* PIN DEFINE BEGIN */
#define DHT11_PIN 2  //put the sensor in the digital pin 2
#define HUMI_CTRL_PIN 3  // for humidifier on/off control
#define ONE_WIRE_BUS 4  // for 18b20 water temprature 
#define WATER_CTRL_PIN 5 // for 18b20 water ctrl.
/* PIN DEFINE END */

/* DATA AREA BEGIN */
#define TIME_DELAY  300
#define LENGTH 20
// MAX data payload: 32*7 + 19 = 243  bytes
uint8_t payload[LENGTH];
uint8_t str_temperature[7];
uint8_t str_humidity[7];
uint8_t str_water_tempe[7];
uint8_t humi_delay = 0;
double temp_room_min = 10;
double temp_room_max = 30;
double temp_water_min = 20;
double temp_water_max = 30;
double humi_min = 95;
double humi_max = 99;

String humi_min_key = "Hmin:";
String humi_max_key = "Hmax:";
String temp_room_min_key = "TRmin:";
String temp_room_max_key = "TRmax:";
String temp_water_min_key = "TWmin:";
String temp_water_max_key = "TWmax:";

bool tx_send_flag = true;
int tx_send_flag_count = 0;
  
dht DHT;
/* DATA AREA END */

/* XBEE STRUCTURE BEGIN */
// create the XBee object
XBee xbee = XBee();

// SH + SL Address of receiving XBee
XBeeAddress64 addr64 = XBeeAddress64(0x0013a200, 0x40b41060); //39
ZBTxRequest zbTx = ZBTxRequest(addr64, payload, sizeof(payload));
ZBTxStatusResponse txStatus = ZBTxStatusResponse();

// create reusable response objects for responses we expect to handle 
ZBRxResponse rx = ZBRxResponse();

/* XBEE STRUCTURE END */

/* SERIAL PORT BEGIN */
// Define NewSoftSerial TX/RX pins
// Connect Arduino pin 9 to TX of usb-serial device
uint8_t ssRX = 10;
// Connect Arduino pin 10 to RX of usb-serial device
uint8_t ssTX = 11;
// Remember to connect all devices to a common Ground: XBee, Arduino and USB-Serial device
SoftwareSerial mySerial(ssRX, ssTX);
/* SERIAL PORT END */


/* 18b20 water sensor begin */
// Setup a oneWire instance to communicate with any OneWire devices (not just Maxim/Dallas temperature ICs)
OneWire oneWire(ONE_WIRE_BUS);

// Pass our oneWire reference to Dallas Temperature. 
DallasTemperature water_sensor(&oneWire);
/* 18b20 water sensor end */

void humidity_func(double humidity)
{
  //humidity conditions
  if(humidity <= humi_min)
  {
    mySerial.println("\t humidity increase");
    digitalWrite(HUMI_CTRL_PIN, HIGH);    // trun on humidifier
    humi_delay = 0;
  }
  else if(humidity > humi_min && humidity < humi_max)
  {
    // increase
    mySerial.println("\t humidity increase");
    digitalWrite(HUMI_CTRL_PIN, HIGH);    // trun on humidifier
    humi_delay = 0;
  }
  else if(humidity >= humi_max)
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
  if(temperature < temp_room_min)
  {
    // increase
    mySerial.println("\t temperature increase");
  }
  else if(temperature >= temp_room_min && temperature < temp_room_max)
  {
    // ok
    mySerial.println("\t temperature ok");
  }
  else if(temperature >= temp_room_max)
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

void water_func(double water_temperature)
{
  //temperature conditions
  if(water_temperature < temp_water_min)
  {
    // increase
    digitalWrite(WATER_CTRL_PIN, HIGH); 
    mySerial.println("\t water_temperature increase");
  }
  else if(water_temperature >= temp_water_min && water_temperature < temp_water_max)
  {
    // ok
    mySerial.println("\t water_temperature ok");
  }
  else if(water_temperature >= temp_water_max)
  {
    //decrease
    digitalWrite(WATER_CTRL_PIN, LOW); 
    mySerial.println("\t water_temperature decrease");
  }
  else
  {
    // error
    mySerial.println("\t water_temperature error");
  }
}

// parse the Rx payload data. get the temperature and humidity value from the packets.
void parse_rxdata(char rx_data[])
{
  int i, j;
  char strKey[8];
  char strNum[8];
  
  mySerial.println(rx_data);
  for(i = 0, j = 0; rx_data[i] != ':'; i++, j++)
  {
    strKey[j] = rx_data[i];
  }
  strKey[j++] = ':';
  strKey[j++] = '\0';
  String stringKey = strKey;
  mySerial.println(stringKey);
  
  // j<6 cut off extral chars.it will cause arduino reset.
  for(i++, j = 0; rx_data[i] != '\0' && j<6; i++, j++)
  {
    strNum[j] = rx_data[i];
  }
  strNum[j++] = '\0';
  
  if(stringKey.compareTo(humi_min_key))
  {
    humi_min = strtod((const char *)strNum, NULL);
    mySerial.println(humi_min);
    tx_send_flag = false;
    tx_send_flag_count = 0;
  }
  else if(stringKey.compareTo(humi_max_key))
  {
    humi_max = strtod((const char *)strNum, NULL);
    mySerial.println(humi_max);
    tx_send_flag = false;
    tx_send_flag_count = 0;
  }
  else if(stringKey.compareTo(temp_room_min_key))
  {
    temp_room_min = strtod((const char *)strNum, NULL);
    mySerial.println(temp_room_min);
    tx_send_flag = false;
    tx_send_flag_count = 0;
  }
  else if(stringKey.compareTo(temp_room_max_key))
  {
    temp_room_max = strtod((const char *)strNum, NULL);
    mySerial.println(temp_room_max);
    tx_send_flag = false;
    tx_send_flag_count = 0;
  }
  else if(stringKey.compareTo(temp_water_min_key))
  {
    temp_water_min = strtod((const char *)strNum, NULL);
    mySerial.println(temp_water_min);
    tx_send_flag = false;
    tx_send_flag_count = 0;
  }
  else if(stringKey.compareTo(temp_water_max_key))
  {
    temp_water_max = strtod((const char *)strNum, NULL);
    mySerial.println(temp_water_max);
    tx_send_flag = false;
    tx_send_flag_count = 0;
  }
  else
  {
    mySerial.println("[ERROR] parse_rxdata() not found: " + stringKey);
  }
  
}

void setup()
{
  Serial.begin(115200);
  xbee.setSerial(Serial);
  
  while (!Serial) {
    ; // wait for serial port to connect. Needed for Leonardo only
  }
  // set the data rate for the SoftwareSerial port
  mySerial.begin(115200);
  mySerial.println("DHT TEST PROGRAM for Fast Planting System");
  mySerial.print("LIBRARY VERSION: ");
  mySerial.println(DHT_LIB_VERSION);
  mySerial.println();
  mySerial.println("Type,\tstatus,\tHumidity (%),\tTemperature (C)");
  mySerial.println("SW serial debug.");
  
  pinMode(HUMI_CTRL_PIN, OUTPUT);
  pinMode(WATER_CTRL_PIN, OUTPUT);

  // Start up the 18b20 water sensor library
  water_sensor.begin();
}

void loop()
{
  int i, j;
  double water_tempe;
  char rx_data[64];
  
  // READ DATA
  //mySerial.print("DHT21, \t");
  int chk = DHT.read22(DHT11_PIN);
  switch (chk)
  {
    case 0:  mySerial.print("OK,\t"); break;
    case -1: mySerial.print("Checksum error,\t"); break;
    case -2: mySerial.print("Time out error,\t"); break;
    default: mySerial.print("Unknown error,\t"); break;
  }
  // DISPLAT DATA
  //mySerial.print(DHT.humidity,1);
  //mySerial.print(",\t");
  //mySerial.println(DHT.temperature,1);
  
  dtostrf(DHT.humidity, 3, 2, (char *)str_humidity);
  dtostrf(DHT.temperature, 3, 2, (char *)str_temperature);
  //mySerial.println(String((char *)str_humidity) + String((char *)str_temperature));
  
  water_sensor.requestTemperatures(); // Send the command to get temperatures
  water_tempe = water_sensor.getTempCByIndex(0);
  dtostrf(water_tempe, 3, 2, (char *)str_water_tempe);
  //mySerial.print("Water temperature is: ");
  //mySerial.println(water_tempe);
  
  // SEND DATA
  i=0;
  for(j=0; i<7 && str_humidity[j]!=0; i++, j++)
  {
    payload[i]=str_humidity[j];
  }
  payload[i++] = ',';
  for(j=0; j<7 && str_temperature[j]!=0; i++,j++)
  {
    payload[i] = str_temperature[j];
  }
  payload[i++] = ',';
  for(j=0; j<7 && str_water_tempe[j]!=0; i++,j++)
  {
    payload[i] = str_water_tempe[j];
  }
  payload[i++] = ',';
  //mySerial.print((char *)payload);
  if(tx_send_flag)
  {
    xbee.send(zbTx);
  }
  else
  {
    tx_send_flag_count++;
    if(tx_send_flag_count>2)
    {
      tx_send_flag = true;
    }
  }
  
  // RECEIVE DATA
  //delay(200);
  // after sending a tx request, we expect a status response
  // wait up to half second for the status response
  if (xbee.readPacket(200)) {
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
        /***
        mySerial.print("checksum is ");
        mySerial.println(rx.getChecksum(), HEX);

        mySerial.print("packet length is ");
        mySerial.println(rx.getPacketLength(), DEC);
        
        mySerial.print("data length is ");
        mySerial.println(rx.getDataLength(), DEC);
        ***/
         for (i = 0; i < rx.getDataLength(); i++) {
           /***
          mySerial.print("payload [");
          mySerial.print(i, DEC);
          mySerial.print("] is ");
          mySerial.println(rx.getData()[i], HEX);
          ***/
          rx_data[i] = rx.getData()[i];
        }
        rx_data[i++] = '\0';
        parse_rxdata(rx_data);
        
        /***
       for (i = 0; i < xbee.getResponse().getFrameDataLength(); i++) {
        mySerial.print("frame data [");
        mySerial.print(i, DEC);
        mySerial.print("] is ");
        mySerial.println(xbee.getResponse().getFrameData()[i], HEX);
      }
      ***/
    }
  } else if (xbee.getResponse().isError()) {
    mySerial.print("Error reading packet.  Error code: ");  
    mySerial.println(xbee.getResponse().getErrorCode());
  } else {
    // local XBee did not provide a timely TX Status Response -- should not happen
    mySerial.print("No TX Status Response\n");
  
  }

  // HANDLE DATA
  humidity_func(DHT.humidity);
  temperature_func(DHT.temperature);
  water_func(water_tempe);

  //delay(1000);
}
//
// END OF FILE
//

