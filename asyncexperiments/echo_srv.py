import asyncio
import socket
import logging
from asyncio import AbstractEventLoop

async def echo(connection: socket.socket,
               loop: AbstractEventLoop) -> None:
    peer = connection.getpeername()
    buff = b''
    try:
        await loop.sock_sendall(connection, b'Hello! This is a my echoserver!\r\n')
        while data := await loop.sock_recv(connection, 1024):
            buff += data
            if buff[-2:] == b'\r\n':
                await loop.sock_sendall(connection, buff)
                print(peer, buff[:-2])
                buff = b''
    except:
        logging.exception(f"{peer} connection lost")
    finally:
        buff = b''
        connection.close()

async def listen_for_connection(server_socket: socket,
                                loop: AbstractEventLoop):
    while True:
        connection, address = await loop.sock_accept(server_socket)
        connection.setblocking(False)
        print(f"Connection query from {address}")
        asyncio.create_task(echo(connection, loop))

async def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_address = ('127.0.0.1', 8000)
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()
    await listen_for_connection(server_socket, asyncio.get_event_loop())

asyncio.run(main())
