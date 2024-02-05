#import asyncio
import eventlet
import socket
import select
import yaml
import json
from concurrent.futures import ThreadPoolExecutor, wait

from nymph.models.messages import NymphMessageDirection
from nymph.models.components import NymphController
from nymph.models.errors import NymphError, MessageValidationFailed
from nymph.models.auth import AuthType
from nymph.serialization.encoder import encode
from nymph.serialization.decoder import decode
from nymph.serialization.serializer import JsonSerializer


from nymph.storage.db.models import Service
from nymph.storage.db.engine import NymphDB
from nymph.util.helpers import parse_message, read_yaml_conf, validate_message, format_message
from nymph.util.logging.logging import logger

from productcatalogbuilder.extension.productcatalogbuilder import nymph_extension_list
from productcatalogbuilder.models.interface import ProductCatalogBuilder as productcatalogbuilder_if
from cryptography.fernet import Fernet

from eventlet.green import socket

class ProductCatalogBuilder(NymphController):
    service_name = "productcatalogbuilder"
    __if = None

    def __init__(self, host, port, conf_path, threads):
        super().__init__(host, port, conf_path)
        self.threads = threads
        self.conf_path = conf_path
        self.services = []
        #self.serdes = JsonSerializer
        # these would be calls to the agent
        self.db = NymphDB()

    def setup(self):
        self.main_loop=None#asyncio.get_event_loop()
        self.executor = ThreadPoolExecutor(self.threads)
        self.ifconfig = read_yaml_conf(self.conf_path)[self.service_name]
        self.guard = Fernet(self.ifconfig['creds']['tanda-key'].encode('utf-8'))

    def register_service(self):
        self.services = nymph_extension_list

    def bind(self, message):
        if (NymphMessageDirection(message.direction) == NymphMessageDirection.CALL):
            proc = self.services.get(message.procedure, None)
            print(message.args)
            return self.executor.submit(proc, {self.service_name: self.__if}, args=message.args)
        else:
            logger.error("not a call")

    def serve(self):
        server = eventlet.listen(( self.host, self.port))
        pool = eventlet.GreenPool()
        """ server = ThreadedTCPServer((self.host, self.port), ThreadedTCPRequestHandler)
        #server.allow_reuse_address = True
        logger.info(server.allow_reuse_address)
        server.serve_forever()"""
        while True:
            try:
                new_sock, address = server.accept()
                print("accepted", address)
                pool.spawn_n(self.handle, new_sock)
            except (SystemExit, KeyboardInterrupt):
                break

            """server = await asyncio.start_server(self.handle, self.host, self.port)
            async with server:
                await server.serve_forever()"""


    def run(self):
        # First start the interface, if successful
        self.setup()
        self.if_config()
        self.register_service()

        logger.info("configuration successful, starting server")

        self.serve()

    def handle(self, fd):
        #loop = asyncio.get_running_loop()
        #logger.info("EVENT LOOP ID-SERVER: {}".format(asyncio.get_running_loop()._selector))
        reader = fd.makefile('r')
        writer = fd.makefile('w')
        while True:
            msg = ""
            while True:
                try:
                    msg += reader.readline()
                    logger.info(msg)
                    break
                except socket.error as e:
                    msg += reader.readline() #await asyncio.sleep()
                except Exception as e:
                    logger.error(e)
                    break

            msg = self.guard.decrypt(msg.encode('utf-8')).decode('utf-8')
            #logger.warning("Message is: {}".format(msg))

            nmsg = self.serdes.read(msg)
            #logger.warning("Message is: {}".format(nmsg))
            #wip = loop.run_in_executor(None, self.bind, nmsg)
            wip = self.bind(nmsg)
            #wip = await wip
            #logger.warning("Message is: {}".format(wip.token))
            #logger.warning("Message is: {}".format(wip.token))

            #while not wip.token.done():
            #    continue
            fp = wip.result()
            logger.info("something: {}".format(fp))
            completed_work = fp #wip.result()

            res = self.serdes.write(completed_work, False)

            nmsg.direction = 2
            nmsg.data = res

            payload = self.serdes.write(nmsg)
            #logger.info(payload)

            fd.sendall(self.guard.encrypt(payload)+'\n'.encode('utf-8'))
            writer.flush()

            #writer.write_eof()
            fd.close()
            break

    def if_config(self):
        self.__if = productcatalogbuilder_if(AuthType(self.ifconfig['auth_type']), self.ifconfig)
        print(self.ifconfig)
        self.__if.channel.warm_up()
        logger.warning("warsming up")
        with self.db.session() as session:
            service = session.query(Service).filter_by(namespace="productcatalogbuilder")
            print(service.first())
            if( service.first().creds):
                self.__if.channel.auth_state = json.loads(service.first().creds)
                logger.warning("Authsate is: {}".format(self.__if.channel.auth_state))
                """expired = self.__if.channel.is_auth_expired()
                if (expired):
                    refresh_token_expired = self.__if.channel.is_refresh_expired()
                    auth_result = self.__if.channel.authenticate(refresh= not refresh_token_expired)
                    #logger.info(auth_result)
                    service.update({"creds":json.dumps(auth_result)}, synchronize_session="fetch")
                    session.commit()"""
                return True
            else:
                auth_result = self.__if.channel.authenticate()
                service.update({"creds":json.dumps(auth_result)}, synchronize_session="fetch")
                session.commit()
                return True

        return False

    def get_interface(self):
        pass

    def check_interface(self):
        pass

    def close_interface(self):
        pass

    def __del__(self):
        pass
