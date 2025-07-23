#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <string.h>
#include <sys/random.h>

#define MAX_DEPTH 5
#define PATTERN_LEN 1  /* 4 bits = 1 nibble = stored in 1 byte */

/*
 * Exam skeleton for the hexentropy tree generator.
 * Fill in the missing pieces to reproduce the behaviour
 * of hexentropy_tree.c.
 */

/* Context structure passed to each thread */
typedef struct {
    int depth;             /* current recursion depth */
    int length;            /* number of bytes to process */
    unsigned char *buffer; /* shared output buffer */
    int offset;            /* starting index in buffer */
} ThreadContext;

/* TODO: implement a real entropy-based coin flip using getrandom */
int flip_coin() {
    return 0; /* placeholder */
}

/* TODO: spawn two worker threads that split the buffer recursively */
void *binary_mutant_worker(void *arg) {
    /* placeholder: you are expected to handle the base case and the
     * recursive case here. */
    (void)arg; /* silence unused parameter warning */
    return NULL;
}

/* TODO: allocate the root buffer, start the first worker and
 * print the resulting bytes in hexadecimal form. */
int main() {
    return 0; /* placeholder */
}
