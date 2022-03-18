from datetime import datetime
import json
import random
import time

from awscrt import io
from awsiot import mqtt_connection_builder


class Thing():
    def __init__(self, device_id, world_topic='world', publish_delay=30):
        self.device_id = device_id
        self.device_type = self.get_device_type()
        self.publish_delay = publish_delay
        self.world_topic = world_topic
        self.mqtt_client = None

    def connect(self, endpoint, cert_filepath, pri_key_filepath):
        event_loop_group = io.EventLoopGroup(1)
        host_resolver = io.DefaultHostResolver(event_loop_group)
        client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)

        self.mqtt_client = mqtt_connection_builder.mtls_from_path(
            client_id=self.device_id,
            endpoint=endpoint,
            client_bootstrap=client_bootstrap,
            cert_filepath=cert_filepath,
            pri_key_filepath=pri_key_filepath,
            on_connection_interrupted=self.on_connection_interrupted,
            on_connection_resumed=self.on_connection_resumed,
            clean_session=False,
            keep_alive_secs=30,
        )
        print(f'Connecting to {endpoint} with client ID {self.device_id}')
        connect_future = self.mqtt_client.connect()
        # Future.result() waits until a result is available
        connect_future.result()
        print('Connected')

    # Callback when connection is accidentally lost.
    def on_connection_interrupted(self, connection, error, **kwargs):
        print("Connection interrupted. error: {}".format(error))


    # Callback when an interrupted connection is re-established.
    def on_connection_resumed(self, connection, return_code, session_present, **kwargs):
        print("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))

        if return_code == mqtt.ConnectReturnCode.ACCEPTED and not session_present:
            print("Session did not persist. Resubscribing to existing topics...")
            resubscribe_future, _ = connection.resubscribe_existing_topics()

            # Cannot synchronously wait for resubscribe result because we're on the connection's event-loop thread,
            # evaluate result with a callback instead.
            resubscribe_future.add_done_callback(self.on_resubscribe_complete)

    def on_resubscribe_complete(self, resubscribe_future):
        resubscribe_results = resubscribe_future.result()
        print("Resubscribe results: {}".format(resubscribe_results))

        for topic, qos in resubscribe_results['topics']:
            if qos is None:
                sys.exit("Server rejected resubscribe to topic: {}".format(topic))

    def run(self):
        while True:
            self.publish_data()
            time.sleep(self.publish_delay)

    def publish_data(self):
        data = {
            'device_id': self.device_id,
            'type': self.device_type,
            'sample_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'value': self.get_data(),
        }
        self.publish(self.world_topic, data)

    def publish(self, topic, data):
        payload = json.dumps(data)
        print(f'Publising in topic {self.world_topic}: {payload}')
        self.mqtt_client.publish(
            topic=topic,
            payload=payload,
            qos=mqtt.QoS.AT_LEAST_ONCE,
        )

    def get_data(self):
        raise NotImplementedError

    @classmethod
    def get_device_type(cls):
        return cls.__name__.lower()

class Thermometer(Thing):
    @classmethod
    def get_data(cls):
        return round(random.uniform(35.5, 42.5), 1)

class Thermostat(Thing):
    def __init__(self, device_id, world_topic, publish_delay, init_temperature):
        super().__init__(device_id, world_topic, publish_delay)
        self.temperature = init_temperature

    def get_data(self):
        return self.temperature
