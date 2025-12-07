from sense_hat import SenseHat
import time
from datetime import datetime
from socket import *
import json

# Opret forbindelse til Sense HAT
sense = SenseHat()

# Gem sidste måling til sammenligning
last_pitch, last_roll, last_yaw = 0, 0, 0
threshold = 5  # hvor mange grader ændring der skal til for at registrere bevægelse

# Opret UDP socket til broadcasting
BROADCAST_IP = '255.255.255.255'
BROADCAST_PORT = 20000
socket_sender = socket(AF_INET, SOCK_DGRAM)
socket_sender.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

while True:
    orientation = sense.get_orientation()
    pitch = orientation['pitch']   # frem/tilbage
    roll = orientation['roll']     # til siderne
    yaw = orientation['yaw']       # rotation omkring lodret akse

    # Udskriv vinklerne
    print(f"Pitch: {pitch:.2f}°, Roll: {roll:.2f}°, Yaw: {yaw:.2f}°")

    # Tjek om der er bevægelse (ændring større end threshold)
    if (abs(pitch - last_pitch) > threshold or
        abs(roll - last_roll) > threshold or
        abs(yaw - last_yaw) > threshold):
        
        # Registrer tidspunktet
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Motion detected at {timestamp}")

        #pak data i JSON og send som broadcast
        #jeg bruger round() for at begrænse antallet af decimaler, så der kun er to decimaler
        data = {
            "pitch": round(pitch, 2),
            "roll": round(roll, 2),
            "yaw": round(yaw, 2),
            'timestamp': timestamp
        }
        message = json.dumps(data).encode('utf-8')
        socket_sender.sendto(message, (BROADCAST_IP, BROADCAST_PORT))


    # Opdater sidste måling
    last_pitch, last_roll, last_yaw = pitch, roll, yaw

    time.sleep(0.5)  # vent et halvt sekund mellem målinger
## broadcast 

