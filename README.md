This is a talking Bender head from Futurama. Controlled from a microcontroller and CircuitPython the head talks and has LEDs that show random patterns when talking and idle. The basic features are:

* Plays random audio files at random intervals
* 20 programmable LEDs (NeoPixels)
* Antenna is a motion detector that can trigger audio
* Antenna is also a button to toggle modes .. (regular, motion detector off, audio off)

The idea and original 3D printer .STL files came from another project (https://www.thingiverse.com/thing:4384974). I've made some various changes to the some models to support the antenna to act as a motion detector.

## Parts List
* Adafruit Feather RP2040 (https://www.adafruit.com/product/4884)
 * Which microcontroller you use is flexible as long as it can support the inputs, outputs, and the CircuitPython modules you need, mainly audiobusio and optionally audiomp3. You also need some storage space for audio files. The Adafruit RP2040 boards have 8MB of flash for storing audio files. Adafruit has support for MP3 audio on their RP2040 boards to help with the storage limits. 
* Adafruit I2S Audio Amp (https://www.adafruit.com/product/3006)
* Adafruit Mini NeoPixels (https://www.adafruit.com/product/2959)
  * You will only need 20 NeoPixels but you need ones with 0.66"/17mm spacing between LEDs for align properly with the teeth.
  * I went with the "Mini" NeoPixels due to the lower power requirement and to be sure I can just power everything through the Feather. They are bright enough if you have pretty clear PLA for the teeth and eyes. Regular sized NeoPixels might work but have not been tested.
* AdaFruit Mini PIR Motion Sensor (https://www.adafruit.com/product/4871) 
* Speaker
  * You need a square 50mm (2 inch) 4-8ohm speaker. There's only about 52mm clearance for mounting.
* PLA / Printing
  * You will need some clear/transparent/translucent PLA or other filliment for printing the teeth and eyes so the LEDs can light them up. How you print and/or paint the rest is up to you.  
