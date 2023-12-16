import sys
import time

import ecal.core.core as ecal_core
from ecal.core.subscriber import ProtoSubscriber


import message_pb2


# Callback for receiving messages
def callback(topic_name, hello_world_proto_msg, time):
    print("Message {} from {}: {}".format(hello_world_proto_msg.sender))


if __name__ == "__main__":
    # initialize eCAL API. The name of our Process will be
    # "Python Protobuf Subscriber"
    ecal_core.initialize(sys.argv, "Python Protobuf Subscriber")

    # Create a Protobuf Publisher that publishes on the topic
    # "hello_world_python_protobuf_topic". The second parameter tells eCAL which
    # datatype we are expecting to receive on that topic.
    sub = ProtoSubscriber("hello_world_python_protobuf_topic"
                          , message_pb2.Ready)

    # Set the Callback
    sub.set_callback(callback)

    # Just don't exit
    while ecal_core.ok():
        time.sleep(0.5)

    # finalize eCAL API
    ecal_core.finalize()