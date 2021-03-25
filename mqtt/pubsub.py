from paho.mqtt import client as mqtt_client
from dotenv import load_dotenv
from datetime import datetime
import os
import pytz
import json

# Load environment variables
load_dotenv()

# Load MQTT details from .env
broker = os.getenv("BROKER")
port = int(os.getenv("PORT"))
client_id = os.getenv("CLIENT_ID")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
topic = os.getenv("TOPIC")


def publish(client, topic, message):
    result = client.publish(topic, message)
    if result[0] == 0:
        print(f"Sent `{message}` to topic `{topic}` successfully!")
    else:
        print(f"Failed to send message to topic {topic}!")


def subscribe(client, topic):
    def on_message(client, userdata, message):
        print(
            f"\r\n=== MESSAGE RECEIVED ===\r\nTOPIC: {message.topic}\r\nMESSAGE: {message.payload.decode()}")
    client.subscribe(topic)
    client.on_message = on_message


def run():
    # Initialise and Setup client
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    print(client.connect(broker, port))

    # Subscribe to the topic
    subscribe(client, topic)

    # Get current time in IST
    ist_zone = pytz.timezone('Asia/Kolkata')
    ist_time = datetime.now(ist_zone)
    formatted_time = ist_time.strftime("%d:%m:%y, %H:%M:%S")

    # Compose the message
    message = {"now": formatted_time, "name": "Swapnajit Banerjee"}

    # Publish the message
    publish(client, topic, message=json.dumps(message))

    # Loop forever to receive message from the subscribed topics
    client.loop_forever()


if __name__ == '__main__':
    run()
