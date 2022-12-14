from kivy.app import App
from kivy.uix.button import Button
#from __future__ import division #Avoid division problems in Python 2
import math
import pyaudio
import sys
#from __future__ import division
import math

from pyaudio import PyAudio # sudo apt-get install python{,3}-pyaudio

class TestApp(App):
    def build(self):
        return Button(text='Hello World',
                      font_size = 30,
                      on_press = self.btn_press)
    def btn_press(self, instance):
        print("i am pressed")
        instance.text = "i am pressed"
        sine_tone(
            # see http://www.phy.mtu.edu/~suits/notefreqs.html
            frequency=440.00,  # Hz, waves per second A4
            duration=3.21,  # seconds to play sound
            volume=1,  # 0..1 how loud it is
            # see http://en.wikipedia.org/wiki/Bit_rate#Audio
            sample_rate=22050  # number of samples per second
        )

#!/usr/bin/env python
"""Play a fixed frequency sound."""


try:
    from itertools import izip
except ImportError: # Python 3
    izip = zip
    xrange = range

def sine_tone(frequency, duration, volume=1, sample_rate=22050):
    n_samples = int(sample_rate * duration)
    restframes = n_samples % sample_rate

    p = PyAudio()
    stream = p.open(format=p.get_format_from_width(1), # 8bit
                    channels=1, # mono
                    rate=sample_rate,
                    output=True)
    s = lambda t: volume * math.sin(2 * math.pi * frequency * t / sample_rate)
    samples = (int(s(t) * 0x7f + 0x80) for t in xrange(n_samples))
    for buf in izip(*[samples]*sample_rate): # write several samples at a time
        stream.write(bytes(bytearray(buf)))

    # fill remainder of frameset with silence
    stream.write(b'\x80' * restframes)

    stream.stop_stream()
    stream.close()
    p.terminate()




TestApp().run()

