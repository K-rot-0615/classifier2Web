#include <ESP8266WiFi.h>
#include <WiFiUDP.h>

const char* ssid = "koblab-1";
const char* password = "koblabfms1116";

WiFiUDP Udp;
unsigned int localUdpPort = 8888;
char incomingPacket[255];
char* low = "LOOW";
char* high = "HIGH";
char replyPacket[] = "Hi there! Got the message : -)";


void setup(){

  pinMode(4, OUTPUT);

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
  //Serial.printf("Received %d bytes from %s, port %d\n", packetSize, Udp.remoteIP().toString().c_str(), Udp.remotePort());
  Udp.read(incomingPacket, 255);

<<<<<<< HEAD
  Serial.println(incomingPacket);
=======
  //Serial.println(incomingPacket);
>>>>>>> origin/master

  if(strcmp(incomingPacket, low) == 0){
     //digitalWrite(4, LOW);
     Serial.println("LOW!!!!!!!");
<<<<<<< HEAD
  }
  
  if(strcmp(incomingPacket, high) == 0){
     //digitalWrite(4, HIGH);
     Serial.println("HIGH!!!!!!");
  }
  /*
  else{
    Serial.printf("nanimonaiyo!");
  }
  */
=======
  }
  
  if(strcmp(incomingPacket, high) == 0){
     //digitalWrite(4, HIGH);
     Serial.println("HIGH!!!!!!");
  }
>>>>>>> origin/master

  Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
  Udp.write(replyPacket);
  Udp.endPacket();
 }
}
