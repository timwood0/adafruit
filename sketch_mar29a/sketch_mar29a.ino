/* 
Blink Turns on an LED on for one second, 
then off for one second, repeatedly. This 
example code is in the public domain. 
*/
// Pin 2 has an LED connected on the NodeMCU ESP8266 boards. 
// Give it a name:
int led = 2; 
// the setup routine runs once when you press reset: 
void setup()
{
  // initialize the digital pin as an output.  
  pinMode(led, OUTPUT);
}
// the loop routine runs over and over again forever:
void loop()
{
  subrtn();
}

void subrtn() {
  digitalWrite(led, HIGH / 2); // turn the LED on (HIGH is the voltage level)  
  delay(1000); // wait for a second  
  digitalWrite(led, LOW); // turn the LED off by making the voltage LOW  
  delay(1000); // wait for a second 
}


