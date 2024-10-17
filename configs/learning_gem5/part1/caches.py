# Import the SimObjects we are going to extend: Cache
from m5.objects import Cache


# Create an L1 cache
class L1Cache(Cache):
    assoc = 2  # 2-way set associative
    tag_latency = 2  # 2 cycle tag lookup
    data_latency = 2  # 2 cycle data access
    response_latency = 2  # 2 cycle response time
    mshrs = 4  # 4 miss status handling registers
    tgts_per_mshr = 20  # 20 targets per MSHR

    # Init method or constructor
    def __init__(self, options=None):
        super().__init__()
        pass

    # Helper functions
    def connectCPU(self, cpu):
        raise NotImplementedError

    def connectBus(self, bus):
        self.mem_side = bus.cpu_side_ports


# Subclasses of L1 cache: Instruction and Data caches
class L1ICache(L1Cache):
    size = "16kB"

    def __init__(self, options=None):
        super().__init__(options)
        if not options or not options.l1i_size:
            return
        self.size = options.l1i_size

    def connectCPU(self, cpu):
        self.cpu_side = cpu.icache_port


class L1DCache(L1Cache):
    size = "64kB"

    def __init__(self, options=None):
        super().__init__(options)
        if not options or not options.l1d_size:
            return
        self.size = options.l1d_size

    def connectCPU(self, cpu):
        self.cpu_side = cpu.dcache_port


# Create an L2 cache
class L2Cache(Cache):
    size = "256kB"  # 256kB
    assoc = 8  # 8-way set associative
    tag_latency = 20  # 20 cycle tag lookup
    data_latency = 20  # 20 cycle data access
    response_latency = 20  # 20 cycle response time
    mshrs = 20  # 20 miss status handling registers
    tgts_per_mshr = 12  # 12 targets per MSHR

    def __init__(self, options=None):
        super().__init__()
        if not options or not options.l2_size:
            return
        self.size = options.l2_size

    def connectCPUSideBus(self, bus):
        self.cpu_side = bus.mem_side_ports

    def connectMemSideBus(self, bus):
        self.mem_side = bus.cpu_side_ports
