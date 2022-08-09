#define S0 9
#define S1 10
#define S2 11
#define S3 12
#define OUT 13

int r=0;
int g=0;
int b=0;

void setup(){
  pinMode(S0, OUTPUT); //đầu ra cho chân S0
  pinMode(S1, OUTPUT);
  pinMode(S2, OUTPUT);
  pinMode(S3, OUTPUT);
  
  //đầu vào cho cảm biến
  pinMode(OUT, INPUT);

  digitalWrite(S0,HIGH); //Xuất tín hiệu ra chân Digital
  digitalWrite(S1,LOW);  //Xuất tín hiệu ra chân Digital

  //Mở 9600
  Serial.begin(9600);
}

void readColor(){
  digitalWrite(S2,LOW);
  digitalWrite(S3,LOW);
  r=pulseIn(OUT,LOW);
  delay(50);

  digitalWrite(S2,HIGH);
  digitalWrite(S3,HIGH);
  g=pulseIn(OUT,LOW);
  delay(50);

  digitalWrite(S2,LOW);
  digitalWrite(S3,HIGH);
  b=pulseIn(OUT,LOW);
  delay(50);

  Serial.println("R= "+(String)r+" G= "+(String)g+" B= "+(String)b);
}

void loop(){
  readColor();
  delay(500);
}
