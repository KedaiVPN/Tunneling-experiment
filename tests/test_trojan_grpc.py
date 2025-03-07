import asyncio
import grpc
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from protocols import trojan_pb2, trojan_pb2_grpc

async def test_echo():
    async with grpc.aio.insecure_channel('localhost:8447') as channel:
        stub = trojan_pb2_grpc.TrojanServiceStub(channel)
        response = await stub.Echo(trojan_pb2.EchoRequest(message="Hello Trojan gRPC!"))
        print(f"Echo test response: {response.message}")

async def test_stream_data():
    async with grpc.aio.insecure_channel('localhost:8447') as channel:
        stub = trojan_pb2_grpc.TrojanServiceStub(channel)
        
        async def request_generator():
            messages = [b"Test data 1", b"Test data 2", b"Test data 3"]
            for msg in messages:
                yield trojan_pb2.DataRequest(data=msg)
                await asyncio.sleep(0.1)  # Simulate some delay between messages
        
        try:
            async for response in stub.StreamData(request_generator()):
                print(f"Received stream response, size: {len(response.data)} bytes")
        except grpc.RpcError as e:
            print(f"gRPC error: {e.details()}")

async def main():
    print("Testing Trojan gRPC service...")
    await test_echo()
    await test_stream_data()
    print("gRPC tests completed")

if __name__ == "__main__":
    asyncio.run(main())
