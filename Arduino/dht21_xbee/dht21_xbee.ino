// 
//   FILE:  dht_test.pde
// PURPOSE: DHT library test sketch for Arduino
//

#include <dht.h>
#include <XBee.h>
#include <SoftwareSerial.h>
#include <stdlib.h> // for dtostrf()
#include <string.h> // for strtok()
#include <pt.h>  // for protothread

#include <OneWire.h>
#include <DallasTemperature.h>


/* PIN DEFINE BEGIN */
#define DHT11_PIN 2  //put the sensor in the digital pin 2
#define HUMI_CTRL_PIN 3  // for humidifier on/off control
#define ONE_WIRE_BUS 4  // for 18b20 water temprature 
#define WATER_CTRL_PIN 5 // for 18b20 water ctrl.
/* PIN DEFINE END */

/* DATA AREA BEGIN */
#define HUMIDITY_TIME_DELAY  300
#define LENGTH 20
#define BUFLEN 80
#define SUB_BUFLEN 15
#define PARAMNUM 6
// MAX data payload: 32*7 + 19 = 243  bytes
static uint8_t payload[LENGTH];
static uint8_t str_temperature[7];
static uint8_t str_humidity[7];
static uint8_t str_water_tempe[7];
static uint8_t humi_delay = 0;

static float temp_room_min;
static float temp_room_max;
static float temp_water_min;
static float temp_water_max;
static float humi_min;
static float humi_max;
    
static const char *humi_min_key = "Hmin:";
static const char * humi_max_key = "Hmax:";
static const char * temp_room_min_key = "TRmin:";
static const char * temp_room_max_key = "TRmax:";
static const char * temp_water_min_key = "TWmin:";
static const char * temp_water_max_key = "TWmax:";
  
static dht DHT;
/* DATA AREA END */

/* XBEE STRUCTURE BEGIN */
// create the XBee object
static XBee xbee = XBee();

// SH + SL Address of receiving XBee
XBeeAddress64 addr64 = XBeeAddress64(0x0013a200, 0x40b41060); //39
ZBTxRequest zbTx = ZBTxRequest(addr64, payload, sizeof(payload));
ZBTxStatusResponse txStatus = ZBTxStatusResponse();

// create reusable response objects for responses we expect to handle 
static ZBRxResponse rx = ZBRxResponse();

/* XBEE STRUCTURE END */

/* SERIAL PORT BEGIN */
// Define NewSoftSerial TX/RX pins
// Connect Arduino pin 9 to TX of usb-serial device
static uint8_t ssRX = 10;
// Connect Arduino pin 10 to RX of usb-serial device
static uint8_t ssTX = 11;
// Remember to connect all devices to a common Ground: XBee, Arduino and USB-Serial device
SoftwareSerial mySerial(ssRX, ssTX);
/* SERIAL PORT END */


/* 18b20 water sensor begin */
// Setup a oneWire instance to communicate with any OneWire devices (not just Maxim/Dallas temperature ICs)
OneWire oneWire(ONE_WIRE_BUS);

// Pass our oneWire reference to Dallas Temperature. 
DallasTemperature water_sensor(&oneWire);
/* 18b20 water sensor end */

// for protothread.
static int counter_send,counter_receive; //counter为定时计数器
static struct pt pt_send, pt_receive; 

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
    if(humi_delay > HUMIDITY_TIME_DELAY)
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

