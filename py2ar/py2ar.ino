#include <ESP8266WiFi.h>
#include <WiFiUDP.h>

const char* ssid = "hogehoge";
const char* password = "hogehoge";

WiFiUDP Udp;
unsigned int localUdpPort = 8888;
char incomingPacket[255];
char replyPacket[] = "Hi there! Got the message : -)";


void setup(){

  pinMode(16, OUTPUT);
  digitalWrite(16, LOW);

  Serial.begin(115200);
  Serial.println();

  Serial.printf("connecting to %s ", ssid);
  WiFi.begin(ssid, password);

  while(WiFi.status() != WL_CONNECTED){
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  //Serial.println(" connected");

  Udp.begin(localUdpPort);
  //Serial.printf("Now listening at IP %s, UDP port %d\n", WiFi.localIP().toString().c_str(), localUdpPort);
  Serial.print("Connected, IP address: ");
  Serial.println(WiFi.localIP());
}

void loop(){
 int packetSize = Udp.parsePacket();
 if(packetSize){
  Serial.printf("Received %d bytes from %s, port %d\n", packetSize, Udp.remoteIP().toString().c_str(), Udp.remotePort());
  int len = Udp.read(incomingPacket, 255);
  if(len > 0){
    incomingPacket[len] = 0;
  }
  Serial.printf("UDP packet contents: %s\n", incomingPacket);

  if(replyPacket != ""){
    digitalWrite(16, HIGH);
    analogWrite(9, 255);
  }
  Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
  Udp.write(replyPacket);
  Udp.endPacket();
 }
}
