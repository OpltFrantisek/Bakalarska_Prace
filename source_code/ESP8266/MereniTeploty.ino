#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Adafruit_Sensor.h>
#include <OneWire.h>
#include <DallasTemperature.h>
/*
  ssid a heslo k wifi
*/
const char* ssid = "....";
const char* password = ".....";
/*
  Nastaveni pro pripojeni k mqtt brokeru
*/
const char* mqtt_server = "192.168.1.110";


WiFiClient espClient;
PubSubClient client(espClient);

long lastMsg = 0;
char msg[50];
int value = 0;
float value2 = 0;

DHT_Unified dht(DHTPIN, DHTTYPE);
/*
 Teplota
*/
// nastavení čísla vstupního pinu
const int pinCidlaDS = 4;
OneWire oneWireDS(pinCidlaDS);
// vytvoření instance senzoryDS z knihovny DallasTemperature
DallasTemperature senzoryDS(&oneWireDS);
void setup_wifi() {

  delay(10);
  // Připojeni k wifi
  Serial.println();
  Serial.print("Pripojuji se k:  ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("Wifi pripojeno");
  Serial.println("IP adresa: ");
  Serial.println(WiFi.localIP());
}
/*
  Medota k pripojeni k MQTT brokeru
*/
void reconnect() {
  // Opakuj dokud nejsme pripojeni
  while (!client.connected()) {
    Serial.print("Pokus o navazani MQTT pripojeni...");
    // Pokus o pripojeni
    if (client.connect("ESP8266Client")) {
      Serial.println("connected");  
    } else {

      Serial.print("Chyba, rc=");
      Serial.print(client.state());
      Serial.println(" zksusim to znovu za 5s");
      // pocka 5s
      delay(5000);
    }
  }
}
float Teplota(){
  senzoryDS.requestTemperatures();
  // výpis teploty na sériovou linku, při připojení více čidel
  // na jeden pin můžeme postupně načíst všechny teploty
  // pomocí změny čísla v závorce (0) - pořadí dle unikátní adresy čidel
  float teplota = senzoryDS.getTempCByIndex(0);
  Serial.print("Teplota cidla DS18B20: ");
  Serial.print(teplota);
  Serial.println(" stupnu Celsia");
  return teplota;
}

void PosliZpravu(){
    /*
      Pokud nejsem pripojen tak se pripojim
     */
	 if (!client.connected()) {
          reconnect();
      }
	  value2 = Teplota();            
      snprintf (msg, 75, "Teplota: %g ", value2);
      Serial.print("Posilam zpravu: ");
      String s = String(value2,2);
      s = "Teplota: "+s;
      Serial.println(s);
      s.toCharArray(msg, 75,0);
      client.publish("zprava",msg ); 
}

void setup() {
  Serial.begin(9600);
  senzoryDS.begin();
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  PosliZpravu();
  
  Serial.println("Usinam na 30 minut");
  ESP.deepSleep(18e8); 
}

void loop() {

}
