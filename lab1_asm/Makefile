bisq_asm: bisq.asm
	fasm bisq.asm

bisq_c_c: bisq_c.c
	gcc -c bisq_c.c -o bisq_c.o

build: bisq bisq_c
	ld bisq_c.o bisq.o -o myprog

run: build myprog
	./myprog

clean:
	rm -f *.o