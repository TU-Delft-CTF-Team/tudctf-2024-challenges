#include "hello_hardware.hpp"

#include <iostream>
#include "../flagstore/flagstore.hpp"

namespace HelloHardware {

    void entrypoint() {
        std::cout << "\n" << Flagstore::flags[Flagstore::HELLO_HARDWARE] << "\n" << std::endl;
    }

}
