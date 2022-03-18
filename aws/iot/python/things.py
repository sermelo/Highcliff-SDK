from datetime import datetime
import json
import time

from awscrt import io
from awsiot import mqtt_connection_builder
import boto3


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
            cert_filepath=cert_filepath,
            client_bootstrap=client_bootstrap,
            pri_key_filepath=pri_key_filepath,
            clean_session=False,
            keep_alive_secs=30)

    def run(self):
        while True:
            self.publish_data()
            time.sleep(self.publish_delay)

    def publish_data(self):
        payload = json.dumps({
            'device_id': self.device_id,
            'type': self.device_type,
            'sample_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'value': self.get_data(),
        })
        print(f'Publising in topic {self.world_topic}: {payload}')
        self.mqtt_client.publish(
            topic=self.world_topic,
            qos=1,
            payload=payload,
        )

    def get_data(self):
        raise NotImplementedError

    @classmethod
    def get_device_type(cls):
        return cls.__name__.lower()
