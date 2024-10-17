# Import the m5 library and all of the SimObjects
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
system.cpu = X86TimingSimpleCPU()

# Create the system-wide memory bus
system.membus = SystemXBar()

# Connect the cahce ports on the CPU to the memory bus
# Resquest port = Response port (or even array of ports). And the connection is made
system.cpu.icache_port = system.membus.cpu_side_ports
system.cpu.dcache_port = system.membus.cpu_side_ports

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
binary = "tests/test-progs/hello/bin/x86/linux/hello"
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
