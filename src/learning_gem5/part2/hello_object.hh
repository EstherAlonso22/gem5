#ifndef __LEARING_GEM5_HELLO_OBJECT_HH__
#define __LEARING_GEM5_HELLO_OBJECT_HH__

#include "params/HelloObject.hh"
#include "sim/sim_object.hh"

namespace gem5
{
    class HelloObject: public SimObject
    {
        public:
            HelloObject(const HelloObjectParams &p);
    };
} //namespace gem5

#endif // __LEARING_GEM5_HELLO_OBJECT_HH__
