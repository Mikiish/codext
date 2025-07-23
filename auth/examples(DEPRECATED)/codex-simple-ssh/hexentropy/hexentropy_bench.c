#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <sys/random.h>
#include <string.h>
#include <time.h>

// === CONFIGURATION ===
#define ITERATIONS 10000
#define ENTROPY_SIZE 1031  // bytes
#define MAX_DEPTH 8
#define SMALL_CHUNK 32

typedef struct {
    unsigned char *buffer;
    size_t length;
    int depth;
} WorkerCtx;

static unsigned char rand_hexbit() {
    unsigned char b;
    if (getrandom(&b, 1, 0) != 1) {
        perror("getrandom");
        exit(EXIT_FAILURE);
    }
    return (b & 1) ? 0x08 : 0x07;
}

static void fill_random(unsigned char *buf, size_t len) {
    if (getrandom(buf, len, 0) != (ssize_t)len) {
        perror("getrandom");
        exit(EXIT_FAILURE);
    }
}

static void *hexentropy_worker(void *arg) {
    WorkerCtx ctx = *(WorkerCtx *)arg;

    if (ctx.length <= SMALL_CHUNK || ctx.depth >= MAX_DEPTH) {
        fill_random(ctx.buffer, ctx.length);
        return NULL;
    }

    pthread_t t1, t2;
    size_t mid;

    if (ctx.length % 2 == 0) {
        size_t half = ctx.length / 2;
        WorkerCtx left = { ctx.buffer, half, ctx.depth + 1 };
        WorkerCtx right = { ctx.buffer + half, half, ctx.depth + 1 };

        pthread_create(&t1, NULL, hexentropy_worker, &left);
        pthread_create(&t2, NULL, hexentropy_worker, &right);
        pthread_join(t1, NULL);
        pthread_join(t2, NULL);
    } else {
        mid = ctx.length / 2;
        ctx.buffer[mid] = rand_hexbit();

        size_t half = mid;
        WorkerCtx left = { ctx.buffer, half, ctx.depth + 1 };
        WorkerCtx right = { ctx.buffer + mid + 1, half, ctx.depth + 1 };

        pthread_create(&t1, NULL, hexentropy_worker, &left);
        pthread_create(&t2, NULL, hexentropy_worker, &right);
        pthread_join(t1, NULL);
        pthread_join(t2, NULL);
    }
    return NULL;
}

int main() {
    printf("Benchmarking %d iterations of entropy generation (%d bytes each)...\n", ITERATIONS, ENTROPY_SIZE);

    // Start timing
    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    for (int i = 0; i < ITERATIONS; ++i) {
        unsigned char *buffer = malloc(ENTROPY_SIZE);
        if (!buffer) {
            perror("malloc");
            return EXIT_FAILURE;
        }

        WorkerCtx root = { buffer, ENTROPY_SIZE, 0 };
        hexentropy_worker(&root);

        // No output, just entropy. Free buffer after use.
        free(buffer);
    }

    clock_gettime(CLOCK_MONOTONIC, &end);

    double elapsed = (end.tv_sec - start.tv_sec) + 
                     (end.tv_nsec - start.tv_nsec) / 1e9;

    printf("\nDone.\nTotal time: %.3f seconds\n", elapsed);
    printf("Throughput: %.2f calls/sec\n", ITERATIONS / elapsed);
    printf("Approx. entropy generated: %.2f GB\n", 
           (double)((unsigned long long)ITERATIONS * ENTROPY_SIZE) / (1024 * 1024 * 1024));

    return 0;
}
