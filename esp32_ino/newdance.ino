#include <Arduino.h>
#include <SPIFFS.h>
#include <WiFi.h>
#include <ESPAsyncWebServer.h>
#include <FastLED.h>
#include <ArduinoJson.h>

// ================== 网络配置 ==================
const char* ssid = "你的WiFi名稱";
const char* password = "你的WiFi密碼";
AsyncWebServer server(80);
WiFiUDP udp;
unsigned int localUdpPort = 12345;
uint8_t incomingPacket[4];

// ================== LED配置 ==================
// 引脚和LED数量配置
#define NUM_LEDS1 7   // 猫耳帽子
#define NUM_LEDS2 2   // 左手套
#define NUM_LEDS3 2   // 右手套
#define NUM_LEDS4 15  // 外套
#define NUM_LEDS5 3   // 左鞋子
#define NUM_LEDS6 3   // 右鞋子
#define NUM_LEDS7 4   // 裤子
#define DATA_PIN1 17
#define DATA_PIN2 16
#define DATA_PIN3 32
#define DATA_PIN4 33
#define DATA_PIN5 25
#define DATA_PIN6 26
#define DATA_PIN7 14

CRGB LED1[NUM_LEDS1];
CRGB LED2[NUM_LEDS2];
CRGB LED3[NUM_LEDS3];
CRGB LED4[NUM_LEDS4];
CRGB LED5[NUM_LEDS5];
CRGB LED6[NUM_LEDS6];
CRGB LED7[NUM_LEDS7];
CRGB* LEDstrings[] = {LED1, LED2, LED3, LED4, LED5, LED6, LED7};

// LED部件映射
int LEDPART1[NUM_LEDS1] = {2, 2, 1, 1, 0, 1, 1};
int LEDPART2[NUM_LEDS2] = {7, 7};
int LEDPART3[NUM_LEDS3] = {8, 8};
int LEDPART4[NUM_LEDS4] = {3, 3, 3, 5, 5, 3, 3, 4, 6, 6, 4, 4, 4, 4, 4};
int LEDPART5[NUM_LEDS5] = {11, 11, 11};
int LEDPART6[NUM_LEDS6] = {12, 12, 12};
int LEDPART7[NUM_LEDS7] = {9, 9, 10, 10};
int* leds[] = {LEDPART1, LEDPART2, LEDPART3, LEDPART4, LEDPART5, LEDPART6, LEDPART7};

// 颜色配置
char colors[][20] = {"#000000","#cbcbcb","#0213ff","#20fff0","#d5ce00","#ff1100","#f5ff85","#13cc06","#c003ff","#7baae3","#c276d3","#ffffff"};
CRGB* colorArray;

// ================== 动画数据 ==================
#define MAX_FRAMES 256
#define PARTS_COUNT 13
int** animationData;
bool newConfigLoaded = false;

// ================== 函数声明 ==================
CRGB hexToColor(const char* hexCode);
void loadAnimationData();
void playFrame(int frameN);
void handleFileUpload(AsyncWebServerRequest *request, String filename, size_t index, uint8_t *data, size_t len, bool final);

void setup() {
  Serial.begin(115200);
  
  // 初始化SPIFFS
  if (!SPIFFS.begin(true)) {
    Serial.println("SPIFFS 初始化失败");
    return;
  }

  // 连接WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi 连接成功！");
  Serial.println(WiFi.localIP());

  // 初始化LED
  FastLED.addLeds<WS2812, DATA_PIN1, GRB>(LED1, NUM_LEDS1);
  FastLED.addLeds<WS2812, DATA_PIN2, GRB>(LED2, NUM_LEDS2);
  FastLED.addLeds<WS2812, DATA_PIN3, GRB>(LED3, NUM_LEDS3);
  FastLED.addLeds<WS2812, DATA_PIN4, GRB>(LED4, NUM_LEDS4);
  FastLED.addLeds<WS2812, DATA_PIN5, GRB>(LED5, NUM_LEDS5);
  FastLED.addLeds<WS2812, DATA_PIN6, GRB>(LED6, NUM_LEDS6);
  FastLED.addLeds<WS2812, DATA_PIN7, GRB>(LED7, NUM_LEDS7);

  // 初始化颜色数组和动画数据
  colorArray = nullptr;
  animationData = nullptr;
  loadAnimationData();

  // 初始化Web服务器
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request) {
    request->send(200, "text/plain", "ESP32 LED控制服务器运行中");
  });

  server.on("/upload", HTTP_POST,
    [](AsyncWebServerRequest *request) { request->send(200); },
    handleFileUpload
  );

  server.begin();

  // 初始化UDP
  udp.begin(localUdpPort);
  Serial.printf("UDP监听端口: %d\n", localUdpPort);
}

