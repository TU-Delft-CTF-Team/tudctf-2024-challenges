#include <stdio.h>
#include <string.h>

int main() {
    char input[16];
    char is_authenticated = 0;
    FILE *file;
    char ch;

    printf("Enter the password: ");
    fflush(stdout);
    fgets(input, 64, stdin);

    if (is_authenticated) {
        file = fopen("flag.txt", "r");
        if (file == NULL) {
            printf("Could not open file flag.txt\n");
            return 1;
        }
        while ((ch = fgetc(file)) != EOF) {
            putchar(ch);
        }
        fclose(file);
    } else {
        printf("Invalid password!\n");
    }

    return 0;
}
