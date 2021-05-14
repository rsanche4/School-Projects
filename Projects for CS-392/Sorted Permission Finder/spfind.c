/******************************************************************************* 
 * Name        : spfind.c
 * Author      : Sydney Cardy and Rafael Sanchez
 * Date        : 31 March 2021
 * Description : sorts the result from pfind
 * Pledge : I pledge my honor that I have abided by the Stevens Honor System.
 ******************************************************************************/

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>
#include <stdbool.h>
#include <string.h>

bool starts_with(const char *str, const char *prefix)
{
    size_t lenpre = strlen(prefix);
    return strlen(str) < lenpre ? false : strncmp(prefix, str, lenpre) == 0;
}

int main(int argc, char *argv[])
{

    int pfind_to_sort[2];
    int sort_to_parent[2];

    if (pipe(pfind_to_sort) < 0)
    {
        fprintf(stderr, "Error: Cannot create pipe pfind_to_sort. %s.\n",
                strerror(errno));
        return EXIT_FAILURE;
    }
    if (pipe(sort_to_parent) < 0)
    {
        fprintf(stderr, "Error: Cannot create pipe sort_to_parent. %s.\n",
                strerror(errno));
        return EXIT_FAILURE;
    }

    pid_t pid[2];
    if ((pid[0] = fork()) == 0)
    {
        // pfind
        close(pfind_to_sort[0]);
        dup2(pfind_to_sort[1], STDOUT_FILENO);

        // Close all unrelated file descriptors.
        close(sort_to_parent[0]);
        close(sort_to_parent[1]);

        if (execv("pfind", argv) < 0)
        {
            fprintf(stderr, "Error: pfind failed.\n");
            exit(EXIT_FAILURE);
        }
    }

    if ((pid[1] = fork()) == 0)
    {
        // sort
        close(pfind_to_sort[1]);
        dup2(pfind_to_sort[0], STDIN_FILENO);

        close(sort_to_parent[0]);
        dup2(sort_to_parent[1], STDOUT_FILENO);

        if (execlp("sort", "sort", NULL) < 0)
        {
            fprintf(stderr, "Error: sort failed.\n");
            exit(EXIT_FAILURE);
        }
    }

    // Parent
    close(sort_to_parent[1]);
    dup2(sort_to_parent[0], STDIN_FILENO);

    // Close all unrelated file descriptors
    close(pfind_to_sort[0]);
    close(pfind_to_sort[1]);

    char buffer[8192];
    long line_number = 0;

    while (true)
    {
        ssize_t count = read(STDIN_FILENO, buffer, sizeof(buffer));
        if (buffer[0] == '\0')
        {
            exit(EXIT_FAILURE);
        }
        if (starts_with(buffer, "Usage"))
        {
            write(STDOUT_FILENO, buffer, count);
            exit(EXIT_FAILURE);
        }

        if (count == -1)
        {
            if (errno == EINTR)
            {
                continue;
            }
            else
            {
                perror("read()");
                exit(EXIT_FAILURE);
            }
        }
        else if (count == 0)
        {

            printf("Total matches: %ld\n", line_number);
            break;
        }
        else
        {
            write(STDOUT_FILENO, buffer, count);
            for (int i = 0; i < count; i++)
            {
                if (buffer[i] == '\n')
                {
                    line_number++;
                }
            }
        }
    }

    close(sort_to_parent[0]);
    wait(NULL);
    wait(NULL);

    return EXIT_SUCCESS;
}