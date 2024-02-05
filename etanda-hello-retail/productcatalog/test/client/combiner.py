from collections import namedtuple
from nymph.models.messages import NymphMessage
from nymph.util.helpers import write_to_controller
from nymph.fx.effects import Effect
from nymph.models.program.Program import Program
from nymph.util.logging.logging import logger
import weakref
import yaml

def generate_effect(path=None):

    prog = Program(None)
    testProduct = None

    if path:
        with open(path, "r") as f:
            testProduct = yaml.safe_load(f)


    t3 =  Effect("t3", NymphMessage(1,1,"productcatalog", "add_product", \
            args = testProduct),
            program=weakref.proxy(prog))
    """t5 = Effect("t5", NymphMessage(1, 1, "udf", "perform_calculations", args={"version":1}), \
            program=weakref.proxy(prog))

    t6 = Effect("t6", NymphMessage(1, 1, "libreqos", "put_libreqos_files", \
                args= {"file_1": "AccessPoints.csv", "file_2": "Shapers.csv"}), \
                program=weakref.proxy(prog))"""

    # Set the dependencies
    #t1 >> [t3, t4]
    #t5 << [t3, t4]
    #t6 << t5

    # the wait to get around this is that have the context assigned all effect to a program.
    # end a program is assigned ot a : prog is actually just
    #effects = [t1, t3, t4, t5, t6]

    #prog = Program(effects)
    prog.create_graph()
    prog.make_call_graph()
    effect_req = None
    prog.eval_order = prog.graph.is_cyclic()
    effs_and_order = prog.get_effects_order()
    print(effs_and_order)
    effect_req = NymphMessage(4, 1, "nymph", "no-op", data= effs_and_order, eof=True)

    return effect_req
