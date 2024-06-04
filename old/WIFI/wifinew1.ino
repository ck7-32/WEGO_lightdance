#include "FastLED.h" 
#include "WiFi.h"
#include <WebServer.h>
#include <SPI.h>


///設定燈光
///設定pin
#define LP_PIN 32  //左褲子
#define RP_PIN 33  //右褲子 1
#define LC_PIN 26  //左衣服 0
#define RC_PIN 25  //右衣服
#define CD_PIN 18  //下半衣 2
#define HD_PIN 5  //頭貓耳3
//設定燈數量
#define LP_NUM 7    
#define RP_NUM 7
#define LC_NUM 8
#define RC_NUM 9
#define CD_NUM 2
#define HD_NUM 2

#define LED_TYPE WS2812B 
#define COLOR_ORDER GRB
#define T_LEN 92//陣列數
#define LEN 6  // 部位數m,j
//設定燈陣
CRGB color[] = {CRGB::Black, CRGB::Purple, CRGB::Pink, CRGB::Blue, CRGB::White};
/// 設定時間陣列
byte A[T_LEN] = {0, 1, 2, 3, 4, 5, 4, 5, 4, 5, 4, 5, 2, 3, 2, 4, 1, 5, 4, 2, 4, 2, 4, 2, 5, 6, 2, 6, 2, 6, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 4, 3, 5, 3, 5, 3, 5, 3, 5, 3, 5, 3, 5, 3, 5, 3, 5, 3, 5, 3, 5, 3, 5, 3, 5, 3, 5, 3, 5, 2, 1};
byte colorPlate[15][LEN] = {{6,7,0,6,5}, {6,7,2,6,5}, {0,0,0,0,0}, {5,5,5,5,5}, {1,1,1,1,1}, {7,7,7,7,7}, {6,6,6,6,6} };
int Time_lst[T_LEN] ={0, 779, 4047, 8677, 11458, 11955, 12451, 12948, 13445, 13942, 14440, 14937, 15443, 16400, 17762, 17898, 21571, 28990, 32833, 33262, 33692, 34122, 34552, 34982, 35413, 36338, 36798, 37258, 37718, 38178, 38637, 39103, 39360, 40295, 40763, 41231, 41700, 42167, 42635, 43103, 43572, 44039, 44507, 44975, 45444, 45911, 46379, 46847, 47316, 47783, 48251, 48719, 49188, 49655, 50123, 50591, 51060, 51527, 51995, 52463, 52952, 54113, 54797, 55684, 56128, 56573, 57016, 57460, 57904, 58348, 58792, 59236, 59680, 60125, 60568, 61012, 61456, 61900, 62344, 62788, 63232, 63676, 64120, 64564, 65009, 65453, 65896, 66340, 66784, 67228, 67697, 67722};
uint8_t max_bright = 255;
int lst_time = 0;
int Start = 0 ;
int Connecting = 0;
///設定WIFI
const char* ssid ="WEGOligntdance";       // 雙引號內，修改為你要 ESP32 連上的 WiFi 網路名稱 SSID
const char* password = "Wgld2023wifi";  


WebServer server(80);  //設定網路伺服器 port number 為 80

// Variable to store the HTTP request
String header;

String output26State = "off";  //設定字串變數 output26State，顯示 GPIO26 狀態。如果您要增加可控制的 GPIO 數目，請在這裡增加
String output27State = "off";

//設置燈條
CRGB lps[LP_NUM]; 
CRGB rps[RP_NUM];
CRGB lcs[LC_NUM];
CRGB rcs[RC_NUM];
CRGB cds[CD_NUM];
CRGB hds[HD_NUM];

