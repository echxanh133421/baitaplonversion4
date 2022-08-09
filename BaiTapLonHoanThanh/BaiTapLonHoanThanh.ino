//gọi thư viện dành cho servo
#include<Servo.h>

//định nghĩa chân của cảm biến màu sắc với chân digital
#define S0 9
#define S1 10
#define S2 11
#define S3 12
#define sensorOut 13

//định nghĩa chân mạch đk động cơ L298N
#define IN1  2
#define IN2  3

//định nghĩa tốc độ động cơ
#define MAX_SPEED 255
#define MIN_SPEED 0

int c;

//khai báo nối chân cảm biến hồng ngoại với chân digital của Arduino
int cam_bien_0=6;
int cam_bien_1=7;
int cam_bien_2=8;

//tạo 2 biến myservo1-2
Servo myservo1;
Servo myservo2;

//khai báo các tần số để đọc màu
int red=0;
int green=0;
int blue=0;

//ma trận 3 hàng tương ứng phân loại 3 màu
int colors[3][6];


void setup()
{
  //thiết lập chân digital cho 2 servo
  myservo1.attach(4);
  myservo2.attach(5);
  myservo1.write(0);
  myservo2.write(0);

  //thiết lập cho các chân của cảm biến màu sắc là OUTPUT
  pinMode(S0,OUTPUT);
  pinMode(S1,OUTPUT);
  pinMode(S2,OUTPUT);
  pinMode(S3,OUTPUT);

  //tương tự chân của L298N
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);

  //thiêt lập sensorOut là chân nhập, đưa dữ liệu vào arduino xử lý
  pinMode(sensorOut,INPUT);

  //thang đo tần số là 20%
  digitalWrite(S0,HIGH);
  digitalWrite(S1,LOW);

  //mở giao tiếp serial
  Serial.begin(9600);
}

//hàm phân biệt màu sắc
int read_color()
{
  //cụm câu lệnh để lọc màu đỏ
  digitalWrite(S2,LOW);
  digitalWrite(S3,LOW);
  red=pulseIn(sensorOut,LOW);
  delay(50);

  //cụm câu lệnh để lọc màu xanh lá
  digitalWrite(S2,HIGH);
  digitalWrite(S3,HIGH);
  green=pulseIn(sensorOut,LOW);
  delay(50);

  //cụm câu lệnh để lọc màu xanh dương
  digitalWrite(S2,LOW);
  digitalWrite(S3,HIGH);
  blue=pulseIn(sensorOut,LOW);
  delay(50);

  //vòng lặp phân biệt màu sắc
  for(int i=0;i<3;i++){
     if(red>=colors[i][0] && red<=colors[i][1] &&
        green>=colors[i][2] && green<=colors[i][3] &&
        blue>=colors[i][4]&& blue<=colors[i][5])
     {
            return i;
     }
  }
  return -1;
}


//hàm khai báo dải màu được khảo sát trước
void initColor()
{
  //RED
  colors[0][0]=20; //Min R
  colors[0][1]=60;

  colors[0][2]=88; //Min G
  colors[0][3]=128;

  colors[0][4]=71; //Min B
  colors[0][5]=111;
  //----------------------
  //GREEN
  colors[1][0]=60; //Min R
  colors[1][1]=100;

  colors[1][2]=46; //Min G
  colors[1][3]=86;

  colors[1][4]=58; //Min B
  colors[1][5]=98;

  //BLUE
  colors[2][0]=72; //Min R
  colors[2][1]=112;

  colors[2][2]=55; //Min G
  colors[2][3]=95;

  colors[2][4]=27; //Min B
  colors[2][5]=67;
}


void dieu_khien_cam_bien_hong_ngoai(int cam_bien_thu_i)
{
  int cam_bien;
  Servo myservo;
  if(cam_bien_thu_i==1)
  {
    cam_bien = cam_bien_1;
    myservo = myservo1;
  }
  else if(cam_bien_thu_i==2)
  {
    cam_bien = cam_bien_2;
    myservo = myservo2;
  }

  //đọc giá trị trả về của cảm biến
  int gia_tri = digitalRead(cam_bien);

  //cảm biến nhận tín hiệu trả về giá trị 0, không nhận tín hiệu trả về giá trị 1
  if(gia_tri==0)
  {
    if(cam_bien_thu_i==1)
    {
      Serial.print("red");
    }
    else if(cam_bien_thu_i==2)
    {
      Serial.print("blue");
    }
    myservo.write(50);
    delay(3000);
    myservo.write(-50);

    c=10; //Thay doi gia tri cua c de thoat vong lap
  }
}

//hàm điều khiển động cơ
void motor_Dung() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
}
void motor_Tien(int speed) { //speed: từ 0 - MAX_SPEED
  speed = constrain(speed, MIN_SPEED, MAX_SPEED);//đảm báo giá trị nằm trong một khoảng từ 0 - MAX_SPEED
  digitalWrite(IN1, HIGH);
  analogWrite(IN2, 255 - speed);
}

void hamchinh(int gia_tri){
    if(gia_tri==0){
    //c là giá trị trả về của hàm read_color(); (0;1;2)
    c=read_color();
    if(c>-1){
      while(c==0){
        dieu_khien_cam_bien_hong_ngoai(1);
        }

      //nếu c=1 thì là màu xanh lá, có nghĩa là đi thẳng
      while(c==1){
        //sử dụng cảm biên 2 để đọc số lượng màu xanh lá gửi về giao diện
        int gia_tri = digitalRead(cam_bien_2);
        if(gia_tri==0){
          c=10;
          Serial.print("green");
        }
      }
      while(c==2){
      dieu_khien_cam_bien_hong_ngoai(2);
      }
    }
  }
}

//biến x nhận tín hiệu từ giao diện trả về
String x;

void loop(){
  //đọc giá trị tốc độ động cơ trả về từ giao diện
  if(Serial.available()>0){
    x=Serial.readString();
    int y=x.toInt();
    motor_Tien(y);
  }

  //đọc giá trị trả về của cảm biến hồng ngoại 0
  int gia_tri=digitalRead(cam_bien_0);
  initColor();
  hamchinh(gia_tri);

  }
