#!/usr/bin/env python
#-*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import pyaudio
import wave
import os
import sys
import cv2

def rec_fun():
    # hide the wrong information
    os.close(sys.stderr.fileno())
    
    BUTT = 17    # GPIO 17, the button that start recording when pressed
    GPIO.setmode(GPIO.BCM)
    # the button voltage become low when pressed
    GPIO.setup(BUTT, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    # CHUNK could be intepreted as data package or pieces
    CHUNK = 512 
    FORMAT = pyaudio.paInt16  
    RATE = 44100  # 44100 samples/second, sampling rate
    WAVE_OUTPUT_FILENAME = "/home/pi/final_project/Voice/voice_record.wav"
    print('Please start recording by pressing the button 17...')
    GPIO.wait_for_edge(BUTT, GPIO.FALLING)
    #key = cv2.waitKey(-1) & 0xFF
    '''mark = True
    while mark:
        key = cv2.waitKey(1) & 0xFF
        if key == ord("r"):
            print("Recording...")
            p = pyaudio.PyAudio()
            stream = p.open(format = FORMAT,
                        channels = 1,  
                        rate = RATE,
                        input = True,
                        frames_per_buffer = CHUNK)
            #print("Recording...")
    
            frames = []
    
            while not cv2.waitKey(0):
                data = stream.read(CHUNK)
                frames.append(data)
            mark = False'''
        
    # To use PyAudio, first instantiate PyAudio using pyaudio.PyAudio(), which sets up the portaudio system.
    p = pyaudio.PyAudio()
    stream = p.open(format = FORMAT,
                    channels = 1,  
                    rate = RATE,
                    input = True,
                    frames_per_buffer = CHUNK)
    print('test')
    print("Recording...")

   
    # Recoding when button pressed, and stop when button released
    frames = []
    while GPIO.input(BUTT) == 0:
        data = stream.read(CHUNK)
        frames.append(data)
        #print("Test...")
    print("Finish recording,file output：" + WAVE_OUTPUT_FILENAME + '\n')
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(FORMAT))    # Returns the size (in bytes) for the specified sample format.
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    return

if __name__ == '__main__':
    rec_fun()
