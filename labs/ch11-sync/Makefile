CC ?= cc
CFLAGS ?= -O1 -g -Wall -Wextra

safe: counter.c
	$(CC) $(CFLAGS) -pthread counter.c -o counter-safe

tsan: counter.c
	$(CC) $(CFLAGS) -DUNSAFE -fsanitize=thread -pthread counter.c -o counter-tsan

clean:
	rm -f counter-safe counter-tsan

.PHONY: safe tsan clean
