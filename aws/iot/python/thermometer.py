#!/usr/bin/env python3
import argparse
import random

from things import Thing

class Thermometer(Thing):
    @classmethod
    def get_data(cls):
        return round(random.uniform(35.5, 42.5), 1)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate random temperatures and publish them.")
    parser.add_argument('--device-id', default='thermometer-livingroom', type=str, help='Device id')
    parser.add_argument('--topic', default='world', type=str, help='MQtt topic.')
    parser.add_argument('--publish-delay', default=30, type=int, help='Time between each published message')
    parser.add_argument(
        '--endpoint',
        default="a15645u9kev0b1-ats.iot.eu-west-2.amazonaws.com",
        help="Your AWS IoT custom endpoint, not including a port. " +
             "Ex: \"abcd123456wxyz-ats.iot.us-east-1.amazonaws.com\""
    )
    parser.add_argument(
        '--cert_filepath', default='/home/ubuntu/certs/certificate.pem.crt',
        help="File path to your client certificate, in PEM format."
    )
    parser.add_argument(
        '--pri_key_filepath', default='/home/ubuntu/certs/private.pem.key',
        help="File path to your private key, in PEM format."
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    thermometer = Thermometer(
        args.device_id,
        args.topic,
        args.publish_delay,
    )
    thermometer.connect(args.endpoint, args.cert_filepath, args.pri_key_filepath)
    thermometer.run()