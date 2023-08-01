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
    person_id=23,
    coordinate='0101000000842FA75F7D874140CEEEDAEF9A645AC0',
    creation_time='2020-07-07 10:38:06.000001'
)


response = stub.Create(location)