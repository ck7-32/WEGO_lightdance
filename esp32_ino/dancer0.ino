
#include <Arduino.h>
#include <FastLED.h>
#include <WiFi.h>

#define NUM_LEDS1 5 //貓耳帽子
#define NUM_LEDS2 2 //左手套
#define NUM_LEDS3 2 //右手套
#define NUM_LEDS4 16 //外套
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
#define COLOR_COUNT 9
            
#define DANCERN 0 //第幾個舞者

int lednums[]={NUM_LEDS1, NUM_LEDS2, NUM_LEDS3, NUM_LEDS4, NUM_LEDS5, NUM_LEDS6, NUM_LEDS7, NUM_LEDS8};
int pins[]={DATA_PIN1, DATA_PIN2, DATA_PIN3, DATA_PIN4, DATA_PIN5, DATA_PIN6, DATA_PIN7, DATA_PIN8};
char colors[][20]={"#000000", "#ffffff", "#0213ff", "#20fff0", "#ffdf2a", "#ff1100", "#f5ff85", "#13cc06", "#c003ff"};

CRGB LED1[NUM_LEDS1]; 
CRGB LED2[NUM_LEDS2];
CRGB LED3[NUM_LEDS3];
CRGB LED4[NUM_LEDS4];
CRGB LED5[NUM_LEDS5];
CRGB LED6[NUM_LEDS6];
CRGB LED7[NUM_LEDS7];
CRGB LED8[NUM_LEDS8];
CRGB* LEDstrings[] = {LED1, LED2, LED3, LED4, LED5, LED6, LED7, LED8};

int LEDPART1[NUM_LEDS1]={1, 1, 1, 1, 0};//貓耳帽子
int LEDPART2[NUM_LEDS2]={7, 7};//左手套
int LEDPART3[NUM_LEDS3]={8, 8};//右手套
int LEDPART4[NUM_LEDS4]={3, 3, 3, 3, 3, 3, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5};//外套
int LEDPART5[NUM_LEDS5]={11, 11, 11};//左鞋子
int LEDPART6[NUM_LEDS6]={12, 12, 12};//右鞋子
int LEDPART7[NUM_LEDS7]={10, 10, 9, 9};//褲子
int LEDPART8[NUM_LEDS8]={};//

int* leds[] = {LEDPART1, LEDPART2, LEDPART3, LEDPART4, LEDPART5, LEDPART6, LEDPART7, LEDPART8};
int data[46][13] = {{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {8, 8, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 2, 0, 2, 0, 3, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {3, 3, 5, 3, 3, 3, 3, 5, 5, 4, 4, 3, 3}, {8, 8, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {3, 3, 5, 3, 3, 3, 3, 5, 5, 4, 4, 3, 3}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {3, 3, 5, 3, 3, 3, 3, 5, 5, 4, 4, 3, 3}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {3, 3, 5, 3, 3, 3, 3, 5, 5, 4, 4, 3, 3}, {3, 3, 5, 3, 3, 3, 3, 5, 5, 4, 4, 3, 3}, {3, 3, 5, 3, 3, 3, 3, 5, 5, 4, 4, 3, 3}, {3, 3, 5, 3, 3, 3, 3, 5, 5, 4, 4, 3, 3}, {3, 3, 5, 3, 3, 3, 3, 5, 5, 4, 4, 3, 3}, {3, 3, 5, 3, 3, 3, 3, 5, 5, 4, 4, 3, 3}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {3, 3, 5, 3, 3, 3, 3, 5, 5, 4, 4, 3, 3}, {3, 3, 5, 3, 3, 3, 3, 5, 5, 4, 4, 3, 3}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {8, 8, 6, 2, 2, 2, 2, 3, 3, 4, 4, 3, 3}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {3, 3, 5, 3, 3, 3, 3, 5, 5, 4, 4, 3, 3}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}};

const char* ssid = "WEGOlightdance";
const char* password = "Wgld2023wifi";
WiFiUDP udp;
unsigned int localUdpPort = 12345;  
uint8_t incomingPacket[4];

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
    for (y = 0; y < COLOR_COUNT; y++) {
        colorArray[y] = hexToColor(colors[y]);
    }
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

    udp.begin(localUdpPort);
    Serial.printf("Now listening at IP %s, UDP port %d\n", WiFi.localIP().toString().c_str(), localUdpPort);
}

void loop()
{
    int packetSize = udp.parsePacket();
    if (packetSize) {
        int len = udp.read(incomingPacket, 4);
        if (len == 4) {
            int receivedNumber = (incomingPacket[0] << 24) | (incomingPacket[1] << 16) | (incomingPacket[2] << 8) | incomingPacket[3];
            Serial.printf("%d\n", receivedNumber);
            playh(receivedNumber);
        }
    }
}

int playh(int frameN)
{
    for (int ledstring = 0; ledstring < USEDPIN_NUM; ledstring++) {
        CRGB* currentString = LEDstrings[ledstring];
        int* currentParts = leds[ledstring];
        int numLeds = lednums[ledstring];
        bool isGlove = (ledstring == 1 || ledstring == 2);

        for (int led = 0; led < numLeds; led++) {
            int currentpart = currentParts[led];
            CRGB color = colorArray[data[frameN][currentpart]];
            currentString[led] = color;
        }
    }
    FastLED.show();
    return frameN;
}
