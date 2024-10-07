#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct __attribute__((packed)) input {
    char command[16];
    void* function;
};

void man(char* command) {
    command[strlen(command) - 1] = '\0'; // replace newline with null terminator
    printf("%s is a command that displays the manual page for a given command\n", command);
    printf("To use it, simply type man followed by the command you want to know more about\n");
}

void cat(char* command) {
    command[strlen(command) - 1] = '\0'; // replace newline with null terminator
    printf("%s is a command that concatenates files and prints them to the standard output\n", command);
    printf("It is often used to read files\n");
    printf("To use it, simply type cat followed by the file you want to print\n");
}

void head(char* command) {
    command[strlen(command) - 1] = '\0'; // replace newline with null terminator
    printf("%s is a command that outputs the first part of files\n", command);
    printf("To use it, simply type head followed by the file you want to print\n");
}

void tail(char* command) {
    command[strlen(command) - 1] = '\0'; // replace newline with null terminator
    printf("%s is a command that outputs the last part of files\n", command);
    printf("To use it, simply type tail followed by the file you want to print\n");
}

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0); // disable buffering. This is just so the challenge works with the infrastructure, don't look into it.
    system("echo Starting process...");
    int MAX_COMMAND_LENGTH = 16;
    while(1) {
        struct input input;
        input.function = NULL;
        printf("Welcome to the linux command zoo!\n"
                "What would you like to know about? Your options are:\n"
                "- man\n"
                "- cat\n"
                "- head\n"
                "- tail\n"
                "- (or exit the application with \"exit\")\n"
                "Enter your choice: ");
        MAX_COMMAND_LENGTH += 1; // Bugfix: add 1 for null terminator
        fgets(input.command, MAX_COMMAND_LENGTH, stdin);
        if(strstr(input.command, "man") != NULL) {
            input.function = &man;
        } else if(strstr(input.command, "cat") != NULL) {
            input.function = &cat;
        } else if(strstr(input.command, "head") != NULL) {
            input.function = &head;
        } else if(strstr(input.command, "tail") != NULL) {
            input.function = &tail;
        } else if(strstr(input.command, "exit") != NULL) {
            printf("Goodbye!");
            exit(0);
        } else {
            printf("Invalid choice\n");
        }
        if(input.function != NULL) {
            ((void (*)(char*))input.function)(input.command);
        }
    }
}
