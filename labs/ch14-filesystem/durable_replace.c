#define _GNU_SOURCE
#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>

static int write_all(int fd, const char *buf, size_t len)
{
    size_t done = 0;
    while (done < len) {
        ssize_t n = write(fd, buf + done, len - done);
        if (n < 0) {
            if (errno == EINTR)
                continue;
            return -1;
        }
        done += (size_t)n;
    }
    return 0;
}

int main(void)
{
    static const char payload[] = "durable replace demo\n";
    const char *tmp_name = "os-tutorial.tmp";
    const char *final_name = "os-tutorial.txt";

    int fd = open(tmp_name, O_WRONLY | O_CREAT | O_TRUNC | O_CLOEXEC, 0644);
    if (fd < 0) {
        perror("open temp");
        return 1;
    }

    if (write_all(fd, payload, sizeof(payload) - 1) < 0) {
        perror("write");
        close(fd);
        return 1;
    }
    if (fsync(fd) < 0) {
        perror("fsync file");
        close(fd);
        return 1;
    }
    if (close(fd) < 0) {
        perror("close");
        return 1;
    }

    if (rename(tmp_name, final_name) < 0) {
        perror("rename");
        return 1;
    }

    int dirfd = open(".", O_RDONLY | O_DIRECTORY | O_CLOEXEC);
    if (dirfd < 0) {
        perror("open directory");
        return 1;
    }
    if (fsync(dirfd) < 0) {
        perror("fsync directory");
        close(dirfd);
        return 1;
    }
    if (close(dirfd) < 0) {
        perror("close directory");
        return 1;
    }

    printf("replaced %s after syncing file and directory\n", final_name);
    return 0;
}
