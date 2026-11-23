#include <LiquidCrystal.h>

//const int rs=12, en=11, d4=5, d5=4, d6=3, d7=2;
const int rs=7, en=8, d4=9, d5=10, d6=11, d7=12;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

void setup() {
  lcd.begin(16,2);
  delay(2000);
}

void loop(){
  lcd.print("Hello, World!");
  delay(3000);
  lcd.clear();



//   Initialize char variable and pass to scrollLeft function
  char myText[] = "Chicken Butt!!!";
  scrollLeft(myText);

//  testLCD();
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
  lcd.clear();
}