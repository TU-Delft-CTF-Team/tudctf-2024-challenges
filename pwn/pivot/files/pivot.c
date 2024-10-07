#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>

void win() {
    char flag[100] = {0};
    FILE *fd = fopen("flag.txt", "r");
    fgets(flag, 100, fd);
    puts(flag);
    exit(0);
}

int read_answer() {
    char answer[16];
    read(STDIN_FILENO, answer, 18);

    if (strncmp(answer, "PIVOOOOOOOT!!", 13) == 0) {
        puts("Yes!! Thank you...");
        return 1;
    } else {
        puts("drops couch...");
        return 0;
    }
}

int main() {
    setbuf(stdout, 0);
    setbuf(stdout, 0);

    int correct = 0;
    printf("Tell me Ross, we're at a %10$hu degree angle, what should we do?\n> ");
    correct = read_answer();
    return correct;
}