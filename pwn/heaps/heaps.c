#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    uint64_t* heap;
    uint64_t size;
    uint64_t free_slots;
} heap_t;

#define NUM_HEAPS 12

heap_t heaps[NUM_HEAPS] = { { .heap = NULL, .size = 0, .free_slots = 0 } };

int find_free_index() {
    for(int i = 0; i < NUM_HEAPS; i++) {
        if(heaps[i].heap == NULL) {
            return i;
        }
    }

    return -1;
}

void create() {
    int idx = find_free_index();
    if(idx == -1) {
        puts("There's no place for a new heap! Delete one of the old heaps first.");
        return;
    }

    printf("Size? ");
    int size;
    scanf("%d", &size);
    if(size < 0 || size > 20) {
        puts("Invalid size!");
        return;
    }

    heaps[idx] = (heap_t){
        .heap = malloc(8 * size),
        .size = size,
        .free_slots = size
    };

    printf("Successfully created a new heap at index %d\n", idx);
}

void delete() {
    printf("Index? ");
    int idx;
    scanf("%d", &idx);

    if(idx < 0 || idx > NUM_HEAPS - 1) {
        puts("Invalid index!");
        return;
    }

    if(heaps[idx].heap == NULL) {
        printf("No heap exists at index %d!\n", idx);
        return;
    }

    free(heaps[idx].heap);
    heaps[idx].free_slots = 0;

    printf("Successfully freed heap at index %d\n", idx);
}

void push(heap_t* heap, uint64_t value) {
    int idx = heap->size - heap->free_slots;
    heap->free_slots--;
    uint64_t* a = heap->heap;
    uint64_t tmp;
    a[idx] = value;
    while(idx > 0 && a[(idx - 1) >> 1] > a[idx]) {
        tmp = a[(idx - 1) >> 1];
        a[(idx - 1) >> 1] = a[idx];
        a[idx] = tmp;
        idx = (idx - 1) >> 1;
    }
}

uint64_t peek(heap_t* heap) {
    return heap->heap[0];
}

uint64_t pop(heap_t* heap) {
    heap->free_slots++;
    uint64_t max_idx = heap->size - heap->free_slots;
    uint64_t* a = heap->heap;
    uint64_t result = a[0];
    a[0] = a[max_idx];
    uint64_t idx = 0;

    while((idx << 1) + 1 < max_idx) {
        uint64_t min_idx = ((idx << 1) + 1);

        if(min_idx + 1 < max_idx && a[min_idx + 1] < a[min_idx]) {
            min_idx++;
        }

        if(a[min_idx] < a[idx]) {
            uint64_t tmp = a[idx];
            a[idx] = a[min_idx];
            a[min_idx] = tmp;
            idx = min_idx;
        } else {
            break;
        }
    }

    return result;
}

int main(void) {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);

    while(true) {
        int choice;
        printf("What do you want to do?\n1) Create a new heap\n2) Delete a heap\n3) Add an element to a heap\n4) Remove the smallest element from a heap\n5) Peek at the smallest element of a heap\n6) Quit\n> ");
        scanf("%d", &choice);

        if(choice == 1) {
            create();
        } else if(choice == 2) {
            delete();
        } else if(choice == 3) {
            printf("Index? ");
            int idx;
            scanf("%d", &idx);
            if(idx < 0 || idx > NUM_HEAPS - 1 || heaps[idx].heap == NULL) {
                puts("Invalid index!");
                continue;
            }
            heap_t* heap = &heaps[idx];
            if(heap->free_slots == 0) {
                puts("This heap has no free slots!");
                continue;
            }
            printf("Value? ");
            uint64_t value;
            scanf("%lu", &value);
            push(heap, value);
        } else if(choice == 4) {
            printf("Index? ");
            int idx;
            scanf("%d", &idx);
            if(idx < 0 || idx > NUM_HEAPS - 1 || heaps[idx].heap == NULL) {
                puts("Invalid index!");
                continue;
            }
            heap_t* heap = &heaps[idx];
            if(heap->free_slots == heap->size) {
                puts("There are no elements on the heap!");
                continue;
            }
            uint64_t result = pop(heap);
            printf("The smallest value on heap %d was %lu\n", idx, result);
        } else if(choice == 5) {
            printf("Index? ");
            int idx;
            scanf("%d", &idx);
            if(idx < 0 || idx > NUM_HEAPS - 1 || heaps[idx].heap == NULL) {
                puts("Invalid index!");
                continue;
            }
            heap_t* heap = &heaps[idx];
            if(heap->free_slots == heap->size) {
                puts("There are no elements on the heap!");
                continue;
            }
            uint64_t result = peek(heap);
            printf("The smallest value on heap %d is %lu\n", idx, result);
        } else if(choice == 6) {
            puts("Bye!");
            break;
        } else {
            puts("Invalid option!");
        }
    }
    return 0;
}
