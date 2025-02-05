from productcatalogbuilder.models.interface import ProductCatalogBuilder as productcatalogbuilder_if
from productcatalogbuilder.models.controller import ProductCatalogBuilder as productcatalogbuilder_ct
from nymph.models.auth import AuthType
import pickle
import yaml
from yaml import BaseLoader
import asyncio
from productcatalogbuilder.extension import productcatalogbuilder
from nymph.kleisli.Kleisli import Kleisli
from nymph.models.messages import NymphMessage


if __name__ == "__main__":

    controller = productcatalogbuilder_ct(
            host = "127.0.0.1", 
            port = 6690, 
            conf_path = "/home/etanda/nymph/conf/services.yml", 
            threads = 5)
    
    asyncio.run(controller.run())
    

