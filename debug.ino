#include "FastLED.h"           // 此示例程序需要使用FastLED库
 
#define NUM_LEDS1 6//帽子+貓耳
#define NUM_LEDS2 25 // 左手套
#define NUM_LEDS3 25 // 右手套
#define NUM_LEDS4 9//左半身
#define NUM_LEDS5 8//右半身
#define NUM_LEDS6 7//左褲子
#define NUM_LEDS7 7//右褲子


#define DATA_PIN1 17
#define DATA_PIN2 16
#define DATA_PIN3 32
#define DATA_PIN4 33
#define DATA_PIN5 25
#define DATA_PIN6 26
#define DATA_PIN7 14
#define DATA_PIN8 27

#define DANCERN 0//第幾個舞者
char colors[][20]=["#000000", "#269aff", "#ffffff", "#faff95", "#ff67b8", "#ff9d9f", "#ffa5ff", "#d9aeff", "#8ac8ff", "#82f3ff", "#97ffac", "#f5ff9e", "#ff8181"];
#define USEDPIN_NUM 7
// #define DATA_PIN8 27 // Not used in 7 types of lights
int lednums[]=[NUM_LEDS1,NUM_LEDS2,NUM_LEDS3,NUM_LEDS4,NUM_LEDS5,NUM_LEDS6,NUM_LEDS7];
int pins[]=[DATA_PIN1,DATA_PIN2,DATA_PIN3,DATA_PIN4,DATA_PIN5,DATA_PIN6,DATA_PIN7,DATA_PIN8];

//建立燈帶

CRGB LED1[NUM_LEDS1]; 
CRGB LED2[NUM_LEDS2];
CRGB LED3[NUM_LEDS3];
CRGB LED4[NUM_LEDS4];
CRGB LED5[NUM_LEDS5];
CRGB LED6[NUM_LEDS6];
CRGB LED7[NUM_LEDS7];
CRGB* LEDs[] = {
  LED1, LED2, LED3, LED4, LED5, LED6, LED7
};
//定義部位
//[0"衣服", 1"貓耳", 2"帽子",3 "左手環",4 "右手環", 5"左手臂",6 "右手臂",7 "左手套",8 "右手套",9 "左短褲",10 "右短褲",11 "左長褲",12 "右長褲"]

int LEDPART1[NUM_LEDS1]={2,2,2,2,1,1};//帽子+貓耳
int LEDPART2[NUM_LEDS2]={6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6};//左手套
int LEDPART3[NUM_LEDS3]={7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7};//右手套
int LEDPART4[NUM_LEDS4]={0,0,0,0,0,6,4,4,6};//左半身
int LEDPART5[NUM_LEDS5]={0,0,0,0,5,3,3,5};//右半身
int LEDPART6[NUM_LEDS6]={10,12,12,10,12,12,12};//左褲子
int LEDPART7[NUM_LEDS7]={9,11,11,9,11,11,11};//右褲子
int* LEDs[]={
  LEDPART1,LEDPART2,LEDPART3,LEDPART4,LEDPART5,LEDPART6,LEDPART7
};

#define LED_TYPE WS2812         // LED灯带型号
#define COLOR_ORDER GRB         // RGB灯珠中红色、绿色、蓝色LED的排列顺序
 
uint8_t max_bright = 255;       // LED亮度控制变量，可使用数值为 0 ～ 255， 数值越大则光带亮度越高
 
CRGB leds[NUM_LEDS];            // 建立光带leds

int data[1][13]=[[1,2,3,4,5,6,7,8,9,10,11,12,13]] 
void setup() {  
  FastLED.addLeds<WS2812, DATA_PIN1, GRB>(leds[0], NUM_LEDS1);
  FastLED.addLeds<WS2812, DATA_PIN2, GRB>(leds[1], NUM_LEDS2);
  FastLED.addLeds<WS2812, DATA_PIN3, GRB>(leds[2], NUM_LEDS3);
  FastLED.addLeds<WS2812, DATA_PIN4, GRB>(leds[3], NUM_LEDS4);
  FastLED.addLeds<WS2812, DATA_PIN5, GRB>(leds[4], NUM_LEDS5);
  FastLED.addLeds<WS2812, DATA_PIN6, GRB>(leds[5], NUM_LEDS6);
  FastLED.addLeds<WS2812, DATA_PIN7, GRB>(leds[6], NUM_LEDS7);
}
void loop() { 
for(int ledstring=0;ledstring<USEDPIN_NUM;ledstring++){
    for(int led=0;led<lednums[ledstring];led++){
      int nowcolorindex=data[0][led];
      LEDs[ledstring][lednums]=colors[nowcolorindex];
    }
  }
  FastLED.show();
}
