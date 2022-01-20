from highcliff.pubsub import create_topic, publish, subscribe

queue_GLOBAL_VARIABLE = {}
topic_something_on_my_ear = "0020"


def callback(topic, message):
    print("on the topic of: ", topic)
    print("we received this message: ", message)


create_topic(queue_GLOBAL_VARIABLE, topic_something_on_my_ear)
subscribe(queue_GLOBAL_VARIABLE, topic_something_on_my_ear, callback)

publish(queue_GLOBAL_VARIABLE, topic_something_on_my_ear, "this is a test message")
