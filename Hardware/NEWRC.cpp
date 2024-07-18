#include <Wire.h>  // 需要使用Wire庫來與OLED通信
#include <Adafruit_GFX.h>  // Adafruit的圖形庫
#include <Adafruit_SSD1306.h>  // Adafruit的SSD1306 OLED庫
#include <WiFi.h>
#include <WiFiUdp.h>

const char* ssid = "LightDanceServer";
const char* pwd = "56781234";

// WiFiServer server(8888);  // 宣告伺服器物件，並設定 port 為 8088 
WiFiUDP udp; // 宣告UDP物件

IPAddress local_IP(192, 168, 111, 222);  
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 255, 0);

#define SCREEN_WIDTH 128 
#define SCREEN_HEIGHT 64  
#define OLED_ADDR 0x3C
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

unsigned long lastTime = 0;
unsigned long OLEDUPDATE = 2000;
int screen = 0;

void setup() {
// 初始化按鈕按鈕
pinMode(4, INPUT);
// OLED初始化
  Wire.begin();
  if (!display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR)) {
    Serial.println(F("SSD1306 initialization failed"));
    for(;;); 
  }

  display.clearDisplay();
  display.setTextSize(3);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.println(F("LIGHT\n  DANCE"));
  display.display();
  delay(1000);

    
    //wifi初始化 // 開始UDP通信
    Serial.begin(115200);
    WiFi.mode(WIFI_AP);
    WiFi.softAPConfig(local_IP,gateway,subnet);
    WiFi.softAP(ssid, pwd);
    delay(100);
    IPAddress IP = WiFi.softAPIP();
    Serial.print("AP IP address: ");
    Serial.println(IP);

}

unsigned long FrameStart = 0;
unsigned long FrameNow = 0;
unsigned long FramePass = 0;
bool ShowStart = false;
bool ConnectReady = false;


void loop()
{
    if(ShowStart == false)
    {
        if(millis() - lastTime > OLEDUPDATE)
        {
            lastTime = millis();
            int numDevices = WiFi.softAPgetStationNum();
            //ready to show
            if (numDevices >= 2)
            {
                ConnectReady = true;
                display.clearDisplay();
                display.setTextSize(3);
                display.setCursor(0, 0);
                display.println("Show\n  Ready");
                display.display();
            }
            //not ready
            else
            {
                ConnectReady = false;
                display.clearDisplay();
                display.setTextSize(3);
                display.setCursor(0, 0);
                display.println("Device CT\n  " + String(numDevices));
                display.display();
            }
        }

        // 按下左鍵開始表演
        if(digitalRead(4) == HIGH and ConnectReady == true)
        {
            ShowStart = true;
            display.clearDisplay();
            display.setTextSize(3);
            display.setCursor(0, 0);
            display.println("Show\n  Start");
            display.display();
            delay(2000);
            FrameStart = millis(); // 最新frame開始時間
        }
        
    }

    else if (ShowStart == true)
    {
        FrameNow = millis(); // 最新frame開始時間
        FramePass = FrameNow - FrameStart;
        if ((FramePass > FrameTime[Frame]) && (Frame < FrameNum))
        {
            FrameUpdate(Frame);
            udp.beginPacket(udp.remoteIP(), udp.remotePort());
            udp.write(Frame);
            udp.endPacket();
            delay(10);
            Frame++;
        }
        if (Frame == FrameNum)
        {
            ShowStart = false;  // 表演結束
            //OLED show start
            display.clearDisplay();
            display.setTextSize(3);
            display.setCursor(0, 0);
            display.println("Show\n  Over");
            display.display();
            delay(2000);            
        }
    }   
}