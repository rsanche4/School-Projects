#*******************************************************************************
 # Name        : pfind.c
 # Author      : Sydney Cardy and Rafael Sanchez
 # Date        : 16 March 2021
 # Description : Finds all files in the system with the given perms
 # Pledge : I pledge my honor that I have abided by the Stevens Honor System.
 #*****************************************************************************/
CC     = gcc
C_FILE = $(wildcard *.c)
TARGET = $(patsubst %.c,%,$(C_FILE))
CFLAGS = -g -Wall -Werror -pedantic-errors

all:
	$(CC) $(CFLAGS) $(C_FILE) -o $(TARGET)
clean:
	rm -f $(TARGET) $(TARGET).exe
