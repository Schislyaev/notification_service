import grpc

from core.logger import Logger
from core.settings import settings
from grpc_src.messages.protobuf import permissions_pb2, permissions_pb2_grpc

logger = Logger(__name__)


async def check_user_rights(token: str, url: str):
    with grpc.insecure_channel(f'{settings.grpc_host}:{settings.grpc_port}') as channel:
        stub = permissions_pb2_grpc.PermissionStub(channel)
        response = stub.CheckPermission(permissions_pb2.PermissionRequest(token=token, url=url))
        return response


async def jwt_check(token, request_path):
    if settings.log_level == 'DEBUG':
        user_id = '5421770f-dd22-467c-8a01-861237fdd159'
    else:
        user_data = await check_user_rights(token=token, url=request_path)
        try:
            user_id = user_data['user_id']
        except IndexError as e:
            logger.debug(e)
    return user_id
