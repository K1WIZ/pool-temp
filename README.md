# pool-temp
Python script to watch an MQTT topic and send temp data to influxDB

Using an ESP-F1 module, flashed with Tasmota, and with a DS18B20 waterproof temperature sensor, I'm trying to build a sensor unit that can be placed inside the pool skimmer which will report temperature every two minutes.

The goals are:
 * battery operated - using a 26650 battery
 * ultra low power sleep
 * waterproof case
 * internal antenna
 * operation for at least a year before needing to charge/replace the battery
 * DS18B20 sensor on GPIO 4
