from gpiozero import DistanceSensor, PWMOutputDevice, LED
from time import sleep

# === CONFIGURABLE PARAMETERS ===
MIN_DISTANCE_CM = 5      # Closest distance to trigger full response
MAX_DISTANCE_CM = 50     # Beyond this distance, everything is off

# ===============================
sensor = DistanceSensor(echo=24, trigger=17, max_distance=2)
buzzer = PWMOutputDevice(27)  # GPIO18

# LEDs
red1 = LED(22)
red2 = LED(23)
yellow1 = LED(25)
yellow2 = LED(16)
green1 = LED(26)
green2 = LED(6)

leds = [green2, green1, yellow2, yellow1, red2, red1]  # Order: far → close

def update_leds(distance):
    for led in leds:
        led.off()

    if distance > MAX_DISTANCE_CM:
        return

    # Divide distance range into 6 steps (one for each LED)
    step = (MAX_DISTANCE_CM - MIN_DISTANCE_CM) / len(leds)

    # Determine how many LEDs to light
    leds_to_light = int((MAX_DISTANCE_CM - distance) / step)

    for i in range(min(leds_to_light, len(leds))):
        leds[i].on()

def calculate_beep_interval(distance_cm):
    if distance_cm > MAX_DISTANCE_CM:
        return None
    elif distance_cm < MIN_DISTANCE_CM:
        distance_cm = MIN_DISTANCE_CM

    interval = ((distance_cm - MIN_DISTANCE_CM) /
                (MAX_DISTANCE_CM - MIN_DISTANCE_CM)) * (0.5 - 0.05) + 0.05
    return interval

try:
    while True:
        dist_cm = sensor.distance * 100
        update_leds(dist_cm)

        interval = calculate_beep_interval(dist_cm)
        if interval:
            buzzer.on()
            sleep(0.05)
            buzzer.off()
            sleep(interval)
        else:
            buzzer.off()
            sleep(0.2)

except KeyboardInterrupt:
    buzzer.off()
    for led in leds:
        led.off()
    print("\nStopped")

