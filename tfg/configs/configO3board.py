from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.components.cachehierarchies.classic.private_l1_shared_l2_cache_hierarchy import (
    PrivateL1SharedL2CacheHierarchy,
)
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator
from components.customO3CPU import *

# Crea el procesador O3
ooo_processor = O3Processor (
    frontend_width = 10,
    backend_width = 12, # = iq_issue_width
    rob_size = 630,
    iq_size = 256,
    lsq_size = 256,
    num_int_phys_regs = 630,
    num_fp_phys_regs = 630,
)

#TODO: cambiar por custom
caches = PrivateL1SharedL2CacheHierarchy(
    l1d_assoc=8,
    l1d_size="32kB",
    l1i_assoc=8,
    l1i_size="32kB",
    l2_assoc=16,
    l2_size="1MB",
)

#TODO: cambiar por custom
main_memory = SingleChannelDDR4_2400(size="2GB")

# Creo la placa TODO: revisar si usar SimpleBoard o X86Board
board = SimpleBoard(
    clk_freq="3GHz",
    processor=ooo_processor,
    memory=main_memory,
    cache_hierarchy=caches,
)

# Asigno programa a ejecutar y lanzo la simulacion
workload = obtain_resource("x86-npb-is-size-s-run")
board.set_workload(workload=workload)
simulator = Simulator(board=board, full_system=False)
print("Empezando simulacion!")
simulator.run()
print("Terminada la simulacion!")