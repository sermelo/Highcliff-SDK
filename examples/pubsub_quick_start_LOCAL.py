# needed to run and access the infrastructure needed to communicate and coordinate
from highcliff.infrastructure import LocalNetwork, InvalidTopic

# define the infrastructure that provides the message queue functionality
network = LocalNetwork.instance()

# define the topic to which we will publish/subscribe
topic_something_on_my_ear = "0020"


# this is the function that will be run when a message is published to our topic
def callback(topic, message):
    print("on the topic of: ", topic)
    print("we received this message: ", message)


# create and subscribe to the topic
network.create_topic(topic_something_on_my_ear)
network.subscribe(topic_something_on_my_ear, callback)

# publish a message to the topic
test_message = {
    "payload": "this is a test message",
    "effects": {"first_effect": True, "second_effect": True}
}
network.publish(topic_something_on_my_ear, test_message)
