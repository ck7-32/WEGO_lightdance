#include <Arduino.h>
#include <FastLED.h>
#include <WiFi.h>
#include <WebServer.h>


#define NUM_LEDS 100            
#define LED_DT 17              
#define LED_TYPE WS2812  
#define COLOR_ORDER GRB         // RGB灯珠中红色、绿色、蓝色LED的排列顺序

 
uint8_t max_bright = 255;       
CRGB leds[NUM_LEDS];  


const char* ssid = "WEGOlightdance";
const char* password = "Wgld2023wifi";

WebServer server(80);

int ledCount = NUM_LEDS;  // 新增變數來儲存滑桿的值

CRGB hexToColor(const char* hexCode) {
    long number = (long) strtol(hexCode + 1, NULL, 16);
    byte r = number >> 16;
    byte g = number >> 8 & 0xFF;
    byte b = number & 0xFF;
    return CRGB(r, g, b);
}


void setup()
{
    Serial.begin(115200);
    LEDS.addLeds<LED_TYPE, LED_DT, COLOR_ORDER>(leds, NUM_LEDS);  
  
    FastLED.setBrightness(max_bright);    
    Serial.print("Connecting to ");
    Serial.println(ssid);

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }

    Serial.println("Connected to WiFi");
    Serial.printf("IP address: %s\n", WiFi.localIP().toString().c_str());

    server.on("/", handleRoot);
    server.on("/setcolor", handleSetColor);
    server.on("/setledcount", handleSetLEDCount);  // 新增處理滑桿變更的路由
    server.begin();
    Serial.println("HTTP server started");
}

void loop()
{
     server.handleClient();

}

void handleRoot() {
    String html = "<html><body style='background-color: black;'><h1 style='color: white; font-family: sans-serif;'></h1>";
    html += "<div id='wegoText' style='font-size: 48px; color: white; text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #fff, 0 0 40px #fff, 0 0 50px #fff, 0 0 60px #fff, 0 0 70px #fff; font-family: sans-serif; font-weight: bold;'>WEGO LIGHTDANCE</div>";
    html += "<input type='range' id='ledCountSlider' min='0' max='100' value='100' style='width: 100%;'>";  // 新增滑桿
    html += "<span id='ledCountValue' style='color: white;'>100</span>";  // 新增顯示數值的元素
    html += "<script src='https://cdn.jsdelivr.net/npm/@jaames/iro@5'></script>";
    html += "<script>";
    html += "var colorPicker = new iro.ColorPicker('#wegoText', { width: 320, color: '#f00' });";
    html += "setInterval(function() {";
    html += "var color = colorPicker.color.hexString.substring(1);";
    html += "var xhr = new XMLHttpRequest();";
    html += "xhr.open('GET', '/setcolor?color=' + color, true);";
    html += "xhr.send();";
    html += "}, 50);"; // 每0.5秒更新一次顏色
    html += "document.getElementById('ledCountSlider').addEventListener('input', function() {";  // 新增滑桿變更事件
    html += "var ledCount = this.value;";
    html += "document.getElementById('ledCountValue').innerText = ledCount;";  // 更新顯示數值
    html += "var xhr = new XMLHttpRequest();";
    html += "xhr.open('GET', '/setledcount?count=' + ledCount, true);";
    html += "xhr.send();";
    html += "});";
    html += "</script></body></html>";
    server.send(200, "text/html", html);
}

void handleSetColor() {
    String color = server.arg("color");
    long number = strtol(color.c_str(), NULL, 16);
    int r = number >> 16;
    int g = (number >> 8) & 0xFF;
    int b = number & 0xFF;
    CRGB playcolor = CRGB(r, g, b);
    playh(playcolor);
    server.send(200, "text/plain", "Color set");
}

void handleSetLEDCount() {
    String count = server.arg("count");
    ledCount = count.toInt();  // 更新 ledCount 變數
    server.send(200, "text/plain", "LED count set");
}

void playh(CRGB playcolor)
{
    fill_solid(leds, ledCount, playcolor);  // 根據 ledCount 變數來控制亮幾顆 LED
    fill_solid(leds + ledCount, NUM_LEDS - ledCount, CRGB::Black);  // 將剩餘的 LED 設置為黑色
    FastLED.show();
}