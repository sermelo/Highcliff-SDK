# Example script for building a component

# Your code should go in this file...

# Define script -> pack and upload to s3 -> deploy stack -> deploy component to device

# To deploy as a component:

# 1. Pack script using pack.sh
# 2. Uncomment the 'component' area in cdk/data_ingest_stack.py...
#       this will push the script to s3 and create the component in the console
# 3. Deploy the component...
#    visit the AWS Console, IoT Core > Greengrass > Components
#    https://eu-west-2.console.aws.amazon.com/iot/home?region=eu-west-2#/greengrass/v2/components
#    select your component and click deploy 

from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
from random import randrange
from datetime import datetime
import time as t
import json
import csv



# New function added to retrieve sample temp data from csv file:
# returns boolean value to reflect if there has been a temp change,
# along with temp value
def _checkTemp(file_name: str, historic_temp: float):
    f = open(file_name, "r")
    c = csv.reader(f, delimiter=',')

    for i, x in enumerate(c):
        if i == 0:
            new_temp = float(x[1])
            sample_time = x[0]
            if new_temp != historic_temp:
                return True, new_temp, sample_time
            else:
                return False, historic_temp, sample_time


# Define ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, MESSAGE, TOPIC, and RANGE
ENDPOINT = "a15645u9kev0b1-ats.iot.eu-west-2.amazonaws.com" # change value per subscription, found in IOT CORE > SETTINGS
PATH_TO_CERTIFICATE = "/home/ubuntu/certs/certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "/home/ubuntu/certs/private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "/home/ubuntu/certs/AmazonRootCA1.pem"
TOPIC = "test/temperatures-control-local" # change per deployment, UNIQUE VALUE PER STACK
RANGE = 20
CLIENT = 'smf-local-device-' + str(randrange(1000, 9000)) # change per deployment, UNIQUE VALUE PER STACK

event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=ENDPOINT,
            cert_filepath=PATH_TO_CERTIFICATE,
            pri_key_filepath=PATH_TO_PRIVATE_KEY,
            client_bootstrap=client_bootstrap,
            ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
            client_id=CLIENT,
            clean_session=False,
            keep_alive_secs=6
            )

connect_future = mqtt_connection.connect()
connect_future.result()

historic_temp = 1
while True:
    is_temp_diff, current_temp, sample_time = _checkTemp(file_name='/home/ubuntu/temps.csv', historic_temp=historic_temp)

    if is_temp_diff == True:

        if int(current_temp) >= 39:
            action = 'temp_turn_down'
        elif int(current_temp) in (38, 37):
            action = 'maintain_temp'
        else:
            action = 'turn_temp_up'

        j = {}
        j['device_id'] = CLIENT
        j['action'] = action
        j['pre_change_detected_temp'] = current_temp
        j['action_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = json.dumps(j)
        print(message)
        mqtt_connection.publish(topic=TOPIC, payload=message, qos=mqtt.QoS.AT_LEAST_ONCE)
        t.sleep(20)

    historic_temp = current_temp


disconnect_future = mqtt_connection.disconnect()
disconnect_future.result()