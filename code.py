import board
import digitalio
import neopixel
import time
import random
import audiocore
import audiobusio
import audiopwmio
import adafruit_led_animation.color as color
from os import listdir
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.animation.sparklepulse import SparklePulse

# Setup motion detector
motion = digitalio.DigitalInOut(board.D9)
motion.direction = digitalio.Direction.INPUT

# Setup the mode button
button = digitalio.DigitalInOut(board.D10)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

# Setup audio
audio = audiobusio.I2SOut(board.TX, board.RX, board.D25)
#audio = audiopwmio.PWMAudioOut(board.TX)

# Setup NeoPixels. My strip is GRB, others are RGB. 
# Code isn't written with RGBW or GRBW strips, see CircuitPython doc if you have one. Code changes will be needed.
teeth = neopixel.NeoPixel(board.D6, 18, brightness=0.5, auto_write=False, pixel_order=neopixel.GRB)
eyes = neopixel.NeoPixel(board.D5, 2, brightness=0.5, auto_write=False, pixel_order=neopixel.GRB)

# Initial operating mode
# 1 = periodic audio, motion detector on, lights on
# 2 = periodic audio, motion detector off, lights on
# 3 = no audio, lights on
mode = 3

# A random audio file will play sometime between these time thresholds (seconds)
min_audio_timer = 15
max_audio_timer = 20

# Wait time before starting to check for motion again after triggering (seconds)
motion_timer = 10

# The teeth will change animations after (seconds)
teeth_timer = 10

# The eyes will change color sometime between these time thresholds (seconds)
min_eye_timer = 5
max_eye_timer = 10

# Define any colors to be used when pulling a "random" color. These are RGB tuples like (255, 33, 128)
colors = [  color.RED,
            color.BLUE,
            color.GREEN,
            color.AMBER,
            color.AQUA,
            color.CYAN,
            color.GOLD,
            color.JADE,
            color.MAGENTA,
            #color.OLD_LACE,
            #color.WHITE,
            #color.BLACK, #led off
            color.ORANGE,
            color.PINK,
            color.PURPLE,
            color.TEAL,
            color.YELLOW ]

# Configure animations
animation1 = Blink(teeth, speed=0.5, color=random.choice(colors))
animation2 = ColorCycle(teeth, speed=1.0, colors=((255, 0, 0), (255, 40, 0), (255, 150, 0), (0, 255, 0), (0, 0, 255), (180, 0, 255)))
animation3 = Solid(teeth, color=random.choice(colors))
animation4 = Chase(teeth, speed=0.5, color=random.choice(colors), size=2, spacing=3, reverse=False)
animation5 = Comet(teeth, speed=0.1, color=random.choice(colors), tail_length=10, reverse=False, bounce=True, ring=False)
animation6 = Pulse(teeth, speed=0.1, color=random.choice(colors), period=5)
animation7 = Rainbow(teeth, speed=0.1, period=5, step=1, precompute_rainbow=True)
animation8 = Sparkle(teeth, speed=0.1, color=random.choice(colors), num_sparkles=2)
animation9 = RainbowChase(teeth, speed=0.01, size=1, spacing=0, reverse=False, step=16)
animation10 = RainbowSparkle(teeth, speed=0.3, period=5, num_sparkles=2, step=1, background_brightness=0.2, precompute_rainbow=True)
animation11 = SparklePulse(teeth, speed=0.1, color=random.choice(colors), period=5, max_intensity=1, min_intensity=0)
animation12 = RainbowComet(teeth, speed=0.1, tail_length=10, reverse=False, bounce=True, colorwheel_offset=0, step=0, ring=False)

animations = AnimationSequence( #animation1, 
                                animation2, 
                                #animation3, 
                                animation4, 
                                animation5, 
                                animation6, 
                                animation7, 
                                animation8, 
                                animation9, 
                                animation10, 
                                animation11,
                                animation12,
                                advance_interval=teeth_timer, random_order=True)
### end config ###
                    
