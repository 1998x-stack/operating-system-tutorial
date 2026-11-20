#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/resource.h>
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

    unsigned char *page = mmap(NULL, (size_t)page_size,
                               PROT_READ | PROT_WRITE,
                               MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (page == MAP_FAILED) {
        perror("mmap");
        return 1;
    }

    page[0] = 0x11;
    printf("parent before fork: 0x%02x (page size %ld)\n",
           page[0], page_size);
    fflush(stdout);

    pid_t child = fork();
    if (child < 0) {
        perror("fork");
        munmap(page, (size_t)page_size);
        return 1;
    }

    if (child == 0) {
        struct rusage before, after;
        getrusage(RUSAGE_SELF, &before);
        page[0] = 0x42;
        getrusage(RUSAGE_SELF, &after);
        dprintf(STDOUT_FILENO,
                "child after write: 0x%02x; minor-fault delta=%ld\n",
                page[0], after.ru_minflt - before.ru_minflt);
        munmap(page, (size_t)page_size);
        _exit(0);
    }

    int status = 0;
    if (waitpid(child, &status, 0) < 0) {
        perror("waitpid");
        munmap(page, (size_t)page_size);
        return 1;
    }

    printf("parent after child exit: 0x%02x\n", page[0]);
    munmap(page, (size_t)page_size);
    return WIFEXITED(status) ? WEXITSTATUS(status) : 1;
}
