from gpiozero import DistanceSensor, PWMOutputDevice, LED
from time import sleep

# Set up distance sensor (trigger, echo)
sensor = DistanceSensor(echo=24, trigger=17, max_distance=2)

# Set up buzzer (PWM pin)
buzzer = PWMOutputDevice(27)  # GPIO18

# Red
red1 = LED(22)
red2 = LED(23)

# Yellow
yellow1 = LED(25)
yellow2 = LED(16)

# Green
green1 = LED(26)
green2 = LED(6)

def update_leds(distance):
    # Turn all off first
    for led in [green1, green2, yellow1, yellow2, red1, red2]:
        led.off()

    if distance < 5:
        red1.on()
        red2.on()
    elif distance < 15:
        red1.on()
        red2.on()
        yellow1.on()
    elif distance < 25:
        red1.on()
        red2.on()
        yellow1.on()
        yellow2.on()
    elif distance < 35:
        red1.on()
        red2.on()
        yellow1.on()
        yellow2.on()
        green1.on()
    elif distance < 50:
        red1.on()
        red2.on()
        yellow1.on()
        yellow2.on()
        green1.on()
        green2.on()

def calculate_beep_interval(distance_cm):
    """
    Maps distance (5-50cm) to beep interval (fast near, slow far)
    """
    if distance_cm > 50:
        return None  # Too far — no beep
    elif distance_cm < 5:
        distance_cm = 5

    # Map distance 5–50 cm → interval 0.05s – 0.5s
    interval = (distance_cm - 5) / (50 - 5) * (0.5 - 0.05) + 0.05
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
    for led in [green1, green2, yellow1, yellow2, red1, red2]:
        led.off()
    print("\nStopped")

