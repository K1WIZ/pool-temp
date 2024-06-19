# NOTES:
# Install dependencies: pip install paho-mqtt 
# set to run from cron:
# @reboot /usr/bin/python3 /scripts/ptempIdb.py > /dev/null 2>&1 &

import json
import time
from datetime import datetime
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient

# MQTT settings
MQTT_BROKER = "your.mqtt.server"
MQTT_PORT = 1883
MQTT_USER = "mqtt.user"
MQTT_PASSWORD = "mqtt.passwd"
MQTT_TOPIC = "tele/tasmota_pooltemp/SENSOR"

# InfluxDB settings
INFLUXDB_HOST = "influxdb.host"
INFLUXDB_PORT = 8086
INFLUXDB_USER = "influx.user"
INFLUXDB_PASSWORD = "influx.passwd"
INFLUXDB_DATABASE = "ptemp"                 # change to suit your needs if necessary
INFLUXDB_MEASUREMENT = "pool_temp"

# InfluxDB connection
def connect_influxdb():
    client = InfluxDBClient(
        host=INFLUXDB_HOST,
        port=INFLUXDB_PORT,
        username=INFLUXDB_USER,
        password=INFLUXDB_PASSWORD,
        database=INFLUXDB_DATABASE
    )
    return client

# MQTT on_connect callback
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")
    client.subscribe(MQTT_TOPIC)

# MQTT on_message callback
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        if 'DS18B20' in payload:
            temp_celsius = payload['DS18B20']['Temperature']
            temp_fahrenheit = (temp_celsius * 9/5) + 32  # Convert Celsius to Fahrenheit
            temp_fahrenheit = round(temp_fahrenheit, 1)  # Limit to one decimal place
            current_time = datetime.utcnow().isoformat()

            influxdb_client = connect_influxdb()
            json_body = [
                {
                    "measurement": INFLUXDB_MEASUREMENT,
                    "time": current_time,
                    "fields": {
                        "temperature": temp_fahrenheit
                    }
                }
            ]
            influxdb_client.write_points(json_body)
            influxdb_client.close()

            print(f"Updated data on InfluxDB: Time={current_time}, Temperature={temp_fahrenheit}")

    except Exception as e:
        print(f"Error: {e}")

# Main function
def main():
    client = mqtt.Client()
    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    client.loop_forever()

if __name__ == "__main__":
    main()
