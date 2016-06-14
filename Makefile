CC = gcc
CFLAGS = -g -Wall

conway: indexFastq.c
	${CC} ${CFLAGS} -o indexFastq indexFastq.c

clean:
	rm indexFastq
