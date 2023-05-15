import asyncio


async def echo_client():
    reader, writer = await asyncio.open_connection('127.0.0.1', 8831)
    while True:
        message = input("Enter: ")
        if message.upper() != "QUIT":
            print(f'Send: {message}')
            writer.write(message.encode())
            await writer.drain()
            data = await reader.read(100)
            print(f'Received: {data.decode()}')
        else:
            break
    writer.close()
asyncio.run(echo_client())
