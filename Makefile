# This makefile compiles all C files in the same directory and produces a single
# executable named solution
CC = gcc
CFLAGS = -std=c11 -Wall -Wextra -pedantic -O2 -g -pthread  # this uses the C11 standard, if you want to use a different standard, change it to -std=c[NUMBER]
CPPFLAGS = -MMD -fopenmp
LD_FLAGS = -lm -fopenmp

#include .env
export OMP_NUM_THREADS=4

BIN_NAME = solution
SRC_FILES = $(wildcard *.c)
OBJ_FILES = $(SRC_FILES:.c=.o) 
DEP_FILES = $(wildcard *.d)

run: $(BIN_NAME)
	./$(BIN_NAME)

include $(DEP_FILES)

$(BIN_NAME): $(OBJ_FILES)
	$(CC) $(CPPFLAGS) $(LD_FLAGS) $(OBJ_FILES) -pthread -o $@

%.o: %.c
	$(CC) $(CFLAGS) $(CPPFLAGS) -c $< -o $@ 

clean:	
	@rm -v *.o *.d
	@rm -v ./$(BIN_NAME)

.PHONY: run clean
