from gpiozero import DistanceSensor, PWMOutputDevice, LED
from time import sleep

# Set up distance sensor (trigger, echo)
sensor = DistanceSensor(echo=24, trigger=17, max_distance=2)

# Set up buzzer (PWM pin)
buzzer = PWMOutputDevice(27)  # GPIO18

# red 2
led = LED(22)
# red 1
led = LED(23)

# yellow 2
led = LED(25)
# yellow 1
led = LED(25)

# green 2
led = LED(26)
led = LED(6)

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
        interval = calculate_beep_interval(dist_cm)

        if interval:
            buzzer.on()
            led.on()
            sleep(0.05)
            buzzer.off()
            led.off()
            sleep(interval)
        else:
            buzzer.off()
            sleep(0.2)

except KeyboardInterrupt:
    buzzer.off()
    print("\nStopped")

