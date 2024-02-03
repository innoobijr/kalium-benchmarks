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

@nymph.resultify
@nymph.signature(input="Void", output= f"nymph.Collection[{nymph_service_name}.{core.Product.type}]")
def add_product(dep, **kwargs):
    productcatalog = CHECK_DEPENDENCY(dep, nymph_service_name, "add_product")
    """if not peeringdb:
        raise Nymph.DEPENDENCY_NOT_PRESENT

     if not CHECK_SIGNATURE():
         raise Nymph.SIGNATURE_NO_MATCH
    """
    ##########
    endpoint = lambda : "product"
    args = kwargs['args']
    do_rest_call = productcatalog.send_authorized_request(endpoint=endpoint, rtype=RestType.POST, streaming=True)
    res = do_rest_call(args).json()
    return res

nymph_extension_list = {
    "add_product" : add_product
}
