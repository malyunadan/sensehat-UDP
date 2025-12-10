from sense_hat import SenseHat
import time
from datetime import datetime, timezone
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

try:
    while True:
        orientation = sense.get_orientation()
        pitch = orientation['pitch']   # frem/tilbage
        roll = orientation['roll']     # til siderne
        yaw = orientation['yaw']       # rotation omkring lodret akse

        # Beregn tilt som samlet hældning (pitch + roll+ yaw )begrænset til 360 grader 
        tilt = round((pitch**2 + roll**2 + yaw**2) ** 0.5 % 360, 2)

        # Udskriv vinklerne
        print(f"Pitch: {pitch:.2f}°, Roll: {roll:.2f}°, Yaw: {yaw:.2f}°, Tilt: {tilt:.2f}°")

        # Tjek om der er bevægelse (ændring større end threshold)
        if (abs(pitch - last_pitch) > threshold or
            abs(roll - last_roll) > threshold or
            abs(yaw - last_yaw) > threshold):

            # Registrer tidspunktet i ISO-8601 format
            timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
            print(f"Motion detected at {timestamp}")

            # Pak data i JSON og send som broadcast
            SensorEvent_dictionary = {
                "PackageId": "1234",  # eksempel på PackageId
                "Description": "Glas",
                "LimitprofilId": "1",
                "evt": "SensorEvent",   # felt som dit API kræver
                "pitch": round(pitch, 2),
                "roll": round(roll, 2),
                "yaw": round(yaw, 2),
                "tilt": tilt,
                "timestamp": timestamp
            }

            message: str = json.dumps(SensorEvent_dictionary)
            message_bytes = message.encode()
            socket_sender.sendto(message_bytes, (BROADCAST_IP, BROADCAST_PORT))
            print(f'Broadcaster sending: {message}')

        # Opdater sidste måling
        last_pitch, last_roll, last_yaw = pitch, roll, yaw
        time.sleep(5)  # vent 5 sekunder mellem målinger

finally:
    socket_sender.close()  # Luk socketten når programmet afsluttes