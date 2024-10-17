from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.private_l1_shared_l2_cache_hierarchy import (
    PrivateL1SharedL2CacheHierarchy,
)
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator

# Create the memory, caches and processor
main_memory = SingleChannelDDR4_2400(size="2GiB")

caches = PrivateL1SharedL2CacheHierarchy(
    l1d_assoc=8,
    l1d_size="32kB",
    l1i_assoc=8,
    l1i_size="32kB",
    l2_assoc=16,
    l2_size="1MB",
)

simple_in_order_cpu = SimpleProcessor(
    cpu_type=CPUTypes.TIMING, num_cores=1, isa=ISA.X86
)

# Plug the components into the board
board = SimpleBoard(
    processor=simple_in_order_cpu,
    memory=main_memory,
    cache_hierarchy=caches,
    clk_freq="3GHz",
)

# Set the workload and run the simulation
board.set_workload(obtain_resource("x86-npb-is-size-s-run"))

simulator = Simulator(board=board)
simulator.run()
