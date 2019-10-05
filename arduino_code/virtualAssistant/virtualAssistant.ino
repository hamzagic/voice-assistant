int red = 8;
int yellow = 9;
int green = 10;
String input = "";
bool stringComplete = false;

void setup() {
  pinMode(red, OUTPUT);
  pinMode(yellow, OUTPUT);
  pinMode(green, OUTPUT);
  Serial.begin(9600);
  input.reserve(200);
}

void loop() {
  if(stringComplete) {
    Serial.print("Assistente falando: ");
    Serial.print(input);
    if(input.startsWith("vermelho")) {
      digitalWrite(red, HIGH);
      digitalWrite(yellow, LOW);
      digitalWrite(green, LOW);
      Serial.print("Vermelho ligado");
    }
    if(input.startsWith("amarelo")) {
      digitalWrite(red, LOW);
      digitalWrite(yellow, HIGH);
      digitalWrite(green, LOW);
      Serial.print("Amarelo ligado");
    }
    if(input.startsWith("verde")) {
      digitalWrite(red, LOW);
      digitalWrite(yellow, LOW);
      digitalWrite(green, HIGH);
      Serial.print("Verde ligado");
    }
    input = "";
    stringComplete = false;
  }

  
}

 void serialEvent() {
    while(Serial.available()) {
      char inChar = (char)Serial.read();
      input += inChar;
      if(inChar == '\n') {
        stringComplete = true;
      }
    }
  }
