from jsonschema import validate, ValidationError
import json

# needed to reference the json schema file from within the host application
import pkgutil


class InvalidMessageFormat(Exception):
    pass


# refer to the package schema file in the host
__json_schema_file_path = 'schema.json'
__json_schema_string = pkgutil.get_data(__name__, __json_schema_file_path).decode("utf-8")
__json_schema = json.loads(__json_schema_string)


def create_topic(queue_global_variable, topic):
    queue_global_variable[topic] = []


def publish(queue_global_variable, the_world_global_variable, topic, message):
    __validate_message(message)

    # add the effects associated with the message to the world
    for effect in message["effects"]:
        for key in effect:
            the_world_global_variable[key] = effect[key]

    # call each callback function registered under the given topic
    for callback in queue_global_variable[topic]:
        callback(topic, message)


def subscribe(queue_global_variable, topic, callback_function):
    # register the callback function under the given topic
    queue_global_variable[topic].append(callback_function)


def __validate_message(json_message):
    # validate the schema against the message and raise an error if invalid
    try:
        validate(json_message, __json_schema)
    except ValidationError:
        raise InvalidMessageFormat
