import asyncio


async def do_echo(reader, writer):
    while True:
        data = await reader.read(100)
        if data:
            message = data.decode()
            cli_addr = writer.get_extra_info('peername')
            print(f'Received {message!r} from {cli_addr}')
            print(f'Send: {message}')
            writer.write(data)
            await writer.drain()  # 버퍼 오버플로우 방지를 위해 일정 용량 확보 대기
        else:
            break
        writer.close()
        print(f'data socket to {cli_addr} closed!')


async def main():
    server = await asyncio.start_server(do_echo, '127.0.0.1', 8831)
    print(f'Serving on {server.sockets[0].getsockname()}')
    await server.serve_forever()
asyncio.run(main())
