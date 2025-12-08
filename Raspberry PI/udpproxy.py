from socket import *
import requests
import json


PORT = 20000

# Opret UDP socket til modtagelse
socket_receiver = socket(AF_INET, SOCK_DGRAM)
socket_receiver.bind(('', PORT))

print("proxy UDP receiver started")
print(f"Listening for incoming UDP messages on port {PORT}...")

# Define REST API endpoint
REST_API_URL = "http://localhost:5187/api/SensorEvent"  # Erstat med den faktiske REST API URL


while True:
    msg, clientAdr = socket_receiver.recvfrom(3000)
    message_str = msg.decode()
    print(f'Message from UDP broadcaster {clientAdr}: {message_str}')

    message_dictionary = json.loads(message_str)
    print(f'Converted to dictionary: {message_dictionary}')

    response = requests.post(REST_API_URL, json=message_dictionary)
    # json=... automatically serializes the dictionary to JSON
    # json=... automatically sets the Content-Type header to application/json
    print(f'Response from REST API: {response.status_code} - {response.text}')  