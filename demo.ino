#include <Arduino.h>
#include <FastLED.h>
#include <WiFi.h>
#include <WebServer.h>

#define NUM_LEDS1 7 //貓耳帽子
#define NUM_LEDS2 2 //左手套
#define NUM_LEDS3 2 //右手套
#define NUM_LEDS4 13 //外套
#define NUM_LEDS5 3 //左鞋子
#define NUM_LEDS6 3 //右鞋子
#define NUM_LEDS7 4 //褲子
#define NUM_LEDS8 0 //

#define DATA_PIN1 17
#define DATA_PIN2 16
#define DATA_PIN3 32
#define DATA_PIN4 33
#define DATA_PIN5 25
#define DATA_PIN6 26
#define DATA_PIN7 14
#define DATA_PIN8 27

#define USEDPIN_NUM 7
#define COLOR_COUNT 12
            
#define DANCERN 3 //第幾個舞者

int lednums[]={NUM_LEDS1, NUM_LEDS2, NUM_LEDS3, NUM_LEDS4, NUM_LEDS5, NUM_LEDS6, NUM_LEDS7, NUM_LEDS8};
int pins[]={DATA_PIN1, DATA_PIN2, DATA_PIN3, DATA_PIN4, DATA_PIN5, DATA_PIN6, DATA_PIN7, DATA_PIN8};

CRGB LED1[NUM_LEDS1]; 
CRGB LED2[NUM_LEDS2];
CRGB LED3[NUM_LEDS3];
CRGB LED4[NUM_LEDS4];
CRGB LED5[NUM_LEDS5];
CRGB LED6[NUM_LEDS6];
CRGB LED7[NUM_LEDS7];
CRGB LED8[NUM_LEDS8];
CRGB* LEDstrings[] = {LED1, LED2, LED3, LED4, LED5, LED6, LED7, LED8};

int LEDPART1[NUM_LEDS1]={2, 2, 1, 1, 0, 1, 1};//貓耳帽子
int LEDPART2[NUM_LEDS2]={7, 7};//左手套
int LEDPART3[NUM_LEDS3]={8, 8};//右手套
int LEDPART4[NUM_LEDS4]={3, 3, 3, 3, 5, 3, 5, 6, 4, 4, 4, 4, 4};//外套
int LEDPART5[NUM_LEDS5]={11, 11, 11};//左鞋子
int LEDPART6[NUM_LEDS6]={12, 12, 12};//右鞋子
int LEDPART7[NUM_LEDS7]={9, 9, 10, 10};//褲子
int LEDPART8[NUM_LEDS8]={};//

int* leds[] = {LEDPART1, LEDPART2, LEDPART3, LEDPART4, LEDPART5, LEDPART6, LEDPART7, LEDPART8};

const char* ssid = "Wong88";
const char* password = "20070415";

WebServer server(80);


int y = 0;

CRGB hexToColor(const char* hexCode) {
    long number = (long) strtol(hexCode + 1, NULL, 16);
    byte r = number >> 16;
    byte g = number >> 8 & 0xFF;
    byte b = number & 0xFF;
    return CRGB(r, g, b);
}

CRGB colorArray[COLOR_COUNT];

void setup()
{
    Serial.begin(115200);
    FastLED.addLeds<WS2812, DATA_PIN1, GRB>(LEDstrings[0], NUM_LEDS1);
    FastLED.addLeds<WS2812, DATA_PIN2, GRB>(LEDstrings[1], NUM_LEDS2);
    FastLED.addLeds<WS2812, DATA_PIN3, GRB>(LEDstrings[2], NUM_LEDS3);
    FastLED.addLeds<WS2812, DATA_PIN4, GRB>(LEDstrings[3], NUM_LEDS4);
    FastLED.addLeds<WS2812, DATA_PIN5, GRB>(LEDstrings[4], NUM_LEDS5);
    FastLED.addLeds<WS2812, DATA_PIN6, GRB>(LEDstrings[5], NUM_LEDS6);
    FastLED.addLeds<WS2812, DATA_PIN7, GRB>(LEDstrings[6], NUM_LEDS7);
    FastLED.addLeds<WS2812, DATA_PIN8, GRB>(LEDstrings[7], NUM_LEDS8);

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
    html += "<script src='https://cdn.jsdelivr.net/npm/@jaames/iro@5'></script>";
    html += "<script>";
    html += "var colorPicker = new iro.ColorPicker('#wegoText', { width: 320, color: '#f00' });";
    html += "setInterval(function() {";
    html += "var color = colorPicker.color.hexString.substring(1);";
    html += "var xhr = new XMLHttpRequest();";
    html += "xhr.open('GET', '/setcolor?color=' + color, true);";
    html += "xhr.send();";
    html += "}, 500);"; // 每0.5秒更新一次顏色
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

void playh(CRGB playcolor)
{
    for (int i = 0; i < USEDPIN_NUM; i++) {
        if (lednums[i] > 0) { // 檢查 lednums[i] 是否大於 0
            for (int j = 0; j < lednums[i]; j++) {
                LEDstrings[i][j] = playcolor;
            }
        }
    }
    FastLED.show();
}