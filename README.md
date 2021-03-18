This is a talking Bender head from Futurama. Controlled by a microcontroller and CircuitPython the head talks and has LEDs that show random patterns when talking and idle. The basic features are:

* Plays random audio files at random intervals
* 20 programmable LEDs (NeoPixels)
* Antenna is a motion detector that can trigger audio
* Antenna is also a button to toggle modes .. (regular, motion detector off, audio off)

The idea and original 3D printer .STL files came from another project (https://www.thingiverse.com/thing:4384974). I've made some various changes to the some models to support the antenna to act as a motion detector.

## Parts List
* Adafruit Feather RP2040 (https://www.adafruit.com/product/4884)
  * Which microcontroller you use is flexible as long as it can support the inputs, outputs, and the CircuitPython modules you need, mainly audiobusio and optionally audiomp3. This project does not use any analog inputs or outputs. The main concern is storage space for audio files, which is extremely limited on microcontrollers. The Adafruit RP2040 boards have 8MB of flash for storing audio files. Adafruit also has support for MP3 audio on their RP2040 boards to help with the storage limits. 
* Adafruit I2S Audio Amp (https://www.adafruit.com/product/3006)
* Adafruit Mini NeoPixels (https://www.adafruit.com/product/2959)
  * You will only need 20 NeoPixels but you need ones with 0.66"/17mm spacing between LEDs to align properly with the teeth.
  * I went with the "Mini" NeoPixels due to the lower power requirement to be sure I can power everything through the Feather. They are bright enough if you have pretty clear PLA for the teeth and eyes. Regular sized NeoPixels might work but have not been tested.
* Adafruit Mini PIR Motion Sensor (https://www.adafruit.com/product/4871) 
* Speaker
  * You need a square 50mm (2 inch) 4-8ohm speaker. There's only about 52mm clearance for mounting. An 8ohm speaker will use less power and is reccomended.
* Power Supply
  * You need a power supply that can support 20 NeoPixels, the microcontroller, the amp, and a speaker. I used the official Raspberry Pi power supply because it's cheap, small, and can provide 3A. I would think that maybe 1A would be plenty sufficient, but there's lots of variables in play.
  * https://www.adafruit.com/product/4298  
* PLA / Printing
  * You will need some clear/transparent/translucent PLA or other filliment for printing the teeth and eyes so the LEDs can light them up. How you print and/or paint the rest is up to you.

## Audio Files
For copyright reasons no audio files are included. You'll have to find them online and convert them down to a low enough bitrate your microcontroller can support and small enough file sizes for the flash storage limitations . You can use the following guide to convert your files (https://learn.adafruit.com/microcontroller-compatible-audio-file-conversion).

## Config Options
Configurable options include:
* Min/max wait times between playing random audio
* Wait timer between motion activated audio

## Modes
There are 3 modes, controlled by pushing the antenna down (it's also a button). Mode changes are indicated by lighting up 1, 2, or 3 teeth. Push and hold antenna down until teeth show the mode change.
1. Regular mode - audio on, motion detector on
2. Regular mode - audio on, motion detector off
3. Silent mode - audio off









