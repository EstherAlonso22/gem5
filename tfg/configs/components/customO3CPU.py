from m5.objects import X86O3CPU
from m5.objects import TournamentBP
from gem5.components.processors.base_cpu_core import BaseCPUCore
from gem5.components.processors.base_cpu_processor import BaseCPUProcessor
from gem5.isas import ISA

# O3Core extiende X86O3CPU. X86O3CPU es uno de los modelos internos de gem5 que implementa
# un pipeline fuera de orden para la arquitectura x86.
class O3Core(X86O3CPU):
    def __init__(self, frontend_width, backend_width, rob_size, iq_size, lsq_size, num_int_phys_regs, num_fp_phys_regs):
        """
        :param TODO: def params.
        """
        super().__init__()
        self.fetchWidth = frontend_width
        self.decodeWidth = frontend_width
        self.renameWidth = frontend_width
        self.issueWidth = backend_width
        self.dispatchWidth = backend_width
        self.commitWidth = backend_width
        self.wbWidth = backend_width
        
        self.numROBEntries = rob_size
        self.numIQEntries = iq_size
        self.LQEntries = lsq_size
        self.SQEntries = lsq_size

        self.numPhysIntRegs = num_int_phys_regs
        self.numPhysFloatRegs = num_fp_phys_regs

        #TODO: cambiar bp
        self.branchPred = TournamentBP()


# O3StdCore hace wrap de O3CPUCore a un core compatible con la libreria estandar de gem5.
class O3StdCore(BaseCPUCore):
    def __init__(self, frontend_width, backend_width, rob_size, iq_size, lsq_size, num_int_phys_regs, num_fp_phys_regs):
        core = O3Core(frontend_width, backend_width, rob_size, iq_size, lsq_size, num_int_phys_regs, num_fp_phys_regs)
        super().__init__(core, ISA.X86)

# O3Processor, junto con BaseCPUProcessor, hace wrap de O3Core a un procesador compatible con la libreria estandar de gem5.
class O3Processor(BaseCPUProcessor):
    def __init__(self, frontend_width, backend_width, rob_size, iq_size, lsq_size, num_int_phys_regs, num_fp_phys_regs):
        cores = [O3StdCore(frontend_width, backend_width, rob_size, iq_size, lsq_size, num_int_phys_regs, num_fp_phys_regs)]
        super().__init__(cores)
        