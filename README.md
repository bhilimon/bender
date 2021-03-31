This is a talking Bender head from Futurama. It's controlled by a Adafruit Feather RP2040 microcontroller and CircuitPython. The main features are:

* He talks! Plays random audio files at random intervals.
* He's colorful! 20 programmable NeoPixel LEDs that play various animations when talking and when idle.
* Antenna is also a motion detector that can trigger audio.
* Antenna is also a button to toggle modes (see below).
* Initial / startup mode (see below).

This project takes quite a bit of time to print, put together, and to gather and properly prep all your audio files. Make sure you read all the documentation about the issues I ran into and limitations before starting this project.

## Config Options
Configurable options include:
* Min/max wait times between playing random audio
* Wait timer after playing audio before re-enabling the motion detector
* Timer on changing eye colors
* Timer on changing teeth LED animations
* A basic config of every animation in the CircuitPython LED animation library is included (https://circuitpython.readthedocs.io/projects/led-animation/en/latest/index.html). You can easily modify them and enable/disable certain animations.

## Modes / Changing Modes
There are 3 modes, controlled by pushing the antenna down (it's also a button). Mode changes are indicated by momentarily lighting up 1, 2, or 3 teeth blue. Note: you can only change the mode while audio is not playing.
1. Audio on, motion detector on
2. Audio on, motion detector off
3. Audio off

## Parts List
* Adafruit Feather RP2040 (https://www.adafruit.com/product/4884)
  * Which microcontroller you use is flexible as long as it can support the inputs, outputs, CircuitPython, and the modules you need, mainly NeoPixels and audiobusio. This project does not use any analog inputs or outputs. The main concern is storage space for audio files, which is extremely limited on microcontrollers. The Adafruit RP2040 boards have 8MB of flash for storing audio files. Adafruit is also working on adding MP3 audio support on their RP2040 boards which will help with the storage limits. If you use a different microcontroller you might have to adjust 3D models for mounting holes and alignment of the USB power cable hole on the back of the head.
* Adafruit I2S Audio Amp (https://www.adafruit.com/product/3006)
  * See the audio notes / issues section below.
* Adafruit Mini NeoPixels (https://www.adafruit.com/product/2959)
  * You will only need 20 NeoPixels but you _need_ ones with 0.66"/17mm spacing between LEDs to align properly with the teeth. You will not be able to mount NeoPixels with wider spacing.
  * I went with the "Mini" NeoPixels due to the lower power requirement to be sure I can power everything through the Feather. Even at 50% brightness they are plenty bright enough if you have pretty clear PLA for the teeth and eyes. Regular sized NeoPixels should work but have not been tested. They might draw too much power.
* Adafruit Mini PIR Motion Sensor (https://www.adafruit.com/product/4871) 
* Speaker
  * You need a square 50mm (2 inch) 4-8ohm speaker. There is only about 52mm clearance for mounting. There are 3D models for both 40mm and 42mm mounting hole spacing since there doesn't seem to be a standard. An 8ohm speaker will use less power and is recommended.
* Power Supply
  * You need a USB-C power supply that can support 20 NeoPixels, the microcontroller, the amp, and a speaker. I don't exactly know how much power everything draws but I imagine 500-600mA should be plenty. I used the official Raspberry Pi power supply (https://www.adafruit.com/product/4298) because it's cheap, small, and can provide more power than you'll need. The 20 NeoPixels alone can in theory pull 400mA (at 100% brightness and full white).
* PLA / Printing
  * You will need some clear/transparent/translucent PLA or other filament for printing the teeth and eyes so the LEDs can shine through. A small 50 gram spool of clear is plenty. The rest of the parts will need around 500 grams depending on how you print.
* Button
  * You need a small button to mount inside the antenna base. I just glued a basic 6mm x 6mm x 5mm (H) breadboard button. If you use a different size switch you might have to tweak the two 3D models for the antenna parts. There is a small amount of extra space around my button.

## 3D Printing
See doc/PRINTING.md

## Assembly
See doc/ASSEMBLY.md

## Audio Files & Prep
For copyright reasons no audio files are included. You'll have to find them online and convert them down to a low enough bitrate your microcontroller can support and to small enough file sizes for the flash storage limitations of the microcontroller. You can use the following guide to convert your files (https://learn.adafruit.com/microcontroller-compatible-audio-file-conversion).

## Audio Notes / Issues
At the time of this writing (April 2021) the RP2040 CPU is still brand new and there seems to be a few audio issues that need to be worked out with CircuitPython.
  * The first audio file played always have noise/static. Any further audio plays fine.
  * The CircuitPython audio playing() function is broken/unreliable so we can't use it to determine when audio is no longer playing. Since we want to show a special LED animation only when audio is playing, that's a problem. The current workaround for this is to add the length of the audio clip (in seconds) into the filename. For example "10-File.wav" means that file is 10 seconds long.

I'm sure both of these issues will be fixed in future releases of CircuitPython. There are open bug reports.

Unrelated to the issues above, the other issue you may have is audio being too loud or too quiet. You can't control the volume in CircuitPython and there is no easy volume control on the I2S (digital) amp. You can add a resistor to change the gain (see product page & data sheet) but I found it to still be too loud and had to modify the audio files to make them quieter.

I also tried using an analog amp (https://www.adafruit.com/product/2130), controlled with PWM (audioiopwm), which does have a gain/volume control knob, but was getting a lot of white noise/interference from the LEDs despite having them on a non-shared PWM pin and keeping it away from other wiring. It also had the same audio issues listed above.

## Other Notes / Limitations
 * The teeth and eyes are separate NeoPixel chains since I don't want the eyes included in the animations. This can easily be changed by changing wiring and code. 
 * I was originally planning to make my own LED animations but once I found the CircuitPython LED animation library I ended up just using that since it has plenty of variety. Integrating your own custom animations will be tough since I use the AnimationSequence() class. I briefly pause the animation sequence while audio is playing to show the special "talking" animation, then resume it when audio is done.
 * Remember this is a microcontroller with not much storage space. You'll only be able to store a couple minutes of audio, total. 
 
 ## Credits
 The original idea and 3D model came from another project (https://www.thingiverse.com/thing:4384974). I completely changed the electronics and code to run from a microcontroller instead of a Raspberry Pi. I've made some various changes to the some 3D models to support my hardware and project changes. The original files as well as updated files are all available as well as the editable sources if you need to tweak things.