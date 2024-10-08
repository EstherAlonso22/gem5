# Import the m5 library and all of the SimObjects, and the caches
# Adding parameters to the script
import argparse

from caches import *

import m5
from m5.objects import *

parser = argparse.ArgumentParser(
    description="A simple system with 2-level cache."
)
parser.add_argument(
    "binary",
    default="tests/test-progs/hello/bin/x86/linux/hello",
    nargs="?",
    type=str,
    help="Path to the binary to execute.",
)
parser.add_argument(
    "--l1i_size", help="L1 instruction cache size. Default: 16kB."
)
parser.add_argument(
    "--l1d_size", help="L1 data cache size. Default: Default: 64kB."
)
parser.add_argument("--l2_size", help="L2 cache size. Default: 256kB.")

options = parser.parse_args()

# Create the system
system = System()

# Set the clock on the system
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "1GHz"
system.clk_domain.voltage_domain = VoltageDomain()

# Use timing mode for the memory simulation
system.mem_mode = "timing"
system.mem_ranges = [AddrRange("512MB")]

# Create a simple CPU - timing based for X86
system.cpu = X86TimingSimpleCPU()

# Create the L1 caches and connect them to the CPU
system.cpu.icache = L1ICache(options)
system.cpu.dcache = L1DCache(options)

system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

# Create the L2 bus and connect the L1 caches to the L2 cache
system.l2bus = L2XBar()

system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)

# Create the L2 cache and connect it to the L2 bus and memory bus
system.l2cache = L2Cache(options)
system.l2cache.connectCPUSideBus(system.l2bus)

system.membus = SystemXBar()
system.l2cache.connectMemSideBus(system.membus)

# Create the interrupt controles and connect the PIO and interrupt ports into the memory bus
# This is specific to X86
system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

system.system_port = system.membus.cpu_side_ports

# Create a memory controller and connect it to the membus
# Simple DDR3 controller for the entire memory range of the system
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

# Create the process and set the command to run and use it as cpu workload
system.workload = SEWorkload.init_compatible(options.binary)

process = Process()
process.cmd = [options.binary]
system.cpu.workload = process
system.cpu.createThreads()

# Instantiate the system and begin execution
root = Root(full_system=False, system=system)
m5.instantiate()

# Run the simulation
print("Empezando simulacion!")
exit_event = m5.simulate()

# Once simulation finishes inspect the state
print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")
