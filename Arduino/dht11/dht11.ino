// 
//   FILE:  dht_test.pde
// PURPOSE: DHT library test sketch for Arduino
//

#include <dht.h>

dht DHT;

#define DHT11_PIN 4//put the sensor in the digital pin 4

void humidity_func(double humidity)
{
  //humidity conditions
  if(humidity > 0 && humidity < 40)
  {
    // increase
    Serial.println("\t humidity increase");
  }
  else if(humidity >= 40 && humidity < 80)
  {
    // ok
    Serial.println("\t humidity ok");
  }
  else if(humidity >= 80 && humidity < 100)
  {
    //decrease
    Serial.println("\t humidity decrease");
  }
  else
  {
    // error
    Serial.println("\t humidity error");
  }
}

void temperature_func(double temperature)
{
  //temperature conditions
  if(temperature < 10)
  {
    // increase
    Serial.println("\t temperature increase");
  }
  else if(temperature >= 10 && temperature < 30)
  {
    // ok
    Serial.println("\t temperature ok");
  }
  else if(temperature >= 30)
  {
    //decrease
    Serial.println("\t temperature decrease");
  }
  else
  {
    // error
    Serial.println("\t temperature error");
  }
}

void setup()
{
  Serial.begin(9600);
  Serial.println("DHT TEST PROGRAM for Fast Planting System");
  Serial.print("LIBRARY VERSION: ");
  Serial.println(DHT_LIB_VERSION);
  Serial.println();
  Serial.println("Type,\tstatus,\tHumidity (%),\tTemperature (C)");
}

void loop()
{

  // READ DATA
  Serial.print("DHT11, \t");
 int chk = DHT.read11(DHT11_PIN);
  switch (chk)
  {
    case 0:  Serial.print("OK,\t"); break;
    case -1: Serial.print("Checksum error,\t"); break;
    case -2: Serial.print("Time out error,\t"); break;
    default: Serial.print("Unknown error,\t"); break;
  }
 // DISPLAT DATA
  Serial.print(DHT.humidity,1);
  Serial.print(",\t");
  Serial.println(DHT.temperature,1);
  
  humidity_func(DHT.humidity);
  temperature_func(DHT.temperature);

  delay(3000);
}
//
// END OF FILE
//

