import m5
from m5.objects import *

# instantiate the root object
root = Root(full_system=False)

# Instantiate the hello object
root.hello = HelloObject()

# Call instantiate on the m5 module and run the simulation
m5.instantiate()

print("Beginning simulation!")
exit_event = m5.simulate()
print(
    f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}"
)
