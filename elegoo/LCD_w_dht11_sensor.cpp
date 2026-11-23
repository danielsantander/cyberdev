

#include <LiquidCrystal.h>
#include <dht.h>
#include <math.h>

//const int rs=12, en=11, d4=5, d5=4, d6=3, d7=2;
const int rs=7, en=8, d4=9, d5=10, d6=11, d7=12;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

//#define DHT11_PIN 7
//#define DHT11_PIN A0
#define DHT11_PIN 2
dht DHT;


void setup() {

  Serial.begin(9600);
  delay(500); //delay to let systems boot

  lcd.begin(16,2);  // initialize interface to the LCD screen w/ specific dimensions (width & height)
  lcd.clear();
  lcd.print("Getting");
  lcd.setCursor(0,1);
  lcd.print("Temp & Humidity");
  delay(2000);
  lcd.clear();
}

void loop(){
  PrintToLCD();
}



void PrintToLCD(){
  int chk = DHT.read11(DHT11_PIN);
  float t_c = DHT.temperature;
  float t_f = celsius_to_fahrenheit(t_c);
  float h = DHT.humidity;
  t_f = roundf(t_f * 100)/100;  // round float to nearset hundreth decimal place
  t_c = roundf(t_c * 100)/100;  // round float to nearest hundreth decimal palce
  lcd.setCursor(0,0);
  lcd.print("Temp: ");
  lcd.print(t_f);
  lcd.print(" F");
  lcd.setCursor(0,1);
  lcd.print("Hum: ");
  lcd.print(h);
  lcd.print(" %");
  delay(3000);



}


void PrintToMonitor(){
  int chk = DHT.read11(DHT11_PIN);
  float t_c = DHT.temperature;
  float t_f = celsius_to_fahrenheit(t_c);
  float h = DHT.humidity;
  Serial.print("Temperature (celsius) = ");
  Serial.print(t_c);
  Serial.println("C ");
  Serial.print("Temperature (fahrenheit) = ");
  Serial.print(t_f);
  Serial.println("F ");
  Serial.print("Humidity = ");
  Serial.print(h);
  Serial.println("% ");
  Serial.print("\n");
  delay(5000);

  // LCD code
  //lcd.print("Hello, World!");
  //delay(3000);
  //lcd.clear();
  // Initialize char variable and pass to scrollLeft function
  //char myText[] = "Chicken Butt!!!";
  //scrollLeft(myText);

}

float celsius_to_fahrenheit(float celsius){
  float fahrenheit;
  fahrenheit = (celsius) * (1.8) + 32;
  return fahrenheit;
}

void scrollLeft(char *text){

  //lcd.print("CHICKEN BUTT!!! :)");
  if (text == NULL){
    char text[] = "No text";
  }
  lcd.print(text);
  delay(3000);
  for (int positionCounter = 0; positionCounter < 16; positionCounter++){
    lcd.scrollDisplayLeft();
    delay(1000);
  }
  lcd.clear();
}

void testLCD() {
  lcd.clear();
  lcd.print("printing text");

  delay(3000);

  lcd.clear();
  lcd.setCursor(0,1);
  lcd.print("setting cursor");

  delay(3000);

  lcd.clear();
  lcd.print("blink cursor");
  lcd.blink();

  delay(3000);
}