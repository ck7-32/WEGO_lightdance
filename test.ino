#include "FastLED.h"           // 此示例程序需要使用FastLED库
 
#define NUM_LEDS 30          // LED灯珠数量
#define DATA_PIN 10              // Arduino输出控制信号引脚
#define LED_TYPE WS2812         // LED灯带型号
#define COLOR_ORDER GRB         // RGB灯珠中红色、绿色、蓝色LED的排列顺序
 
uint8_t max_bright = 255;       // LED亮度控制变量，可使用数值为 0 ～ 255， 数值越大则光带亮度越高
 
CRGB leds[NUM_LEDS];            // 建立光带leds
 
void setup() {  
  LEDS.addLeds<LED_TYPE, DATA_PIN, COLOR_ORDER>(leds, NUM_LEDS);  // 初始化光带 
  FastLED.setBrightness(max_bright);                            // 设置光带亮度
}
int R,G,B; 
void loop() { 
  fill_solid(leds,30,CRGB::Red)  ;     // 设置光带中第一个灯珠颜色为红色，leds[0]为第一个灯珠，leds[1]为第二个灯珠
  FastLED.show();                // 更新LED色彩
  delay(500);       
  fill_solid(leds,30,CRGB::Green) ;      // 设置光带中第一个灯珠颜色为红色，leds[0]为第一个灯珠，leds[1]为第二个灯珠
  FastLED.show();                // 更新LED色彩
  delay(500); 
  fill_solid(leds,30,CRGB::Blue);       // 设置光带中第一个灯珠颜色为红色，leds[0]为第一个灯珠，leds[1]为第二个灯珠
  FastLED.show();                // 更新LED色彩
  delay(500);               // 等待500毫秒
}