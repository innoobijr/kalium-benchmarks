import requests_cache as requests
import csv
import itertools
import json
from datetime import datetime
from functools import partial
from datetime import timedelta

from nymph.models.components import NymphInterface
from nymph.typeclass.api import RestType
from nymph.util.fp import compose

from nymph.models.auth import AuthType, AdminAuthType
from nymph.util.logging.logging import logger
from productcatalog.models.channel import ProductCatalogApi

class ProductCatalog(NymphInterface):

    session = None

    def __init__(self, auth_type, config):
        super().__init__(auth_type, config)
        self.channel = ProductCatalogApi(self, config)
        self.auth_type = auth_type

        # Match on the authentication types
    #**************************************************************
    #|        Configuration Management for ProductCatalog Controller      |
    #**************************************************************

    def send_authorized_request(self, **kwargs):
        return partial(self.__send_authorized_request,\
                        endpoint = kwargs['endpoint'], \
                        rtype = kwargs.get("rtype", RestType.GET), \
                        ctype = kwargs.get("ctype", "application/json"), \
                        streaming = kwargs.get('streaming', False))

    def __send_authorized_request(self, query, endpoint, rtype=RestType.GET, ctype="application/json", streaming=False):
        result = None
        config = self.config['environment'][self.channel.environment]
        if (streaming):
            config['stream'] = True

        logger.warn(f"API Key is: {self.channel.auth_state['api-key']}") ## TODO: get the states

        header = {
                "Access-Control-Allow-Origin": '*',
                'Access-Control-Allow-Credentials': True,
                "Authorization": "Api-Key {}".format(self.channel.auth_state['api-key']),
                "Accept": f"{ctype}"}

        uri = '/'.join([self.config['base'], endpoint()])

        response = self.channel.make_request(rtype, uri=uri, query=query, header=header, config=config)
        #logger.error(response)
        return response
