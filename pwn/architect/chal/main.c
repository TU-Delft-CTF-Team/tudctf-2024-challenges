#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <linux/bpf.h>
#include <linux/filter.h>
#include <linux/seccomp.h>
#include <stddef.h>
#include <sys/prctl.h>
#include <asm/unistd_64.h>
#include <asm-generic/errno-base.h>
#include <string.h>

typedef struct message {
    char* message;
    int length;
    struct message* next;
} message_t;
message_t* head = NULL;

void debug_info();
void get_input();
void leave_message();
void read_message();
void print_message(message_t* message);
void exit_program();

static int install_filter(int nr){
    struct sock_filter filter[] = {
            BPF_STMT(BPF_LD + BPF_W + BPF_ABS, (offsetof(struct seccomp_data, nr))),
            BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_K, nr, 0, 1),
            BPF_STMT(BPF_RET + BPF_K, SECCOMP_RET_ERRNO | (EPERM & SECCOMP_RET_DATA)),
            BPF_STMT(BPF_RET + BPF_K, SECCOMP_RET_ALLOW),
    };
    struct sock_fprog prog = {
            .len = (unsigned short)(sizeof(filter) / sizeof(filter[0])),
            .filter = filter,
    };
    if (prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0)) {
        perror("prctl(PR_SET_NO_NEW_PRIVS)");
        return 1;
    }
    if (prctl(PR_SET_SECCOMP, 2, &prog)) {
        perror("prctl(PR_SET_SECCOMP)");
        return 1;
    }
    return 0;
}

void install_filters(){
    int allowed_nr = 9;
    int allowed_syscalls[] = {__NR_getuid, __NR_read, __NR_write, __NR_exit_group, __NR_fstat, __NR_getrandom, __NR_brk, __NR_mmap, __NR_prctl};
    for(int i = 0; i < __NR_process_mrelease; i++){
        int allowed = 0;
        for(int j = 0; j < allowed_nr; j++){
            if(i == allowed_syscalls[j]){
                allowed = 1;
                break;
            }
        }
        if(!allowed){
            int res = install_filter(i);
            if(res) {
                puts("Failed to install filter");
                exit(1);
            }
        }
    }
    install_filter(__NR_prctl); // install last
}

void main(void){
    setvbuf(stdout, NULL, _IONBF, 0); // Makes stdout unbuffered to avoid issues with printing. Just for convenience, not part of the challenge.
    puts("Welcome to the architect association's internal message board");
    debug_info();
    install_filters();
    while(1){
    	get_input();
    }
}

void debug_info(){
    uid_t uid = getuid();
    puts("---Debug info---");
    printf("User id: %d\n", uid);
    printf("Current location: %p\n", &uid);
}

void get_input(){
    puts("----------------");
    puts("Please select an option:");
    puts("1. Leave a message");
    puts("2. Read message");
    puts("3. Exit");
    puts("----------------");
    printf("Choice: ");
    char choice[4];
    fgets(choice, 4, stdin);
    switch(choice[0]){
        case '1':
            leave_message();
            break;
        case '2':
            read_message();
            break;
        case '3':
            exit_program();
            break;
        default:
            puts("Invalid choice");
            break;
    }
}

void leave_message(){
    // get message length
    printf("Message length: ");
    char length[4];
    fgets(length, 4, stdin);
    long len = strtol(length, NULL, 10);
    len += 1; // add space for null byte

    // get message
    printf("Enter your message: ");
    char* message = malloc(len);
    fread(message, 1, len, stdin);
    puts("Message saved!");
    printf("Unique identifier: %p\n", message);

    // add message to linked list
    message_t* new_message = malloc(sizeof(message_t));
    new_message->message = message;
    new_message->length = len;
    new_message->next = head;
    head = new_message;
}

void read_message(){
    // get message address
    printf("Enter the unique identifier of the message you want to read: ");
    char buf[16];
    fgets(buf, 16, stdin);
    char* ptr;
    sscanf(buf, "%p", &ptr);

    // find message in linked list
    message_t* current = head;
    while(current != NULL){
        if(current->message == ptr){
            break;
        }
        current = current->next;
    }
    if(current == NULL){
        puts("Message not found!");
        return;
    }

    // print message
    print_message(current);
}

void print_message(message_t* message){
    char buffer[128];
    memcpy(buffer, message->message, message->length);
    printf("Message: %s\n", buffer);
}

void exit_program(){
    puts("Goodbye!");
    exit(0);
}
