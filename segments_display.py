import RPi.GPIO as GPIO
import time

# BCM pin mappings
segmentPins = {
    'A': 17,
    'B': 18,
    'C': 27,
    'D': 22,
    'E': 23,
    'F': 24,
    'G': 25,
    'DP': 4  # Optional
}

# Segment encoding
digits = {
    '0': ['A','B','C','D','E','F'],
    '1': ['B','C'],
    '2': ['A','B','G','E','D'],
    '3': ['A','B','C','D','G'],
    '4': ['B','C','F','G'],
    '5': ['A','C','D','F','G'],
    '6': ['A','C','D','E','F','G'],
    '7': ['A','B','C'],
    '8': ['A','B','C','D','E','F','G'],
    '9': ['A','B','C','D','F','G']
}

def setup():
    GPIO.setmode(GPIO.BCM)
    for pin in segmentPins.values():
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

def display_digit(n):
    for seg in segmentPins:
        GPIO.output(segmentPins[seg], GPIO.LOW)
    for seg in digits[n]:
        GPIO.output(segmentPins[seg], GPIO.HIGH)

try:
    setup()
    while True:
        for n in range(10):
            display_digit(str(n))
            time.sleep(1)
finally:
    GPIO.cleanup()

