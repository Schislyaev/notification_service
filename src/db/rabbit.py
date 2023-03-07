from typing import Optional, Tuple

from aio_pika import Connection
from aio_pika.abc import AbstractChannel

connection: Connection | None = None
channel: AbstractChannel | None = None


async def get_rabbit() -> Tuple[Optional[Connection], Optional[AbstractChannel]]:
    return connection, channel
