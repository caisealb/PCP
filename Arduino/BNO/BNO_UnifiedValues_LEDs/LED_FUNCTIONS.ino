void distCounterLED() {
  illumNoCounter();

  //Serial.println(illumNoRound);

  if ((illumNoRound > 0) && (illumNoRound <= 16)) {
    red = 255;
    blue = 255;
    green = 0;
    for (int i = 0; i < illumNoRound; i++) {
      ring1.setPixelColor(i, red, green, blue);
      ring1.show();
    }
  }

  else {
    for (int i = 0; i < ring1.numPixels(); i++) {
      ring1.setPixelColor(i, 0, 0, 0);
      ring1.show();
    }
  }
}

void illumNoCounter() {
  illumNo = (totalDistance / 10);
  illumNoRound = illumNo;
  illumNoRound = illumNoRound % 16;
}
