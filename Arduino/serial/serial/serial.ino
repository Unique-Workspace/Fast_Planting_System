String comdata = "";
int ledPin = 10;
int val;

void setup()
{
    pinMode(ledPin, OUTPUT);
    Serial.begin(9600);
}

void loop()
{

  Serial.print('A');
  delay(1000);
  val = Serial.read();
  if (-1 != val)
  {
    if ('A' == val)
    {
      digitalWrite(ledPin, HIGH);
      delay(500);
      digitalWrite(ledPin, LOW);
      delay(500);
    }
  }

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
