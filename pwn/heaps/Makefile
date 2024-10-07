.PHONY: patch clean

heaps: heaps.o
	gcc -o heaps heaps.o

heaps.o: heaps.c
	gcc -Wall -Wextra -Wpedantic -std=c17 -c -o heaps.o heaps.c

patch:
	patchelf --set-interpreter ./ld-linux-x86-64.so.2 heaps
	patchelf --replace-needed libc.so.6 ./libc.so.6 heaps

clean:
	rm *.o heaps