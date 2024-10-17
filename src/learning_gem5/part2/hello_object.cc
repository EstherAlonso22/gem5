#include "learning_gem5/part2/hello_object.hh"
#include "base/trace.hh"
#include "debug/HelloExample.hh"

namespace gem5
{
    HelloObject::HelloObject(const HelloObjectParams &params) :
        SimObject(params)
    {
        DPRINTF(HelloExample, "Hola mundo! Desde un SimObject!\n");
    }
}