# Misc init
eyes[0] = random.choice(colors)
eyes[1] = random.choice(colors)
eyes.show()
prev_mode = mode
last_audio = 0
next_audio = time.monotonic() + random.randint(min_audio_timer, max_audio_timer)
next_left_eye = time.monotonic() + random.randint(min_eye_timer, max_eye_timer)
next_right_eye = time.monotonic() + random.randint(min_eye_timer, max_eye_timer)
last_motion = time.monotonic()
print("-----Starting-----")

def play_audio():

    # Load a random audio file, get the lenth from the first 2 characters of the file name
    files = [f for f in listdir("audio")]
    file = random.choice(files)
    #file = "01-Front_Center.wav"
    length = int(file[:2])
    data = open("audio/" + file, "rb")
    wav = audiocore.WaveFile(data)
    audio.play(wav, loop=False)

    # Teeth "talking" animation for as long as the audio is playing
    # Hack while audio.playing() is bugged? in CircuitPython
    animations.freeze()
    last_audio = time.monotonic()

    i = 0
    eyes.fill(color.WHITE)
    eyes.show()
    while(time.monotonic() - last_audio) < (length + 0.5):
        set1 = [0, 2, 4, 7, 9, 11, 12, 14, 16]
        set2 = [1, 3, 5, 6, 8, 10, 13, 15, 17]
        if (i % 2) == 0:
            for t in set1:
                teeth[t] = color.BLUE
            for t in set2:
                teeth[t] = color.WHITE
        else:
            for t in set1:
                teeth[t] = color.WHITE
            for t in set2:
                teeth[t] = color.BLUE
        
        teeth.show()
        time.sleep(.2)
        i += 1

    # Reset audio, restore animations
    data.close()
    time.sleep(1)
    eyes[0] = random.choice(colors)
    eyes[1] = random.choice(colors)
    eyes.show()
    animations.resume()

# Workaround for first audio play always being distorted.
data = open("blank.wav", "rb")
wav = audiocore.WaveFile(data)
audio.play(wav, loop=False)
time.sleep(3)
data.close()

# Main loop
while True:
    
    #Check for button pushes and change mode
    if button.value == False:
        prev_mode = mode
        if mode == 1:
            mode = 2
        elif mode == 2:
            mode = 3
        elif mode == 3:
            mode = 1

    # Normal modes, audio with (1) and without (2) motion detector
    if mode == 1 or mode == 2:

        # Detect mode change
        if mode != prev_mode:
            if mode == 1:
                print("Changed to mode 1")
                prev_mode = mode
                teeth[0] = color.BLUE
                for p in range(1,18):
                    teeth[p] = color.BLACK
                teeth.show()
                time.sleep(1)

            else:
                print("Changed to mode 2")
                prev_mode = mode
                teeth[0] = color.BLUE
                teeth[1] = color.BLUE
                for p in range(2,18):
                    teeth[p] = color.BLACK
                teeth.show()
                time.sleep(1)

        # Check to see if we need to play a random audio file. Also reset the motion timer so we don't get too much audio 
        if time.monotonic() > next_audio:
            next_audio = time.monotonic() + random.randint(min_audio_timer, max_audio_timer)
            last_motion = time.monotonic()
            print("Play random audio")
            play_audio()

        if mode == 1:
            # Check to see if we should look for motion.
            if (time.monotonic() - last_motion) > motion_timer:
                if motion.value == True:
                    next_audio = time.monotonic() + random.randint(min_audio_timer, max_audio_timer)
                    last_motion = time.monotonic()
                    print("Motion detected")
                    play_audio()

    # Quiet mode
    elif mode == 3:
        if mode != prev_mode:
            print("Changed to mode 3")
            prev_mode = mode
            teeth[0] = color.BLUE
            teeth[1] = color.BLUE
            teeth[2] = color.BLUE
            for p in range(3,18):
                teeth[p] = color.BLACK
            teeth.show()
            time.sleep(1)

    # Change eye color
    if time.monotonic() > next_left_eye:
        next_left_eye = time.monotonic() + random.randint(min_eye_timer, max_eye_timer)
        eyes[0] = random.choice(colors)
        eyes.show()
    
    if time.monotonic() > next_right_eye:
        next_right_eye = time.monotonic() + random.randint(min_eye_timer, max_eye_timer)
        eyes[1] = random.choice(colors)
        eyes.show()

    # Show LED animations 
    animations.animate()

###