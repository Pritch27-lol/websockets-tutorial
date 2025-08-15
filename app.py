#!/usr/bin/env python

from game_sockets import handler

import asyncio
import logging
import http
import os
import signal

from websockets.asyncio.server import serve, ServerConnection
from websockets.http11 import Request

logging.basicConfig(
    format="%(asctime)s %(message)s",
    level=logging.DEBUG,
)

def health_check(connection: ServerConnection, request: Request):
    """
    Required health check for Koyeb server hosting public backend
    """
    if request.path == "/healthz":
        return connection.respond(http.HTTPStatus.OK, "Ok\n")


async def main():
    port = int(os.environ.get("PORT", "8001"))
    async with serve(handler, "", port, process_request=health_check) as server:
        loop = asyncio.get_running_loop()
        loop.add_signal_handler(signal.SIGTERM, server.close)
        await server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())
