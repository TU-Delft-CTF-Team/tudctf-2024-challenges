#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void print_menu() {
    puts("Hi and welcome to one of TU Delft's printer rooms!");
    puts("Please identify yourself with one of the following options:");
    puts("1. Enter your campus card number");
    puts("2. Enter your initials");
    puts("3. Scan your campus card");
    puts("4. Leave");
    printf("> ");
}

void employee_printing() {
    char content[2000];
    puts("We will be printing in colour, and determine the amount of sheets on your input.");
    printf("Please enter all of the content you would like to print: ");
    fgets(content, 2000, stdin);
    puts("Here is your preview:");
    printf(content);
    printf("Printing will commence now.\n[ ");
    for (int i = 0; i < 5; i++) {
        printf(".");
        sleep(1);
    }
    puts(" ]\nThank you for printing today, hope everything was to your liking!");
}

int main() {
    setbuf(stdout, 0);
    setbuf(stdin, NULL);

    char initials[10];
    long unsigned cardnr;
    int choice = 0;
    char *usertype = malloc(1);
    *usertype = 'S';

    while (1) {
        print_menu();
        scanf("%d", &choice);
        getchar();
        switch (choice) {
        case 1:
            puts("Enter the number on the front of your campus card please.");
            printf("> ");
            scanf("%lu", &cardnr);
            getchar();
            for (int i = 0; i < 3; i++) {
                printf(".");
                sleep(1);
            }
            if (*usertype == 'E') {
                puts("It appears that you are an employee, enjoy superior printing services");
                employee_printing();
            } else {
                putchar('\n');
                printf("Thank you. According to my database, campus card number %lu belongs to an student.\n", cardnr);
                puts("You get one free sheet of paper. Draw something fun on it :)");
            }
            exit(0);
            break;
        case 2:
            printf("Please enter your initials: ");
            fgets(initials, 10, stdin);
            printf("\nNice to meet you, ");
            printf(initials);
            puts("\nI'm unsure how you want me to identify you with only your initials, but I hope you have a great day...\n");
            break;
        case 3:
            puts("How would this even work? Try another option\n");
            break;
        case 4:
            puts("Who even needs paper right?? We have computers these days...");
            exit(1);
            break;
        default:
            puts("Invalid choice, kicking you out...");
            exit(2);
            break;
        }
    }

    return 0;
}