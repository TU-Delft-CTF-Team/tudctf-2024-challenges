#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void print_flag() __attribute__ ((section (".secret")));

void print_flag() {
    char flag[100] = {0};
    FILE *fd = fopen("flag.txt", "r");
    fgets(flag, 100, fd);
    puts(flag);
    exit(0);
}

int main() {
    setbuf(stdin, 0);
    setbuf(stdout, 0);
    
    char pool[32];
    float fill_rate;
    puts("You have been hired to fill up the pool in the ME building, but you can fill it with whatever you want.");
    printf("What would you like to fill it with?\n> ");
    gets(pool);

    fill_rate = strlen(pool)*100/32;
    printf("\nAround %0.0f percent of the pool has been filled. ", fill_rate);
    if (fill_rate > 100) {
        puts("That's an overflow!!");
    } else {
        puts("Thanks for helping out");
    }
}