static char strData[BUFLEN];
static char strSubData[PARAMNUM][SUB_BUFLEN];
// parse the Rx payload data. get the temperature and humidity value from the packets.
void parse_rxdata(char rx_data[])
{
    int i, j, k;
    char strKey[8];
    char strNum[8];
    
  //mySerial.println(rx_data);
  for(i=0; i<strlen(rx_data); i++)
  {
      strData[i] = rx_data[i];
  }
  strData[i] = '\0';
  mySerial.println(strData);
  
  // split the string "TRmin:20.0,TRmax:30.0,Hmin:90.0,Hmax:100.0,TWmin:20.0,TWmax:35.0"
  char *ptr = strtok(strData,",");
  for(j = 0; j<PARAMNUM && ptr != NULL; j++)
  {
     strcpy(strSubData[j], ptr);  // save the string to strSubData[][]
     ptr = strtok(NULL, ","); 
  }

  // extract the params from each string strSubData[][].
  for(k=0; k<PARAMNUM; k++)
  {
    for(i = 0, j = 0; strSubData[k][i] != ':'; i++, j++)
    {
      strKey[j] = strSubData[k][i];
    }
    strKey[j++] = ':';
    strKey[j++] = '\0';
    
    // j<6 cut off extral chars.it will cause arduino reset.
    for(i++, j = 0; strSubData[k][i] != '\0' && j<6; i++, j++)
    {
      strNum[j] = strSubData[k][i];
    }
    strNum[j++] = '\0';

    if(0 == strcmp(temp_room_min_key, strKey))
    {
      temp_room_min = atof((const char *)strNum);
      mySerial.println(temp_room_min);
    }
    else if(/*stringKey.compareTo(temp_room_max_key)*/0 == strcmp(temp_room_max_key, strKey))
    {
      temp_room_max = atof((const char *)strNum);
      mySerial.println(temp_room_max);
    }
    else if(0 == strcmp(humi_min_key, strKey))
    {
      humi_min = atof((const char *)strNum);
      mySerial.println(humi_min);
    }
    else if(0 == strcmp(humi_max_key, strKey))
    {
      humi_max = atof((const char *)strNum);
      mySerial.println(humi_max);
    }
    else if(0 == strcmp(temp_water_min_key, strKey))
    {
      temp_water_min = atof((const char *)strNum);
      mySerial.println(temp_water_min);
    }
    else if(0 == strcmp(temp_water_max_key, strKey))
    {
      temp_water_max = atof((const char *)strNum);
      mySerial.println(temp_water_max);
    }
    else
    {
       mySerial.println("[ERROR] parse_rxdata() not found: " );
    }
  }

      mySerial.println("+++++++++++++++++++++++++");
      mySerial.println(temp_room_min);
    mySerial.println(temp_room_max);
    mySerial.println(humi_min);
    mySerial.println(humi_max);
    
    mySerial.println(temp_water_min);
    mySerial.println(temp_water_max);
    mySerial.println("+++++++++++++++++++++++++");
}

void send_data()
{

    int i, j;
    double water_tempe;

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
  
    xbee.send(zbTx);

      // HANDLE DATA
    humidity_func(DHT.humidity);
    temperature_func(DHT.temperature);
    water_func(water_tempe);
}

/**
#define NO_ERROR 0
#define CHECKSUM_FAILURE 1
#define PACKET_EXCEEDS_BYTE_ARRAY_LENGTH 2
#define UNEXPECTED_START_BYTE 3
**/

void receive_data()
{
    int i;
    char rx_data[BUFLEN];

     // RECEIVE DATA
    // after sending a tx request, we expect a status response
    // wait up to half second for the status response
    if (xbee.readPacket(200)) 
    {
        // got a response!
        mySerial.println("got a response!");
        // should be a znet tx status            	
       if (xbee.getResponse().getApiId() == ZB_TX_STATUS_RESPONSE) 
       {
           xbee.getResponse().getZBTxStatusResponse(txStatus);

           // get the delivery status, the fifth byte
          if (txStatus.getDeliveryStatus() == SUCCESS) 
          {
              // success.  time to celebrate
              mySerial.println("success.");
          } 
          else {
              // the remote XBee did not receive our packet. is it powered on?
              mySerial.println("the remote XBee did not receive our packet");
          }
       }
       else if(xbee.getResponse().getApiId() == ZB_RX_RESPONSE) 
       {
          // got a zb rx packet
          // now fill our zb rx class
          xbee.getResponse().getZBRxResponse(rx);
      
          mySerial.println("Got an rx packet!");
          if (rx.getOption() == ZB_PACKET_ACKNOWLEDGED) 
          {
              // the sender got an ACK
            mySerial.println("packet acknowledged");
          } 
          else 
          {
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
          for (i = 0; i < rx.getDataLength(); i++) 
          {
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
    } 
    else if (xbee.getResponse().isError()) 
    {
        mySerial.print("Error reading packet.  Error code: ");  
        mySerial.println(xbee.getResponse().getErrorCode());
    } 
    else 
    {
        // local XBee did not provide a timely TX Status Response -- should not happen
        mySerial.println("No TX Status Response");
    }
}

static int protothread_send(struct pt *pt) 
{  
    PT_BEGIN(pt);  
    while(1) 
    {  
        PT_WAIT_UNTIL(pt, counter_send==10); 
        send_data();
        counter_send=0;   
    } 
    PT_END(pt); 
} 
 
 
static int protothread_receive(struct pt *pt) 
{ 
    PT_BEGIN(pt); 
    while(1) 
    {    
        PT_WAIT_UNTIL(pt, counter_receive==1); 
        receive_data();
        counter_receive=0; 
    } 
    PT_END(pt); 
} 

void setup()
{
    Serial.begin(115200);
    xbee.setSerial(Serial);
  
    while (!Serial) 
    {
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
    PT_INIT(&pt_send);  //线程1初始化
    PT_INIT(&pt_receive);  //线程2初始化
}



void loop()
{
    protothread_send(&pt_send); 
    protothread_receive(&pt_receive); 

    counter_send++; 
    counter_receive++; 
}
//
// END OF FILE
//
