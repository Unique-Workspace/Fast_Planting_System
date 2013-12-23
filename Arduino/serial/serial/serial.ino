String comdata = "";
int ledPin = 10;
int val;
int int32_cmd;

void setup()
{
    pinMode(ledPin, OUTPUT);
    Serial.begin(9600);
}

void loop()
{
  int i;
  //Serial.print('A');
  //delay(1000);
  while (Serial.available() > 0)  
  {
      comdata += char(Serial.read());
      delay(2);
  }
  if (comdata.length() == 4)
  {
      Serial.print(comdata);
      comdata = "";
  }
  /*
  if (-1 != int32_cmd)
  {
    Serial.print(int32_cmd);
    if (0x1004FFF == int32_cmd)
    {
      digitalWrite(ledPin, HIGH);
      delay(500);
      digitalWrite(ledPin, LOW);
      delay(500);
    }
    else if('A' == int32_cmd)
    {
      digitalWrite(ledPin, HIGH);
      delay(100);
      digitalWrite(ledPin, LOW);
      delay(100);
    }
  }
*/
 /***
  digitalWrite(ledPin, HIGH); //点亮小灯
  delay(1000); //延时1 秒
  digitalWrite(ledPin, LOW); //熄灭小灯
  delay(1000); // 延时1 秒
Serial.println('LED');
 
    while (Serial.available() > 0)  
    {
        comdata += char(Serial.read());
        delay(2);
    }
    if (comdata.length() > 0)
    {
        Serial.println(comdata);
        comdata = "";
    }
***/
}
