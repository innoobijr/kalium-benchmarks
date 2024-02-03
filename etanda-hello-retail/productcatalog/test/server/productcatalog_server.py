from productcatalog.models.interface import productcatalog as productcatalog_if
from productcatalog.models.controller import productcatalog as productcatalog_ct
from nymph.models.auth import AuthType
import pickle
import yaml
from yaml import BaseLoader
import asyncio
from productcatalog.extension import productcatalog
from nymph.kleisli.Kleisli import Kleisli
from nymph.models.messages import NymphMessage


if __name__ == "__main__":

    controller = productcatalog_ct(
            host = "127.0.0.1", 
            port = 6666, 
            conf_path = "/Users/innocentobijr/Desktop/ConvergedTechnologyNetworks/sandbox/nymph/conf/services.yml", 
            threads = 5)
    
    asyncio.run(controller.run())
    

