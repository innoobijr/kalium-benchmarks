from nymph.typeclass.api import RestAPI, RestType
from nymph.util.logging.logging import logger
#import requests_cache as requests
import requests
from datetime import timedelta,datetime
from asyncio import Future
import time

# For the QUICKBOOK OAUTHCLIENT
# this can be removed in order to remove the dependency


class ProductCatalogApi(RestAPI):
    session = None
    auth_state = {}
    environment = 'none'

    def __init__(self, interface, configs):
        self.interface = interface
        self.configs = configs
        self.session = requests.Session()
        '''CachedSession(
                configs['cache_id'],
                use_cache_dir=True,
                cache_control=True,
                expire_after=timedelta(days=configs['cache_expiry']),
    ignored_parameters=configs['ignored_parameters'],
                match_headers=True,
                stale_if_error=True
        )'''

    def warm_up(self, *args, **kwargs):
        logger.error("warm_up")
        self.environment = kwargs.get("environment", "development")

    def authenticate(self, *args, **kwargs):
        #refresh = kwargs.get("refresh", False)
        #logger.info(refresh)
        #if (refresh):
        #    uri = '/'.join([self.configs['base'], self.configs['auth_path'], self.auth_state['refresh_token']])
        #    response = self.make_request(RestType.GET, uri=uri, config=self.configs['environment'][self.environment])
        #    self.auth_state = response.json()
       # else:
        #uri = '/'.join([self.configs['base'], self.configs['auth_path']])
        #response = self.make_request(RestType.POST, uri=uri, query=self.configs['creds'], config=self.configs['environment'][self.environment])
        self.auth_state = self.configs['creds']

        return self.auth_state

    def do_GET(self, *args, **kwargs):
        uri = kwargs['uri']
        query =  kwargs.get('query', None)
        header = kwargs.get('header', None)
        config = kwargs['config']

        return self.session.get(uri, params=query, headers=header, **config)

    def do_POST(self, *args, **kwargs):
        uri = kwargs['uri']
        query =  kwargs.get('query', None)
        header = kwargs.get('header', None)
        config = kwargs['config']

        return self.session.post(uri, json=query, headers=header, **config)

    def do_PUT(self, *args, **kwargs):
        uri = kwargs['uri']
        query =  kwargs.get('query', None)
        header = kwargs.get('header', None)
        config = kwargs['config']

        pass

    def do_PATCH(self, *args, **kwargs):
        uri = kwargs['uri']
        query =  kwargs.get('query', None)
        header = kwargs.get('header', None)
        config = kwargs['config']

        pass

    def do_DELETE(self, *args, **kwargs):
        uri = kwargs['uri']
        query =  kwargs.get('query', None)
        header = kwargs.get('header', None)
        config = kwargs['config']
        pass


    """def make_request(self, rtype, **kwargs):
        uri = kwargs['uri']
        query =  kwargs.get('query', None)
        header = kwargs.get('header', None)
        config = kwargs['config']

        try:
            if (rtype == RestType.GET):
                response = self.session.get(uri, params=query, headers=header, **config)
            elif (rtype == RestType.POST):
                response = self.session.post(uri, json=query, headers=header, **config)
            elif (rtype == RestType.PUT): pass
            elif (rtype == RestType.PATCH): pass
            elif (rtype == RestType.DELETE): pass
            else: pss
        except Exception as e:
            raise e

        return response"""

    def is_auth_expired(self, *args, **kwargs):
        logger.error(self.auth_state)
        try:
            logger.error(self.auth_state['access_token_expiration'])
            if (datetime.now() > datetime.fromtimestamp(int(self.auth_state['access_token_expiration']))):
                logger.error(f"Token expired {datetime.now()}")
                return True
            else:
                logger.warning("Token good")
                return False
            return False
        except:
            return True

    def is_refresh_expired(self, *args, **kwargs):
        try:
            if(datetime.now() > datetime.fromtimestamp(int(self.auth_state['refresh_token_expiration']))):
                logger.error("Refresh token expired")
                return True
            else:
                return False
        except:
            return True
