#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

int main(void)
{
    long page_size = sysconf(_SC_PAGESIZE);
    if (page_size <= 0) {
        perror("sysconf");
        return 1;
    }

    int *value = mmap(NULL, (size_t)page_size,
                      PROT_READ | PROT_WRITE,
                      MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (value == MAP_FAILED) {
        perror("mmap");
        return 1;
    }

    *value = 7;
    printf("parent before fork: %d\n", *value);
    fflush(stdout);

    pid_t child = fork();
    if (child < 0) {
        perror("fork");
        munmap(value, (size_t)page_size);
        return 1;
    }

    if (child == 0) {
        *value = 99;
        dprintf(STDOUT_FILENO, "child after write: %d\n", *value);
        munmap(value, (size_t)page_size);
        _exit(0);
    }

    int status = 0;
    if (waitpid(child, &status, 0) < 0) {
        perror("waitpid");
        munmap(value, (size_t)page_size);
        return 1;
    }

    printf("parent after child exit: %d\n", *value);
    munmap(value, (size_t)page_size);
    return WIFEXITED(status) ? WEXITSTATUS(status) : 1;
}
