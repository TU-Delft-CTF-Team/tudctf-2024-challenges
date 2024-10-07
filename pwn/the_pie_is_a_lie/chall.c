#include <stdbool.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <unistd.h>

uint64_t get_answer() {
    return 42L;
}

void shell() {
    system("/bin/sh");
}

int main(void) {
    char name[64];

    setbuf(stdin, NULL);
    setbuf(stdout, NULL);

    while(true) {
        printf("1) Enter your name\n2) Request a pie\n3) Get The Answer to the Ultimate Question of Life, The Universe, and Everything.\n4) Quit\n> ");
        int option;
        scanf("%d", &option);

        if(option == 1) {
            printf("Enter your name: ");
            read(0, name, 0x64);
        } else if(option == 2) {
            printf("A pie for %s has been ordered, surely it will be baked soon.\n", name);
        } else if(option == 3) {
            printf("The Answer to the Ultimate Question of Life, The Universe, and Everything is %lu\n", get_answer);
        } else if(option == 4) {
            break;
        }
    }

    return 0;
}