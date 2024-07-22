import json
import os

# 讀取 JSON 檔案
def load_json(file_path):
    with open(file_path, 'r', encoding="utf-8") as file:
        return json.load(file)

data = load_json('data.json')
setting = load_json('setting.json')
frames = data.get("frames", [])

# 建立輸出資料夾
output_dir = 'esp32_ino'
os.makedirs(output_dir, exist_ok=True)

def array_to_string(arr):
    return str(arr).replace('[', '{').replace(']', '}').replace("'", '"')

def create_ino_file(code_string, file_name, file_path):
    if not file_name.endswith('.ino'):
        file_name += '.ino'
    full_path = os.path.join(file_path, file_name)
    os.makedirs(file_path, exist_ok=True)
    try:
        with open(full_path, 'w', encoding="utf-8") as file:
            file.write(code_string)
        print(f"檔案已成功創建：{full_path}")
    except IOError as e:
        print(f"創建檔案時發生錯誤：{e}")

def generate_content(dancerN):
    nowdancer = dancerN
    partnames = setting["dancers"][setting["dancersname"][nowdancer]]["parts"]
    LED_stripesetting = setting["dancers"][setting["dancersname"][nowdancer]]["LED"]
    LEDannotation = setting["dancers"][setting["dancersname"][nowdancer]]["LEDannotation"]

    NUM_LEDS = [0] * 8
    LED_stripe = ["{}"] * 8
    stripenames = [""] * 8
    
    for i, stripe in enumerate(LED_stripesetting):
        LED_stripe[i] = array_to_string(stripe)
        NUM_LEDS[i] = len(stripe)
        stripenames[i] = LEDannotation[i]
    colorarray = array_to_string(data["color"])
    

    out = {"frame": [[frames[nowdancer][j][y] for y in range(len(frames[nowdancer][j]))] for j in range(len(frames[nowdancer]))]}
    a, b = len(out["frame"]), len(out["frame"][0])
    out["define"] = f"[{a}][{b}]"
    c = array_to_string(out["frame"])
    framedata = f"int data[{a}][{b}] = {c};"

    stripesetting = "\n".join([
        f"int LEDPART{i+1}[NUM_LEDS{i+1}]={LED_stripe[i]};//{stripenames[i]}"
        for i in range(len(LED_stripe))
    ])

    Settingcode = f"""
#include <Arduino.h>
#include <FastLED.h>
#include <WiFi.h>

#define NUM_LEDS1 {NUM_LEDS[0]} //{stripenames[0]}
#define NUM_LEDS2 {NUM_LEDS[1]} //{stripenames[1]}
#define NUM_LEDS3 {NUM_LEDS[2]} //{stripenames[2]}
#define NUM_LEDS4 {NUM_LEDS[3]} //{stripenames[3]}
#define NUM_LEDS5 {NUM_LEDS[4]} //{stripenames[4]}
#define NUM_LEDS6 {NUM_LEDS[5]} //{stripenames[5]}
#define NUM_LEDS7 {NUM_LEDS[6]} //{stripenames[6]}
#define NUM_LEDS8 {NUM_LEDS[7]} //{stripenames[7]}

#define DATA_PIN1 17
#define DATA_PIN2 16
#define DATA_PIN3 32
#define DATA_PIN4 33
#define DATA_PIN5 25
#define DATA_PIN6 26
#define DATA_PIN7 14
#define DATA_PIN8 27

#define USEDPIN_NUM {len(LED_stripesetting)}
#define COLOR_COUNT {len(data["color"])}
            
#define DANCERN {nowdancer} //第幾個舞者

int lednums[]={{NUM_LEDS1, NUM_LEDS2, NUM_LEDS3, NUM_LEDS4, NUM_LEDS5, NUM_LEDS6, NUM_LEDS7, NUM_LEDS8}};
int pins[]={{DATA_PIN1, DATA_PIN2, DATA_PIN3, DATA_PIN4, DATA_PIN5, DATA_PIN6, DATA_PIN7, DATA_PIN8}};
char colors[][20]={colorarray};

CRGB LED1[NUM_LEDS1]; 
CRGB LED2[NUM_LEDS2];
CRGB LED3[NUM_LEDS3];
CRGB LED4[NUM_LEDS4];
CRGB LED5[NUM_LEDS5];
CRGB LED6[NUM_LEDS6];
CRGB LED7[NUM_LEDS7];
CRGB LED8[NUM_LEDS8];
CRGB* LEDstrings[] = {{LED1, LED2, LED3, LED4, LED5, LED6, LED7, LED8}};

{stripesetting}

int* leds[] = {{LEDPART1, LEDPART2, LEDPART3, LEDPART4, LEDPART5, LEDPART6, LEDPART7, LEDPART8}};
{framedata}

const char* ssid = "Wong88";
const char* password = "20070415";
WiFiUDP udp;
unsigned int localUdpPort = 12345;  
uint8_t incomingPacket[4];

int y = 0;

CRGB hexToColor(const char* hexCode) {{
    long number = (long) strtol(hexCode + 1, NULL, 16);
    byte r = number >> 16;
    byte g = number >> 8 & 0xFF;
    byte b = number & 0xFF;
    return CRGB(r, g, b);
}}

CRGB colorArray[COLOR_COUNT];
"""

    maincode = r"""
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

            if (isGlove) {
                color.nscale8_video(4);  // 使用更快的nscale8_video
            }

            currentString[led] = color;
        }
    }
    FastLED.show();
    return frameN;
}
"""
    return Settingcode + maincode

def main():
    for i in range(len(setting["dancersname"])):
        code = generate_content(i)
        create_ino_file(code, f"dancer{i}", output_dir)

main()
