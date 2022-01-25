# needed to access the publish/subscribe functionality of Highcliff
from highcliff.pubsub import create_topic, publish, subscribe

# define the message queue global variable
# when running a local version of Highcliff, use global variables to simulate the underlying MQ infrastructure
# these global variables will be replaced with a url in the production version
queue_GLOBAL_VARIABLE = {}
the_world_GLOBAL_VARIABLE = {}

# define the topic to which we will publish/subscribe
topic_something_on_my_ear = "0020"
create_topic(queue_GLOBAL_VARIABLE, topic_something_on_my_ear)


# this is the function that will be run when a message is published to our topic
def callback(topic, message):
    print("on the topic of: ", topic)
    print("we received this message: ", message)


# subscribe to the topic
subscribe(queue_GLOBAL_VARIABLE, topic_something_on_my_ear, callback)

# publish a message to the topic
message = {
    "payload": "this is a test message",
    "effects": [{"first_effect": True}, {"second_effect": True}]
}
publish(queue_GLOBAL_VARIABLE, the_world_GLOBAL_VARIABLE, topic_something_on_my_ear, message)
