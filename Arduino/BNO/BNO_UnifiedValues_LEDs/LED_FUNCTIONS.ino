void distCounterLED() {
  illumNoCounter();

  //Serial.println(illumNoRound);

  if ((illumNoRound > 0) && (illumNoRound <= 16)) {
    for (int i = 0; i < illumNoRound; i++) {
      ring1.setPixelColor(i, red, green, blue);
      ring1.show();
    }
    if ((illumNoRound > 0) && (illumNoRound <= 4)) {
      red = 255;
      green = 0;
      blue = 0;
    }
    else if ((illumNoRound > 4) && (illumNoRound <= 8)) {
      red = 255;
      green = 128;
      blue = 0;
    }
    else if ((illumNoRound > 8) && (illumNoRound <= 12)) {
      red = 255;
      green = 255;
      blue = 0;
    }
    else if ((illumNoRound > 12) && (illumNoRound < 16)) {
      red = 128;
      green = 255;
      blue = 0;
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
  illumNo = (totalDistance / 0.1);
  illumNoRound = illumNo;
  illumNoRound = illumNoRound % 17;
}
