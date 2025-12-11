from socket import *
import requests
import json

PORT = 20000
REST_API_URL = "http://localhost:5187/api/SensorEvent"

socket_receiver = socket(AF_INET, SOCK_DGRAM)
socket_receiver.bind(('', PORT))

print("proxy UDP receiver started")
print(f"Listening for incoming UDP messages on port {PORT}...")

while True:
    msg, clientAdr = socket_receiver.recvfrom(3000)
    message_str = msg.decode()
    print(f'Message from UDP broadcaster {clientAdr}: {message_str}')

    try:
        message_dictionary = json.loads(message_str)
        print(f'Converted to dictionary: {message_dictionary}')
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        continue

    try:
        response = requests.post(REST_API_URL, json=message_dictionary, timeout=5)
        print(f'Response from REST API: {response.status_code} - {response.text}')
    except requests.exceptions.RequestException as e:
        print(f"Error sending to REST API: {e}")
