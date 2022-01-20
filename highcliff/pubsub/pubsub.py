def create_topic(queue_global_variable, topic):
    queue_global_variable[topic] = []


def publish(queue_global_variable, topic, message):
    # call each callback function registered under the given topic
    for callback in queue_global_variable[topic]:
        callback(topic, message)


def subscribe(queue_global_variable, topic, callback_function):
    # register the callback function under the given topic
    queue_global_variable[topic].append(callback_function)
