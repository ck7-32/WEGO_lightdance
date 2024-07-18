#include <Wire.h>  // 需要使用Wire庫來與OLED通信
#include <Adafruit_GFX.h>  // Adafruit的圖形庫
#include <Adafruit_SSD1306.h>  // Adafruit的SSD1306 OLED庫
#include <WiFi.h>
#include <WiFiUdp.h>

const char* ssid = "LightDanceServer";
const char* pwd = "56781234";

WiFiServer server(8088);  // 宣告伺服器物件，並設定 port

WiFiUDP udp;

#define SCREEN_WIDTH 128  // OLED顯示器的寬度，以像素為單位
#define SCREEN_HEIGHT 64  // OLED顯示器的高度，以像素為單位

// 定義OLED顯示器的I2C位址，這裡假設是0x3C，具體位址可能因你的OLED模組而異
#define OLED_ADDR 0x3C

// 宣告一個Adafruit_SSD1306類型的物件
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

unsigned long lastTime = 0;
unsigned long OLEDUPDATE = 2000;
int screen = 0;

float FrameTime[] = {0, 636.379, 863.657, 1136.3909999999998, 1463.672, 1727.3149999999998, 2177.9480000000003, 2477.054, 2642.191, 2798.1530000000002, 2985.7909999999997, 3126.63, 3337.889, 3492.812, 3606.1890000000003, 3761.628, 3994.7870000000003, 4250.806, 4530.112, 4736.652999999999, 4957.3, 5177.622, 5383.231000000001, 5598.187, 5859.872, 6116.485, 6736.53, 7586.048, 8489.164, 8525.66, 8584.054999999998, 8635.151, 8686.247, 8737.342, 8781.138, 9219.099999999999, 11540.285000000002, 12441.545, 12622.021999999999, 13756.173999999999, 15125.441, 15622.416, 16085.456, 16556.98, 17050.362, 17107.155, 17188.788, 17265.318, 17346.951, 17443.89, 17515.319000000003, 17592.718999999997, 18645.461, 18760.464, 18855.467, 18955.469, 19060.472, 19155.474000000002, 19315.478, 19780.488999999998, 19839.035, 19892.606, 19958.081, 20023.557, 20069.659, 20069.659, 20677.377, 20745.172, 20821.441, 20880.762000000002, 20963.927000000003, 21039.193, 21125.211, 21211.229, 22570.896, 24945.187, 25138.727, 25349.25};
int FrameNum = size(FrameTime);
int Frame = 0;

void setup() {

  // 初始化Wire庫，開始I2C通信
  Wire.begin();

  // 初始化OLED顯示器，請確保顯示器的I2C位址正確
  if (!display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR)) {
    Serial.println(F("SSD1306 initialization failed"));
    for(;;);  // 如果初始化失敗，停止執行
  }

  // 清空顯示器內容
  display.clearDisplay();

  // 設置顯示器文字大小
  display.setTextSize(3);
  // 設置顯示器文字顏色，白色
  display.setTextColor(SSD1306_WHITE);

  // 在顯示器上顯示文字
  display.setCursor(0, 0);
  display.println(F("LIGHT\n  DANCE"));
  display.display();  // 更新顯示器內容
  delay(1000);

    // 初始化按鈕
    //按鈕左邊 GPIO 4 (預設pull down)
    pinMode(4, INPUT_PULLDOWN);
    //按鈕右邊 GPIO 27 (預設pull down)
    pinMode(27, INPUT_PULLDOWN);

    Serial.begin(115200);

    // 连接WiFi
    WiFi.mode(WIFI_AP);
    WiFi.softAP(ssid, pwd); // 设置ESP32作为AP，SSID为ESP32-AP，密码为password
    delay(100);

    // 获取本地IP地址并打印
    IPAddress IP = WiFi.softAPIP();
    Serial.print("AP IP address: ");
    Serial.println(IP);

    // 启动UDP服务器
    udp.begin(8088);

    //顯示今天表演的frame
    display.clearDisplay();
    display.setTextSize(2);
    display.setCursor(0, 0);
    display.println("ShowFrame");
    display.setCursor(72, 50);
    display.println(FrameNum);
    display.display();
    delay(2000);

    
}

unsigned long FrameStart = 0;
String rstatus = "";
bool D1connect = false;
bool D2connect = false;
bool D3connect = false;
bool AUconnect = false;
bool D1Over= false;
bool D2Over = false;
bool D3Over = false;
bool AUOver = false;
bool ShowStart = false;
bool ButtonL = false;
bool ButtonR = false;

void FrameUpdate(int F) // 更新frame UDP broadcast
{
    udp.beginPacket(udp.remoteIP(), udp.remotePort());
    udp.write(F);
    udp.endPacket();
    Serial.println("Frame Update"+String(F)); // send frame
}

