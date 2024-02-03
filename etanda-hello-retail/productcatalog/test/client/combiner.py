from collections import namedtuple
from nymph.models.messages import NymphMessage
from nymph.util.helpers import write_to_controller
from nymph.effects.effects import Effect
from nymph.models.program.Program import Program
from nymph.util.logging.logging import logger
import weakref


def generate_effect():

    prog = Program(None)

    t1 = Effect("t1", [
            NymphMessage(1, 1, "splynx", "get_list_of_plans"),
            NymphMessage(1, 1, "splynx", "get_list_of_customers")
            ], program=weakref.proxy(prog))

    t3 =  Effect("t3", NymphMessage(1,1,"udf", "process_and_write_plans"), \
            program=weakref.proxy(prog))

    t4 =  Effect("t4", NymphMessage(1, 1, "udf", "process_and_write_customers"), \
            program=weakref.proxy(prog))

    """t5 = Effect("t5", NymphMessage(1, 1, "udf", "perform_calculations", args={"version":1}), \
            program=weakref.proxy(prog))

    t6 = Effect("t6", NymphMessage(1, 1, "libreqos", "put_libreqos_files", \
                args= {"file_1": "AccessPoints.csv", "file_2": "Shapers.csv"}), \
                program=weakref.proxy(prog))"""

    # Set the dependencies
    t1 >> [t3, t4]
    #t5 << [t3, t4]
    #t6 << t5

    # the wait to get around this is that have the context assigned all effect to a program.
    # end a program is assigned ot a : prog is actually just
    #effects = [t1, t3, t4, t5, t6]

    #prog = Program(effects)
    prog.create_graph()
    prog.make_call_graph()
    effect_req = None

    if (not prog.is_cyclic()):
        effs_and_order = prog.get_eval_order()
        #effects_mapped = dict(map(lambda x: (x.name,  x), prog.effects))
        effect_req = NymphMessage(4, 1, "nymph", "no-op", data= effs_and_order, eof=True)

    else:
        logger.error("There are cycles in the program")

    return effect_req