void loop() {
  // 处理UDP数据
  int packetSize = udp.parsePacket();
  if (packetSize) {
    int len = udp.read(incomingPacket, 4);
    if (len == 4) {
      int frameNumber = (incomingPacket[0] << 24) | (incomingPacket[1] << 16) | (incomingPacket[2] << 8) | incomingPacket[3];
      playFrame(frameNumber);
    }
  }

}

// ================== 功能函数 ==================
CRGB hexToColor(const char* hexCode) {
  long number = strtol(hexCode + 1, NULL, 16);
  return CRGB(number >> 16, number >> 8 & 0xFF, number & 0xFF);
}

void loadAnimationData() {
  File file = SPIFFS.open("/config.json");
  if (!file) {
    Serial.println("无法打开配置文件");
    return;
  }

  DynamicJsonDocument doc(4096);
  DeserializationError error = deserializeJson(doc, file);
  if (error) {
    Serial.println("JSON解析失败");
    return;
  }

  // 动态分配颜色数组
  JsonArray colorsArray = doc["colors"];
  int colorCount = colorsArray.size();
  CRGB* newColorArray = new CRGB[colorCount];
  for (int i = 0; i < colorCount; i++) {
    newColorArray[i] = hexToColor(colorsArray[i]);
  }
  delete[] colorArray;
  colorArray = newColorArray;

  // 动态分配动画数据数组
  JsonArray frames = doc["frames"];
  int frameCount = frames.size();
  int** newAnimationData = new int*[frameCount];
  for (int i = 0; i < frameCount; i++) {
    JsonArray frame = frames[i];
    int partCount = frame.size();
    newAnimationData[i] = new int[partCount];
    for (int j = 0; j < partCount; j++) {
      newAnimationData[i][j] = frame[j];
    }
  }
  for (int i = 0; i < MAX_FRAMES; i++) {
    delete[] animationData[i];
  }
  delete[] animationData;
  animationData = newAnimationData;

  file.close();
  Serial.println("动画数据加载完成");
}

void playFrame(int frameN) {
  frameN = frameN % MAX_FRAMES;
  
  for (int ledGroup = 0; ledGroup < 7; ledGroup++) {
    CRGB* currentLEDs = LEDstrings[ledGroup];
    int* parts = leds[ledGroup];
    int ledCount = (ledGroup == 0) ? NUM_LEDS1 :
                   (ledGroup == 1) ? NUM_LEDS2 :
                   (ledGroup == 2) ? NUM_LEDS3 :
                   (ledGroup == 3) ? NUM_LEDS4 :
                   (ledGroup == 4) ? NUM_LEDS5 :
                   (ledGroup == 5) ? NUM_LEDS6 : NUM_LEDS7;

    for (int i = 0; i < ledCount; i++) {
      int partIndex = parts[i];
      currentLEDs[i] = colorArray[animationData[frameN][partIndex]];
    }
  }
  FastLED.show();
}

void handleFileUpload(AsyncWebServerRequest *request, String filename, size_t index, uint8_t *data, size_t len, bool final) {
  static File uploadFile;
  
  if (!index) {
    Serial.printf("開始上傳: %s\n", filename.c_str());
    SPIFFS.remove("/config.json");
    uploadFile = SPIFFS.open("/config.json", "w");
  }

  if (uploadFile) {
    uploadFile.write(data, len);
  }

  if (final) {
    uploadFile.close();
    Serial.println("文件上傳完成");
    loadAnimationData();  // 直接加載新的動畫數據
  }
}