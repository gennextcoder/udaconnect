import grpc
import location_pb2
import location_pb2_grpc

"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""

print("Sending sample payload...")

channel = grpc.insecure_channel("localhost:5005")
stub = location_pb2_grpc.LocationServiceStub(channel)

# Update this with desired payload
location = location_pb2.LocationMessage(
    id=2222,
    person_id=8,
    latitude='37.3387',
    longitude='121.8853',
    creation_time='2020-07-07 10:38:06.000001'
)


response = stub.Create(location)