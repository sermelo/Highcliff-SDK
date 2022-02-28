# needed to make local variables behave like centralized infrastructure
from highcliff.singleton import Singleton

# needed for message queuing and validation
from jsonschema import validate, ValidationError
import json

# needed to reference the json schema file from within the host application
import pkgutil


class InvalidMessageFormat(Exception):
    pass


class InvalidTopic(Exception):
    pass


class Network:
    def __init__(self):
        pass

    def the_world(self):
        # returns a dictionary that describes the current state of the world
        raise NotImplementedError

    def update_the_world(self, update):
        # adds the given update to the persistent store of the world state
        raise NotImplementedError

    def create_topic(self, topic):
        # creates the given topic in the centralized message queue
        raise NotImplementedError

    def publish(self, topic, message):
        # uses the centralized message queue to publish the given message to the given topic
        raise NotImplementedError

    def subscribe(self, topic, callback_function):
        # registers the given callback function to be called by the centralized message queue
        # when a message is published to the given topic
        raise NotImplementedError


@Singleton
class LocalNetwork(Network):
    __the_world = {}
    __message_queue = {}

    # refer to the package schema file in the host
    __json_schema_file_path = 'schema.json'
    __json_schema_string = pkgutil.get_data(__name__, __json_schema_file_path).decode("utf-8")
    __json_schema = json.loads(__json_schema_string)

    def the_world(self):
        return self.__the_world

    def update_the_world(self, update):
        self.__the_world.update(update)

    def create_topic(self, topic):
        self.__message_queue[topic] = []

    def topics(self):
        return list(self.__message_queue.keys())

    def publish(self, topic, message):
        # raise an error to the caller if the topic is invalid
        try:
            self.__validate_topic(topic)
        except InvalidTopic:
            raise InvalidTopic

        self.__validate_message(message)

        # add the effects associated with the message to the world
        self.update_the_world(message["effects"])

        # call each callback function registered under the given topic
        for callback in self.__message_queue[topic]:
            callback(topic, message)

    def subscribe(self, topic, callback_function):
        # register the callback function under the given topic
        self.__message_queue[topic].append(callback_function)

    def reset(self):
        # clears all state
        self.__the_world = {}
        self.__message_queue = {}

    def __validate_topic(self, topic):
        # validate the the topic exists in the communication infrastructure
        if topic not in self.__message_queue.keys():
            raise InvalidTopic

    def __validate_message(self, json_message):
        # validate the schema against the message and raise an error if invalid
        try:
            validate(json_message, self.__json_schema)
        except ValidationError:
            raise InvalidMessageFormat
