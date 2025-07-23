#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <string.h>
#include <sys/random.h>

#define MAX_DEPTH 5
#define PATTERN_LEN 1  // 4 bits = 1 nibble = still stored in 1 byte

// Flip a coin using real entropy
int flip_coin() {
    unsigned char byte;
    if (getrandom(&byte, 1, 0) != 1) {
        perror("getrandom");
        exit(1);
    }
    return byte & 1;
}

// Structure to pass context to threads
typedef struct {
    int depth;
    int length;
    unsigned char *buffer;
    int offset;
} ThreadContext;

void *binary_mutant_worker(void *arg) {
    ThreadContext *ctx = (ThreadContext*) arg;

    if (ctx->depth >= MAX_DEPTH || ctx->length <= (2 * PATTERN_LEN)) {
        // Base case: generate random bytes
        if (getrandom(&ctx->buffer[ctx->offset], ctx->length, 0) != ctx->length) {
            perror("getrandom (base)");
            exit(1);
        }
        pthread_exit(NULL);
    }

    int half = (ctx->length - PATTERN_LEN) / 2;
    int mid = ctx->offset + half;

    // Inject pattern based on coin flip
    ctx->buffer[mid] = flip_coin() ? 0b00001000 : 0b00000111;

    pthread_t t1, t2;
    ThreadContext *left = malloc(sizeof(ThreadContext));
    ThreadContext *right = malloc(sizeof(ThreadContext));

    *left = (ThreadContext){ ctx->depth+1, half, ctx->buffer, ctx->offset };
    *right = (ThreadContext){ ctx->depth+1, half, ctx->buffer, mid + PATTERN_LEN };

    pthread_create(&t1, NULL, binary_mutant_worker, left);
    pthread_create(&t2, NULL, binary_mutant_worker, right);

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    free(left);
    free(right);
    pthread_exit(NULL);
}

int main() {
    int total_length = 1 << (MAX_DEPTH + 1);  // 2^(depth+1) for symmetry
    unsigned char *buffer = calloc(total_length, sizeof(unsigned char));

    if (!buffer) {
        perror("calloc");
        return 1;
    }

    pthread_t root;
    ThreadContext *root_ctx = malloc(sizeof(ThreadContext));
    *root_ctx = (ThreadContext){ 0, total_length, buffer, 0 };

    pthread_create(&root, NULL, binary_mutant_worker, root_ctx);
    pthread_join(root, NULL);
    free(root_ctx);

    printf("\nGenerated hexentropy:\n");
    for (int i = 0; i < total_length; i++) {
        printf("%02x", buffer[i]);
    }
    printf("\n\nDone.\n");
    free(buffer);
    return 0;
}