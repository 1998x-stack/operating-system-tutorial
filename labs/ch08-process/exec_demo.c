#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

int main(void)
{
    pid_t child = fork();
    if (child < 0) {
        perror("fork");
        return 1;
    }

    if (child == 0) {
        char *const args[] = {"/bin/echo", "child image replaced by execve", NULL};
        execv(args[0], args);
        perror("execv");
        _exit(127);
    }

    int status = 0;
    if (waitpid(child, &status, 0) < 0) {
        perror("waitpid");
        return 1;
    }

    printf("parent observed child exit status: %d\n",
           WIFEXITED(status) ? WEXITSTATUS(status) : -1);
    return 0;
}
