# Importa la libreria y todos los SimObjects
# TODO: Juntar esto con el basic 
import m5
from m5.objects import *
from components.customO3CPU import *
from components.customCaches import *
from gem5.resources.resource import obtain_resource

# Creo el sistema
system = System()

# Crea la CPU out of order
system.cpu = O3Processor(
    frontend_width = 10,
    backend_width = 12, # = iq_issue_width
    rob_size = 630,
    iq_size = 256,
    lsq_size = 256,
    num_int_phys_regs = 630,
    num_fp_phys_regs = 630,
)

# Frecuencia del reloj del sistema
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "3GHz"
system.clk_domain.voltage_domain = VoltageDomain()

# Crea la jeraquia de caches y las conecta
system.cpu.l1d = L1DCache()
system.cpu.l1i = L1ICache()
system.l1_to_l2 = L2XBar()
system.l2cache = L2Cache()
system.membus = SystemXBar()
system.cpu.l1d.connectCPU(system.cpu.cores[0].core)
system.cpu.l1d.connectBus(system.l1_to_l2)
system.cpu.l1i.connectCPU(system.cpu.cores[0].core)
system.cpu.l1i.connectBus(system.l1_to_l2)
system.l2cache.connectCPUSideBus(system.l1_to_l2)
system.l2cache.connectMemSideBus(system.membus)


system.system_port = system.membus.cpu_side_ports

# Crea el controlador de memoria y lo conecta al bus de memoria
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR4_2400_8x8()
#TODO: system.mem_ctrl.dram.num_channels = 2
#system.mem_ctrl.dram.size = "2GB"
#system.mem_ctrl.port = system.membus.mem_side_ports
#system.system_port = system.membus.cpu_side_ports

# Asigna el proceso a ejecutar
workload = obtain_resource("x86-npb-is-size-s-run")
#system.workload = SEWorkload.init_compatible(workload)

process = Process()
process.cmd = [workload]
system.cpu.cores[0].core.workload = process
system.cpu.cores[0].core.createThreads()

# Instancia el sistema y comienza la ejecucion
root = Root(full_system=False, system=system)
m5.instantiate()

print("Empezando simulacion!")
exit_event = m5.simulate()
print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")
print("Terminada la simulacion!")