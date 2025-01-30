# Importa la libreria y todos los SimObjects
import m5
from m5.objects import *
from components.customO3CPU import *
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

# Memoria TODO: cambiar por custom
system.mem_ctrl = DDR4_2400_8x8()
system.mem_ctrl.range = AddrRange("2GB")

# Caches TODO: cambiar por custom
system.cpu.icache = Cache(
    size="32kB",
    assoc=8,
)
system.cpu.dcache = Cache(
    size="32kB",
    assoc=8,
)
system.cpu.l2cache = Cache(
    size="1MB",
    assoc=16,
)

# Conectar caches
# TODO: Buscar como 

# Asigna el proceso a ejecutar
workload = obtain_resource("x86-npb-is-size-s-run")
system.workload = SEWorkload.init_compatible(workload)

process = Process()
process.cmd = [workload]
system.cpu.workload = process
system.cpu.createThreads()

# Instancia el sistema y comienza la ejecucion
root = Root(full_system=False, system=system)
m5.instantiate()

print("Empezando simulacion!")
exit_event = m5.simulate()
print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")
print("Terminada la simulacion!")