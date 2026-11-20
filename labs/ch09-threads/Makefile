CC ?= cc
CFLAGS ?= -O2 -g -Wall -Wextra -Wpedantic

all: counter

counter: counter.c
	$(CC) $(CFLAGS) -pthread $< -o $@

clean:
	rm -f counter

.PHONY: all clean