void loop() {

    if(ShowStart == true)
    {
        FrameStart = millis(); // 最新frame開始時間
        if (ButtonR == true)
        {
            ShowStart = false;  // 按下右鍵結束表演
            ButtonR = false;
            //OLED show start
            FrameUpdate(0);
            display.clearDisplay();
            display.setTextSize(2);
            display.setCursor(0, 0);
            display.println("Show Stop");
            display.display();
            delay(1000);
        }
        if (Frame == FrameNum-1)
        {
            FrameUpdate(Frame);
            ShowStart = false;  // 表演結束
            //OLED show start
            display.clearDisplay();
            display.setTextSize(2);
            display.setCursor(0, 0);
            display.println("Show Over");
            display.display();
            delay(1000);
        }
        else{
        if (FrameStart > FrameTime[Frame])
        {
            FrameUpdate(Frame);
            Frame++;
        }
        }
    }
    else if(ShowStart == false)
    {
        FrameStart = 0;
        Frame = 0;
        if (ButtonL == true)
        {
            ShowStart = true;  // 按下左鍵開始表演
            ButtonL = false;
            //OLED show start
            display.clearDisplay();
            display.setTextSize(2);
            display.setCursor(0, 0);
            display.println("Show Start");
            display.display();
            delay(1000);

        }

    }

    //按鈕操作
    if (digitalRead(4) == HIGH)
    {
        ButtonL = true;
    }
    else if (digitalRead(27) == HIGH)
    {
        ButtonR = true;
    }
    

    // UDP 數據包處理(傳送frame/接收狀態)
    int packetSize = udp.parsePacket();
        if (packetSize) {
        Serial.print("Received packet of size ");
        Serial.println(packetSize);

        // 读取数据包内容
        char packetBuffer[255]; // buffer to hold incoming packet,
        udp.read(packetBuffer, 255);

        // 打印接收到的内容
        Serial.print("Contents:");
        Serial.println(packetBuffer);
        
        // 將接收到的內容轉換為字串
        rstatus = String(packetBuffer);
        Serial.println(rstatus);
                        }


    //連接最新狀態確認
    if (rstatus == "D1D1")
    {
        D1connect = true;
        rstatus = "";
    }
    else if (rstatus == "D2D2")
    {
        D2connect = true;
        rstatus = "";
    }
    else if (rstatus == "D3D3")
    {
        D3connect = true;
        rstatus = "";
    }
    else if (rstatus == "AUAU")
    {
        AUconnect = true;
        rstatus = "";
    }

    //表演結束狀態
    else if (rstatus == "D1OV")
    {
        D1connect = false;
        D1Over = true;
        rstatus = "";
    }
    else if (rstatus == "D2OV")
    {
        D2connect = false;
        D2Over = true;
        rstatus = "";
    }
    else if (rstatus == "D3OV")
    {
        D3connect = false;
        D3Over = true;
        rstatus = "";
    }
    else if (rstatus == "AUOV")
    {
        AUconnect = false;
        AUOver = true;
        rstatus = "";
    }

    //更新OLED
    if (millis() - lastTime > OLEDUPDATE)
    {
        if(screen == 0)
        {

            lastTime = millis();
            display.clearDisplay();
            display.setTextSize(2);
            display.setCursor(0, 0);
            display.println("D1");
            display.setCursor(31, 0);
            display.println("D2");
            display.setCursor(63, 0);
            display.println("D3");
            display.setCursor(95, 0);
            display.println("AU");
            display.setTextSize(2);
            display.setCursor(0, 40);
            if (D1Over)
            {
                display.println("-");
            }
            else
            {
                if (D1connect)
                {
                    display.println("O");
                }
                else
                {
                    display.println("X");
                }
            }
            
            display.setCursor(31, 40);
            if (D2Over)
            {
                display.println("-");
            }
            else
            {
                if (D2connect)
                {
                    display.println("O");
                }
                else
                {
                    display.println("X");
                }
            }

            display.setCursor(63, 40);
            if (D3Over)
            {
                display.println("-");
            }
            else
            {
                if (D3connect)
                {
                    display.println("O");
                }
                else
                {
                    display.println("X");
                }
            }

            display.setCursor(95, 40);
            if (AUOver)
            {
                display.println("-");
            }
            else
            {
                if (AUconnect)
                {
                    display.println("O");
                }
                else
                {
                    display.println("X");
                }
            }

            display.display();

            screen = 1;

        }

        else if(screen == 1)
        {

            lastTime = millis();
            display.clearDisplay();
            display.setTextSize(2);
            display.setCursor(0, 0);
            display.println("CurrFrame");
            display.setCursor(72, 50);
            display.println(Frame);
            display.display();

            screen = 0;

        }   

    }

}

