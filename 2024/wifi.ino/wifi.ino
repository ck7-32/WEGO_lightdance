#include "WiFi.h"
#include <WebServer.h>

const char* ssid ="WEGOlightdance";       // 雙引號內，修改為你要 ESP32 連上的 WiFi 網路名稱 SSID
const char* password = "Wgld2023wifi";   // 雙引號內，鍵入此網路的密碼

WebServer server(80);  //設定網路伺服器 port number 為 80

// Variable to store the HTTP request
String header;

String output26State = "off";  //設定字串變數 output26State，顯示 GPIO26 狀態。如果您要增加可控制的 GPIO 數目，請在這裡增加
String output27State = "off";

// Assign output variables to GPIO pins
const int output26 = 22;
const int output27 = 23;


void start(){
    digitalWrite(output26, HIGH);
    server.send(200,"text/html","啟動");
    delay(1000);
}
void test(){
    digitalWrite(output27, HIGH);
    server.send(201,"text/html","測試");
    delay(1000);
    digitalWrite(output27, LOW);
}
void setup(){     
     Serial.begin(115200);     
     pinMode(output26, OUTPUT);
  pinMode(output27, OUTPUT);
  // Set outputs to LOW
  digitalWrite(output26, LOW);
  digitalWrite(output27, HIGH);

  Serial.println("Connecting to ");  // 連上你所指定的Wi-Fi，並在序列埠螢幕中，印出 ESP32 web server 的 IP address
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  // Print local IP address and start web server
  digitalWrite(output27, LOW);
  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  //伺服器啟動
  server.on("/start",start);
  server.on("/test",test);
  server.begin();
}

void loop(){
    server.handleClient();
}