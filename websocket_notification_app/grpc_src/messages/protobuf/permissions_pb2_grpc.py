# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from ..protobuf import permissions_pb2 as protobuf_dot_permissions__pb2


class PermissionStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CheckPermission = channel.unary_unary(
            '/permissions.Permission/CheckPermission',
            request_serializer=protobuf_dot_permissions__pb2.PermissionRequest.SerializeToString,
            response_deserializer=protobuf_dot_permissions__pb2.PermissionResponse.FromString,
        )


class PermissionServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CheckPermission(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PermissionServicer_to_server(servicer, server):
    rpc_method_handlers = {
        'CheckPermission': grpc.unary_unary_rpc_method_handler(
            servicer.CheckPermission,
            request_deserializer=protobuf_dot_permissions__pb2.PermissionRequest.FromString,
            response_serializer=protobuf_dot_permissions__pb2.PermissionResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        'permissions.Permission', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class Permission(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CheckPermission(request,
                        target,
                        options=(),
                        channel_credentials=None,
                        call_credentials=None,
                        insecure=False,
                        compression=None,
                        wait_for_ready=None,
                        timeout=None,
                        metadata=None):
        return grpc.experimental.unary_unary(request, target, '/permissions.Permission/CheckPermission',
                                             protobuf_dot_permissions__pb2.PermissionRequest.SerializeToString,
                                             protobuf_dot_permissions__pb2.PermissionResponse.FromString,
                                             options, channel_credentials,
                                             insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
