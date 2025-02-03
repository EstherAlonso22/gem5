# Import the m5 library and all of the SimObjects, and the caches
from components.customCaches import *
import m5
from m5.objects import *

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
#TODO: Cambiar a custom O3 CPU
system.cpu = X86TimingSimpleCPU()

# Create the L1 caches and connect them to the CPU
system.cpu.icache = L1ICache()
system.cpu.dcache = L1DCache()

system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

# Create the L2 bus and connect the L1 caches to the L2 cache
system.l2bus = L2XBar()

system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)

# Create the L2 cache and connect it to the L2 bus and memory bus
system.l2cache = L2Cache()
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
binary = "ansibench/coremark/bin/coremark"
system.workload = SEWorkload.init_compatible(binary)

process = Process()
process.cmd = [binary]
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
