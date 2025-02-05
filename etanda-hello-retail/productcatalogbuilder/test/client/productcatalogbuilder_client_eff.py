import socket
import argparse
import json
from cryptography.fernet import Fernet
import asyncio
from asyncio import LimitOverrunError
from nymph.models.messages import NymphMessage, NymphMessageCodec
from combiner import generate_effect

from nymph.serialization.encoder import encode
from nymph.util.logging.logging import logger

KEY="w_mx_mmQf0SJ21uwM9GWbFzGyk5De19meUM3ysfENh8=".encode('utf-8')

async def do_in_main(f, args):
    codec = NymphMessageCodec()
    res = None

    effect_req = generate_effect(args.file)
    effect_req.args = {"client_id": "Innocent"}
    data = json.dumps(encode(effect_req))
    logger.info(data)

    reader, writer = await asyncio.open_connection(args.host, args.port)
    writer.write(f.encrypt(data.encode()) + "\n".encode("utf-8"))
    await writer.drain()

    msg = bytes()
    while True:
        try:
            logger.info("Reading")
            msg += await reader.readuntil()
            #logger.info(str(msg))
            break
        except LimitOverrunError as e:
            msg += await reader.read(2048)
            #logger.info(str(msg))
        except Exception as e:
            logger.error(e)
            break

    msg = f.decrypt(msg).decode("utf-8")
    res = json.loads(msg)
    #with open("/Users/innocentobijr/dev/sw-security-practices/data-collection/test.json", 'w') as file:
    #    file.write(json.dumps(res))

    logger.warning(msg)

if __name__ == "__main__":
    f = Fernet(KEY)
    parser = argparse.ArgumentParser(description='Nymph client')
    parser.add_argument("--host", action="store", type=str)
    parser.add_argument("--port", action="store", type=int)
    parser.add_argument("--file", action="store", type=str)


    args = parser.parse_args()
    asyncio.run(do_in_main(f, args))

    #print(res)
