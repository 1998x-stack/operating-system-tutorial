#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

enum { THREAD_COUNT = 2, ITERATIONS = 500000 };

static long counter;
#ifndef UNSAFE
static pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
#endif

static void *worker(void *unused)
{
    (void)unused;
    for (int i = 0; i < ITERATIONS; ++i) {
#ifdef UNSAFE
        ++counter;
#else
        pthread_mutex_lock(&lock);
        ++counter;
        pthread_mutex_unlock(&lock);
#endif
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
#ifndef UNSAFE
    pthread_mutex_destroy(&lock);
    return counter == (long)THREAD_COUNT * ITERATIONS ? 0 : 1;
#else
    return 0;
#endif
}
