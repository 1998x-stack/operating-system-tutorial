#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

enum { THREAD_COUNT = 4, ITERATIONS = 250000 };

static pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
static long counter;

static void *worker(void *unused)
{
    (void)unused;
    for (int i = 0; i < ITERATIONS; ++i) {
        pthread_mutex_lock(&lock);
        ++counter;
        pthread_mutex_unlock(&lock);
    }
    return NULL;
}

int main(void)
{
    pthread_t threads[THREAD_COUNT];

    for (int i = 0; i < THREAD_COUNT; ++i) {
        int err = pthread_create(&threads[i], NULL, worker, NULL);
        if (err != 0) {
            fprintf(stderr, "pthread_create: %d\n", err);
            return 1;
        }
    }

    for (int i = 0; i < THREAD_COUNT; ++i) {
        int err = pthread_join(threads[i], NULL);
        if (err != 0) {
            fprintf(stderr, "pthread_join: %d\n", err);
            return 1;
        }
    }

    printf("counter=%ld expected=%d\n",
           counter, THREAD_COUNT * ITERATIONS);
    pthread_mutex_destroy(&lock);
    return counter == (long)THREAD_COUNT * ITERATIONS ? 0 : 1;
}
