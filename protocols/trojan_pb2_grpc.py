# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from protocols import trojan_pb2 as protocols_dot_trojan__pb2

GRPC_GENERATED_VERSION = '1.70.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in protocols/trojan_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class TrojanServiceStub(object):
    """Define the Trojan service
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Echo = channel.unary_unary(
                '/trojan.TrojanService/Echo',
                request_serializer=protocols_dot_trojan__pb2.EchoRequest.SerializeToString,
                response_deserializer=protocols_dot_trojan__pb2.EchoResponse.FromString,
                _registered_method=True)
        self.StreamData = channel.stream_stream(
                '/trojan.TrojanService/StreamData',
                request_serializer=protocols_dot_trojan__pb2.DataRequest.SerializeToString,
                response_deserializer=protocols_dot_trojan__pb2.DataResponse.FromString,
                _registered_method=True)


class TrojanServiceServicer(object):
    """Define the Trojan service
    """

    def Echo(self, request, context):
        """Basic echo request/response for testing
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StreamData(self, request_iterator, context):
        """Stream for actual data transfer
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TrojanServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Echo': grpc.unary_unary_rpc_method_handler(
                    servicer.Echo,
                    request_deserializer=protocols_dot_trojan__pb2.EchoRequest.FromString,
                    response_serializer=protocols_dot_trojan__pb2.EchoResponse.SerializeToString,
            ),
            'StreamData': grpc.stream_stream_rpc_method_handler(
                    servicer.StreamData,
                    request_deserializer=protocols_dot_trojan__pb2.DataRequest.FromString,
                    response_serializer=protocols_dot_trojan__pb2.DataResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'trojan.TrojanService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('trojan.TrojanService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class TrojanService(object):
    """Define the Trojan service
    """

    @staticmethod
    def Echo(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/trojan.TrojanService/Echo',
            protocols_dot_trojan__pb2.EchoRequest.SerializeToString,
            protocols_dot_trojan__pb2.EchoResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def StreamData(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(
            request_iterator,
            target,
            '/trojan.TrojanService/StreamData',
            protocols_dot_trojan__pb2.DataRequest.SerializeToString,
            protocols_dot_trojan__pb2.DataResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
