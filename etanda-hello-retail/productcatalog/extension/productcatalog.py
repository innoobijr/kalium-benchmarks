import sys

from nymph.models.errors import DependencyNotPresent
from nymph.util.fp import compose
from nymph.util.asserts import CHECK_DEPENDENCY
from nymph.typeclass.api import RestType
from nymph.dataclass.result import Result, ResultType
from nymph.annotations.decorators import nymph
from productcatalog.models.core import core


# this is a great addition when teh language capabilities are ready
# signature = "Sequence[NymphDependencyMap, str, int] -> Sequence[Sequence[AnyVar]]"

nymph_service_name = "productcatalog"
nymph_service_version = "1"

#@nymph.extension( service = nymph_service_name, version = nymph_service_version )
#@nymph.signature(in : "Void" , "out" : f"Collection[{nymph_service_name}.Plan]")
@nymph.resultify
@nymph.signature(input="Void", output= f"nymph.Collection[{nymph_service_name}.{core.Categories.type}]")
def get_categories(dep, **kwargs):
    productcatalog = CHECK_DEPENDENCY(dep, nymph_service_name, "get_categories")
    """if not peeringdb:
        raise Nymph.DEPENDENCY_NOT_PRESENT

     if not CHECK_SIGNATURE():
         raise Nymph.SIGNATURE_NO_MATCH
    """
    ##########
    endpoint = lambda : "categories"
    args = kwargs['args']
    do_rest_call = productcatalog.send_authorized_request(endpoint=endpoint, rtype=RestType.GET, streaming=True)
    res = do_rest_call(args).json()
    return res


@nymph.resultify
@nymph.signature(input="Void", output= f"nymph.Collection[{nymph_service_name}.{core.Products.type}]")
def get_products(dep, **kwargs):
    productcatalog = CHECK_DEPENDENCY(dep, nymph_service_name, "get_categories")
    """if not peeringdb:
        raise Nymph.DEPENDENCY_NOT_PRESENT

     if not CHECK_SIGNATURE():
         raise Nymph.SIGNATURE_NO_MATCH
    """
    ##########
    endpoint = lambda : "products"
    args = kwargs['args']
    do_rest_call = productcatalog.send_authorized_request(endpoint=endpoint, rtype=RestType.GET, streaming=True)
    res = do_rest_call(args).json()
    return res



nymph_extension_list = {
    "get_products" : get_products,
    "get_categories" : get_categories
}
