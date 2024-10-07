import asyncio
import json
from uuid import uuid4
from random import randbytes

clients_left = 3
writers = {}


async def handle_client(reader, writer):
    global clients_left
    global writers
    clients_left -= 1

    id = uuid4()
    writers[id] = writer
    writer.write((str(id) + '\n').encode())
    await writer.drain()

    while clients_left > 0:
        await asyncio.sleep(1)

    msgs = [
        b'Hello, World!', b'Lorem ipsum dolor sit amet,', b'Good luck, and who knows...', b'A monad is just a monoid in the category of endofunctors',
        b'\xe0\xb6\x9e', b'Nondeterministic Turing Machine with k finite memory tapes', b'I use Arch btw', b'Rewrite it in Rust',
        b'When life gives you lemons, don\'t make lemonade!', b'Egal wie dicht du bist, Goethe war immer Dichter.', b'Bruce Schneier is always the man in the middle.', b'Bruce Schneier refers to PGP as "Perfectly Good Plaintext"',
        b'Kak propatcit\' KDE2 pod FreeBSD?', b'When the compiler encounters [a given undefined construct] it is legal for it to make demons fly out of your nose', b'There is no free lunch in computer science.', b'2B v ~2B',
        b'Did you know that Vikingskipet was built as the speed skating rink for the 1994 Winter Olympics?', b'According to all known laws of aviation, there is no way a bee should be able to fly.', b'$ curl parrot.live', b'balls'
    ] * 2
    for msg in msgs:
        writer.write(msg + b'\n')
        await writer.drain()

        while True:
            msg = json.loads((await reader.readline()).decode())
            if 'sigma' in msg:
                # TODO: save the signatures, we need them so bad
                break
            msg['id'] = str(id)
            coros = []
            for k, w in writers.items():
                if k == id:
                    continue
                w.write((json.dumps(msg) + '\n').encode())
                coros.append(w.drain())
            await asyncio.gather(*coros)


async def main():
    server = await asyncio.start_server(handle_client, '0.0.0.0', 7070)

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())
