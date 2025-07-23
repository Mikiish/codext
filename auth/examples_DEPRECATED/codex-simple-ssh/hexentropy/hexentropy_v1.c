#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <sys/random.h>
#include <string.h>

// Context passed to each thread
typedef struct {
    unsigned char *buffer;  // pointer to buffer region
    size_t length;          // bytes to generate
    int depth;              // recursion depth
} WorkerCtx;

#define MAX_DEPTH 4      // limit recursion to avoid CPU explosion
#define SMALL_CHUNK 32   // below this, just fill sequentially

// Return a random nibble, either 0x07 or 0x08
static unsigned char rand_hexbit() {
    unsigned char b;
    if (getrandom(&b, 1, 0) != 1) {
        perror("getrandom");
        exit(EXIT_FAILURE);
    }
    return (b & 1) ? 0x08 : 0x07;
}

// Fill buffer with random bytes
static void fill_random(unsigned char *buf, size_t len) {
    if (getrandom(buf, len, 0) != (ssize_t)len) {
        perror("getrandom");
        exit(EXIT_FAILURE);
    }
}

// Recursive worker implementing the described strategy
static void *hexentropy_worker(void *arg) {
    WorkerCtx ctx = *(WorkerCtx *)arg; // copy context

    if (ctx.length == 0)
        return NULL;

    // Base case: small chunk or depth limit
    if (ctx.length <= SMALL_CHUNK || ctx.depth >= MAX_DEPTH) {
        fill_random(ctx.buffer, ctx.length);
        return NULL;
    }

    pthread_t t1, t2;
    size_t half;

    if (ctx.length % 2 == 0) {
        // Even length: split evenly and recurse on both halves
        half = ctx.length / 2;

        WorkerCtx *left = malloc(sizeof(WorkerCtx));
        WorkerCtx *right = malloc(sizeof(WorkerCtx));
        if (!left || !right) {
            perror("malloc");
            free(left); free(right);
            exit(EXIT_FAILURE);
        }
        *left = (WorkerCtx){ ctx.buffer, half, ctx.depth + 1 };
        *right = (WorkerCtx){ ctx.buffer + half, half, ctx.depth + 1 };
        pthread_create(&t1, NULL, hexentropy_worker, left);
        pthread_create(&t2, NULL, hexentropy_worker, right);
        pthread_join(t1, NULL);
        pthread_join(t2, NULL);
        free(left);
        free(right);
        return NULL;
    } else {
        // Odd length: insert one random nibble then recurse on each half
        half = (ctx.length - 1) / 2;
        ctx.buffer[half] = rand_hexbit();

        WorkerCtx *left = malloc(sizeof(WorkerCtx));
        WorkerCtx *right = malloc(sizeof(WorkerCtx));
        if (!left || !right) {
            perror("malloc");
            free(left); free(right);
            exit(EXIT_FAILURE);
        }
        *left = (WorkerCtx){ ctx.buffer, half, ctx.depth + 1 };
        *right = (WorkerCtx){ ctx.buffer + half + 1, half, ctx.depth + 1 };
        pthread_create(&t1, NULL, hexentropy_worker, left);
        pthread_create(&t2, NULL, hexentropy_worker, right);
        pthread_join(t1, NULL);
        pthread_join(t2, NULL);
        free(left);
        free(right);
        return NULL;
    }

}

int main(int argc, char *argv[]) {
    size_t n = 64; // default length
    if (argc > 1) {
        n = strtoul(argv[1], NULL, 10);
        if (n == 0) {
            fprintf(stderr, "Invalid length\n");
            return EXIT_FAILURE;
        }
    }

    unsigned char *buffer = malloc(n);
    if (!buffer) {
        perror("malloc");
        return EXIT_FAILURE;
    }

    WorkerCtx root = { buffer, n, 0 };
    hexentropy_worker(&root);

    for (size_t i = 0; i < n; ++i)
        printf("%02x", buffer[i]);
    printf("\n");

    free(buffer);
    return 0;
}
