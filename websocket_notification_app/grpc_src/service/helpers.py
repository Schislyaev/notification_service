import grpc
from fastapi import HTTPException

from core.settings import settings
from grpc_src.messages.protobuf import permissions_pb2, permissions_pb2_grpc


async def check_user_rights(token: str, url: str):
    with grpc.insecure_channel(f'{settings.grpc_host}:{settings.grpc_port}') as channel:
        stub = permissions_pb2_grpc.PermissionStub(channel)
        response = stub.CheckPermission(permissions_pb2.PermissionRequest(token=token, url=url))
        return response


async def get_user(token: str, request_path: str):
    if settings.debug:
        return '5421770f-dd22-467c-8a01-861237fdd159'

    user_data = await check_user_rights(token=token, url=request_path)
    if user_data['status'] != '200':
        raise HTTPException(status_code=user_data['status'])

    return user_data['user_id']
