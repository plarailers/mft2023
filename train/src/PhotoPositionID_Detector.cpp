#include "PhotoPositionID_Detector.h"

PhotoPositionID_Detector::PhotoPositionID_Detector() 
: 	SENSOR1_PIN(34),
	SENSOR2_PIN(35),
	WHITE_THRESHOLD1(1100),
	WHITE_THRESHOLD2(1750),
	LEAVE_THRESHOLD(3950),
	TIME_OUT(250)
{
	this->positionID = 0;
	this->sensorValue1 = 0;
	this->sensorValue2 = 0;
	this->detectedColor1 = black;
	this->detectedColor2 = black;
	this->preDetectedColor1 = black;
	this->preDetectedColor2 = black;
	this->bitIndex1 = 0;
	this->bitIndex2 = 0;
	this->bitDetectedTime1 = 0;
	this->bitDetectedTime2 = 0;
	this->nowTime = 0;
}

void PhotoPositionID_Detector::photoRefSetup() {
	memset(gotData1, '\0', BIT);
	memset(gotData2, '\0', BIT);
	resetAll();
}

void PhotoPositionID_Detector::setPhotoRefAnalogValue(int sensorValue1, int sensorValue2) {
	this->sensorValue1 = sensorValue1;
	this->sensorValue2 = sensorValue2;
}

int PhotoPositionID_Detector::getPhotoPositionID() {
	nowTime = millis();

	positionID = 0;

	if(sensorValue1 < WHITE_THRESHOLD1){detectedColor1 = white;}
	else{detectedColor1 = black;}

	if(sensorValue2 < WHITE_THRESHOLD2){detectedColor2 = white;}
	else{detectedColor2 = black;}

	measure1Clock2();
	measure2Clock1();

	preDetectedColor1 = detectedColor1;
	preDetectedColor2 = detectedColor2;

	if (positionID > 0) {
		Serial.print("PositionID: ");
		Serial.println(positionID);
	}

	// Serial.print("Val1:");
	// Serial.print(sensorValue1);
	// Serial.print(", Val2:");
	// Serial.print(sensorValue2);
	// Serial.print(", Color1:");
	// Serial.print(detectedColor1*1000);
	// Serial.print(", Color2:");
	// Serial.print(detectedColor2*1000);

	// Serial.print(", TOP:");
	// Serial.print("4096");
	// Serial.print(", BOTTOM:");
	// Serial.print("0");

	// Serial.println("");

    return positionID;
}

void PhotoPositionID_Detector::reset1(){
	bitIndex1 = 0;
	for(int j = 0; j < BIT; j++){
		gotData1[j] = 0;
	}	
}

void PhotoPositionID_Detector::reset2(){
	bitIndex2 = 0;
	for(int j = 0; j < BIT; j++){
		gotData2[j] = 0;
	}
}

void PhotoPositionID_Detector::resetAll(){
	reset1();
	reset2();
}

void PhotoPositionID_Detector::measure1Clock2(){
	if(detectedColor2 != preDetectedColor2){
		gotData1[bitIndex1] = detectedColor1;
		bitIndex1 += 1;
		bitDetectedTime1 = millis();
	}

	if(bitIndex1 >= BIT){
		positionID = 0;
		for(int j = 0; j < BIT; j++){
			positionID += gotData1[BIT - j - 1] * (pow(2, BIT - j - 1) + 0.5);
		}
		resetAll();
	}

	if(sensorValue1 > LEAVE_THRESHOLD) resetAll();
	if(nowTime - bitDetectedTime1 > TIME_OUT) reset1();
}

void PhotoPositionID_Detector::measure2Clock1(){
	if(detectedColor1 != preDetectedColor1){
		gotData2[bitIndex2] = detectedColor2;
		bitIndex2 += 1;
		bitDetectedTime2 = millis();
	}

	if(bitIndex2 >= BIT){
		positionID = 0;
		for(int j = 0; j < BIT; j++){
			positionID += gotData2[j] * (pow(2,j) + 0.5);
		}
		resetAll();
	}

	if(sensorValue2 > LEAVE_THRESHOLD) resetAll();
	if(nowTime - bitDetectedTime2 > TIME_OUT) reset2();
}