void start(){
    Connecting = 0;
    Start = 1;
    server.send(200,"text/html","啟動");
    Serial.print("start");
    delay(1000);
}
void test(){
    Start = 0;
    Connecting = 1;
    server.send(201,"text/html","測試");
    delay(1000);
    Serial.print("test");
}
void getstate(){
    server.send(203,"text/html","測試");
    delay(1000);
    if(Start==0){
      Serial.print("hasnt start");
    }
    if(Start==1){
      Serial.print("started");
    }
};
void connecting_light(){

         fill_solid(lcs, LC_NUM, colorPlate[2][0]);
         fill_solid(rcs, RC_NUM, colorPlate[2][0]);
         fill_solid(cds, CD_NUM, colorPlate[2][1]);
         fill_solid(hds, HD_NUM, colorPlate[2][2]);
         fill_solid(lps, LP_NUM, colorPlate[2][4]);
         fill_solid(rps, RP_NUM, colorPlate[2][4]);
         FastLED.show();
         delay(500);
         fill_solid(lcs, LC_NUM, CRGB::Black);
         fill_solid(rcs, RC_NUM, CRGB::Black);
          fill_solid(cds, CD_NUM, CRGB::Black);
         fill_solid(hds, HD_NUM, CRGB::Black);
         fill_solid(lps, LP_NUM, CRGB::Black);
         fill_solid(rps, RP_NUM, CRGB::Black);
         FastLED.show();
         delay(500);

};
void setup() {
   Serial.begin(115200);
   //初始化燈條
   LEDS.addLeds<LED_TYPE, LP_PIN, COLOR_ORDER>(lps, LP_NUM);
   LEDS.addLeds<LED_TYPE, RP_PIN, COLOR_ORDER>(rps, RP_NUM); 
   LEDS.addLeds<LED_TYPE, LC_PIN, COLOR_ORDER>(lcs, LC_NUM);
   LEDS.addLeds<LED_TYPE, RC_PIN, COLOR_ORDER>(rcs, RC_NUM);
   LEDS.addLeds<LED_TYPE, CD_PIN, COLOR_ORDER>(cds, CD_NUM);
   LEDS.addLeds<LED_TYPE, HD_PIN, COLOR_ORDER>(hds, HD_NUM);
   fill_solid(lcs, LC_NUM, CRGB::Black);
   fill_solid(rcs, RC_NUM, CRGB::Black);
   fill_solid(cds, CD_NUM, CRGB::Black);
   fill_solid(hds, HD_NUM, CRGB::Black);
   fill_solid(lps, LP_NUM, CRGB::Black);
   fill_solid(rps, RP_NUM, CRGB::Black);
  
   FastLED.setBrightness(max_bright);
   Serial.print("reset\n");
   ///初始化WIFI
   // Set outputs to LOW
   Start = 0;

   Serial.print("Connecting to ");  // 連上你所指定的Wi-Fi，並在序列埠螢幕中，印出 ESP32 web server 的 IP address
   Serial.println(ssid);
   WiFi.begin(ssid, password);
   while (WiFi.status() != WL_CONNECTED) {
     delay(500);
     Serial.print(".");
     connecting_light();
  }
  // Print local IP address and start web server
  Serial.println("");
  Serial.println("WiFi connected.");

  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  //伺服器啟動
  server.on("/start",start);
  server.on("/test",test);
  server.on("/getstate",getstate);
  server.begin();
}
void dance();
void loop() {
     server.handleClient();
     fill_solid(lcs, LC_NUM, CRGB::Black);
     fill_solid(rcs, RC_NUM, CRGB::Black);
     fill_solid(cds, CD_NUM, CRGB::Black);
     fill_solid(hds, HD_NUM, CRGB::Black);
     fill_solid(lps, LP_NUM, CRGB::Black);
     fill_solid(rps, RP_NUM, CRGB::Black);
     if (Connecting == 1){
          connecting_light();
          delay(500);
     }
     if (Start == 1){
          dance();
       }
}
void dance() {
       for(int i = 0;i<T_LEN;i++){
       int Time = Time_lst[i];
       int Delay = Time - lst_time;
       delay(Delay * 10);
       //改變燈
       //改變下半衣
       fill_solid(cds, CD_NUM, color[colorPlate[A[i]][1]]);
       
       //改變上衣
       fill_solid(lcs, LC_NUM, color[colorPlate[A[i]][0]]);
       fill_solid(rcs, RC_NUM, color[colorPlate[A[i]][0]]);
       //改變袖子
       fill_solid(lcs+7, 2, color[colorPlate[A[i]][3]]);
       fill_solid(rcs+6, 2, color[colorPlate[A[i]][3]]);
      
      //改變褲子
      fill_solid(lps, LP_NUM, color[colorPlate[A[i]][4]]); //寫錯了5->4
      fill_solid(rps, RP_NUM, color[colorPlate[A[i]][4]]);
      //改變頭
      fill_solid(hds,HD_NUM, color[colorPlate[A[i]][2]]);
   
      lst_time = Time;
      //秀燈
      FastLED.show();
   }
}
