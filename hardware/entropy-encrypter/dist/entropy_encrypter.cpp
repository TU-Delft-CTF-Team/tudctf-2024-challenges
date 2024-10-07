#include <iostream>
#include <cstdlib>
#include <cstring>
#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include "hardware/adc.h"

#include "entropy_encrypter.hpp"
#include "../flagstore/flagstore.hpp"


namespace EntropyEncrypter {

    uint8_t rng_byte() {
        uint8_t res = 0;
        for(int i = 0; i < 8; i++){
            int bit = (adc_read() >> 5) & 1;
            res |= (bit << i);
        }
        return res;
    }
    
    char* keygen(int length) {
        const char* flag = Flagstore::flags[Flagstore::ENTROPY_ENCRYPTER];
        int baselen = std::strlen(flag);
        char* seed = new char[length + 1];
        for(int i = 0; i < length; i++){
            do {
                seed[i] = (flag[i % baselen] ^ rng_byte()) % 127;
            } while (seed[i] < 32);
        }
        
        seed[length] = '\0';
        return seed;
    }

    void init() {
        adc_init();
        adc_gpio_init(26);
        adc_select_input(0);
    }

    void generate(int length) {
        char* password = keygen(length);
        std::cout << "\nNew password: \"" << password << "\"" << std::endl;
        delete[] password;
    } 

}
