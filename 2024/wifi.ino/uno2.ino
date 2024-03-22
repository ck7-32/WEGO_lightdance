#include "FastLED.h" 
#include <SPI.h>

#define LP_PIN 13  //左褲子
#define RP_PIN 12  //右褲子
#define LC_PIN 11  //左衣服
#define RC_PIN 10  //右衣服
#define CD_PIN 9   //下半衣
#define HD_PIN 8   //頭貓耳
//設定燈數量
#define LP_NUM 7    
#define RP_NUM 7
#define LC_NUM 8
#define RC_NUM 9
#define CD_NUM 2
#define HD_NUM 2

#define LED_TYPE WS2812 
#define COLOR_ORDER GRB
#define T_LEN 96//陣列數
#define LEN 6  // 不位數
//顏色陣列
//設定燈陣
CRGB color[] = {CRGB::Black, CRGB::Purple, CRGB::Pink, CRGB::Blue, CRGB::White};
/// 設定時間陣列
byte A[T_LEN] ={0, 1, 2, 3, 4, 3, 4, 3, 4, 3, 4, 2, 5, 4, 6, 7, 8, 9, 10, 1, 2, 4, 2, 4, 2, 4, 8, 11, 2, 11, 2, 11, 2, 12, 13, 12, 13, 12, 13, 12, 13, 12, 13, 12, 13, 12, 13, 12, 13, 12, 13, 8, 5, 8, 5, 8, 5, 8, 5, 8, 5, 8, 5, 2, 4, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 10, 14, 10, 14, 10, 14, 10, 14, 10, 14, 10, 14, 1};
byte colorPlate[15][LEN] = {{6,7,0,6,5}, {6,7,2,6,5}, {0,0,0,0,0}, {3,3,3,3,3}, {1,1,1,1,1}, {5,5,5,5,5}, {0,0,0,0,7}, {7,7,0,7,7}, {7,7,7,7,7}, {0,7,0,0,0}, {6,7,2,6,0}, {6,6,6,6,6}, {7,7,7,7,5}, {5,5,5,5,7}, {0,0,0,0,5} };
int Time_lst[T_LEN] = {0, 779, 4047, 11458, 11955, 12451, 12948, 13445, 13942, 14440, 14937, 15443, 16400, 17762, 21498, 21639, 21780, 25230, 25371, 25512, 32833, 33262, 33692, 34122, 34552, 34982, 35413, 36338, 36798, 37258, 37718, 38178, 38637, 39103, 39984, 40426, 40867, 41307, 41749, 42190, 42631, 43072, 43513, 43954, 44395, 44835, 45277, 45718, 46158, 46600, 47041, 47479, 47935, 48390, 48847, 49302, 49759, 50214, 50670, 51127, 51582, 52039, 52494, 52952, 53845, 54797, 55226, 55656, 56086, 56516, 56946, 57376, 57806, 58236, 58666, 59096, 59527, 59956, 60387, 60816, 61246, 61676, 62106, 62100, 62569, 63038, 63507, 63975, 64445, 64914, 65382, 65852, 66320, 66790, 67259, 67722};
uint8_t max_bright = 255;
int lst_time = 0;

//設置燈條
CRGB lps[LP_NUM]; 
CRGB rps[RP_NUM];
CRGB lcs[LC_NUM];
CRGB rcs[RC_NUM];
CRGB cds[CD_NUM];
CRGB hds[HD_NUM];
void setup() {
   Serial.begin(9600);
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
   FastLED.show();
   FastLED.setBrightness(max_bright);
   Serial.print("reset\n");
}
void dance();
void connecting_light();
void loop() {
      fill_solid(lcs, LC_NUM, CRGB::Black);
      fill_solid(rcs, RC_NUM, CRGB::Black);
      fill_solid(cds, CD_NUM, CRGB::Black);
      fill_solid(hds, HD_NUM, CRGB::Black);
      fill_solid(lps, LP_NUM, CRGB::Black);
      fill_solid(rps, RP_NUM, CRGB::Black);
      int signalValue = digitalRead(5);//esp32 22
      int connecting = digitalRead(6);//23
      if (connecting == 1){
         connecting_light();
      }
      if (signalValue == 1){
         dance();
      }
      else{
        Serial.print("0\n");
      }
}
void dance() {
   delay(100);
      int signalValue = digitalRead(5);//esp32 22
      int connecting = digitalRead(6);//23
    if(signalValue == 1){
      Serial.print("startdance");
      for(int i = 0;i<T_LEN;i++){
      int Time = Time_lst[i];
      int Delay = Time - lst_time;
      delay(Delay);
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
}
void connecting_light(){
    delay(100);
    int signalValue = digitalRead(5);//esp32 22
    int connecting = digitalRead(6);//23
    if(connecting == 1){
      Serial.print("connecting");
      for(int i=0;i<3;i++){
          fill_solid(lcs, LC_NUM, CRGB::Blue);
          fill_solid(rcs, RC_NUM, CRGB::Blue);
          fill_solid(cds, CD_NUM, CRGB::Blue);
          fill_solid(hds, HD_NUM, CRGB::Blue);
          fill_solid(lps, LP_NUM, CRGB::Blue);
          fill_solid(rps, RP_NUM, CRGB::Blue);
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
        }
    }
}