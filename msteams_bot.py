import sys
import subprocess
import paho.mqtt.client as mqtt 
from random import randrange, uniform
import time

mqttBroker ="mqtt.eclipseprojects.io" 

client = mqtt.Client("iKesh-MacbookPro")
client.connect(mqttBroker) 

 
PY3K = sys.version_info >= (3, 0)
if PY3K:
    from plistlib import loads as read_plist_from_string
else:
    from plistlib import readPlistFromString as read_plist_from_string


def check_bluetooth_connection(device_name):
    output = subprocess.check_output(["system_profiler",
                                      "-xml",
                                      "-detailLevel",
                                      "basic",
                                      "SPBluetoothDataType"])

    plist = read_plist_from_string(output)
    devices = plist[0]['_items'][0]['device_title']

    for d in devices:
        if device_name in d.keys():
            device_info = d[device_name]
            break
    else:
        msg = u"\"{}\" not found".format(device_name)
        if not PY3K:
            msg = msg.encode('utf-8')
        raise ValueError(msg)

    if device_info['device_isconnected'] == "attrib_Yes":
        return True
    else:
        return False


def main():
    # if len(sys.argv) <= 1:
    #     print("Usage: python check_bluetooth_connection.py "
    #           "bluetooth_device_name")
    #     return

    # device_name = sys.argv[1]
    device_name = 'WH-1000XM4'

    while True:
        time.sleep(1)
        if not PY3K:
            device_name = device_name.decode('utf-8')

        try:
            is_connected = check_bluetooth_connection(device_name)
        except (OSError, subprocess.CalledProcessError) as e:
            print(e)
            print("----")
            print("Failed to run \"system_profiler -xml -detailLevel basic "
                "SPBluetoothDataType\"")
            sys.exit(1)
        except ValueError as e:
            print(e)
            sys.exit(1)


        if is_connected:
            client.publish("MEETING/STATUS", "CONNECTED")
            print("Just published " + "CONNECTED" + " to topic MSTeams/Presence")
        else:
            client.publish("MEETING/STATUS", "DISCONNECTED")
            print("Just published " + "DISCONNECTED" + " to topic MSTeams/Presence")


if __name__ == '__main__':
    main()

