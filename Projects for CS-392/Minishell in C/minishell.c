/******************************************************************************* 
 * Name        : minishell.c
 * Author      : Sydney Cardy and Rafael Sanchez
 * Date        : 9 April 2021
 * Pledge : I pledge my honor that I have abided by the Stevens Honor System.
 ******************************************************************************/

#include <stdbool.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>
#include <limits.h>
#include <signal.h>
#include <ctype.h>
#include <pwd.h>

#define BRIGHTBLUE "\x1b[34;1m"
#define DEFAULT "\x1b[0m"
#define ARGS_LEN 2048

sig_atomic_t interrupted = 0;

char args[ARGS_LEN];
char argv[ARGS_LEN][ARGS_LEN];
int argc;

// Signal handler
void catch_signal(int sig)
{
    char *msg = "\n";
    write(STDOUT_FILENO, msg, 1); // use write for this
    interrupted = sig;
}

// Just flushes out old arguments
void flush()
{
    for (int o = 0; o < ARGS_LEN; o++)
    {
        args[o] = '\0';
        for (int f = 0; f < ARGS_LEN; f++)
        {
            argv[o][f] = '\0';
        }
    }
}

char **get_args(char *input, int arg_count)
{
    char **args = malloc((arg_count + 1) * sizeof(char *));

    char *arg = strtok(input, " ");
    for (int i = 0; i < arg_count && arg != NULL; ++i)
    {
        args[i] = arg;
        arg = strtok(NULL, " ");
    }
    args[arg_count] = NULL;
    return args;
}

bool starts_with(const char *str, const char *prefix)
{
    size_t lenpre = strlen(prefix);
    return strlen(str) < lenpre ? false : strncmp(prefix, str, lenpre) == 0;
}

void removeSpaceInBetween()
{
    // Take args and null out all the stuff that comes after the null. So null it all out.
    int count = 0;
    while (args[count] != '\0')
    {
        count++;
    }
    // So now at count, we have our null terminating, null out everything afterwards
    for (int i = count; i < ARGS_LEN; i++)
    {
        args[i] = '\0';
    }

    /*
    * For example:
    * x - - - - - x 0 where x is a letter, n is a newline, and 0 is the null term (- is a space), after this loops terminates, args has
    * x n n n n - x 0
    */
    int z = 0;
    while (args[z] != '\0')
    {
        if (args[z] == ' ' && args[z + 1] == ' ')
        {
            args[z] = '\n';
        }
        z++;
    }

    /*
    * For example:
    * x n n n n - x 0 
    * x - x 0 0 0 0 0
    */
    char copy[ARGS_LEN];
    // Null out copy
    for (int i = 0; i < ARGS_LEN; i++)
    {
        copy[i] = '\0';
    }

    int i = 0;
    for (int j = 0; j < ARGS_LEN; j++)
    {
        if (args[j] != '\n')
        {
            copy[i] = args[j];
            i++;
        }
    }

    // Copy the stuff from copy back to args
    for (int i = 0; i < ARGS_LEN; i++)
    {
        args[i] = copy[i];
    }

    return;
}

// Takes args and erases any unnessary lines from trailing
void trimwhitespace(char *str)
{
    char *end;

    // Trim leading space
    while (isspace((unsigned char)*str))
        str++;

    if (*str == 0) // All spaces?
        return;

    // Trim trailing space
    end = str + strlen(str) - 1;
    while (end > str && isspace((unsigned char)*end))
        end--;

    // Write new null terminator character
    end[1] = '\0';

    return;
}

// Remove leading space
void removeLeadingSpaces(char *str)
{
    static char str1[ARGS_LEN];
    int count = 0, j, k;

    while (str[count] == ' ')
    {
        count++;
    }

    // removing leading white spaces
    for (j = count, k = 0;
         str[j] != '\0'; j++, k++)
    {
        str1[k] = str[j];
    }
    str1[k] = '\0';

    for (int i = 0; i < ARGS_LEN; i++)
    {
        str[i] = str1[i];
    }
    return;
}

int main()
{
    struct sigaction action;

    memset(&action, 0, sizeof(struct sigaction));
    action.sa_handler = catch_signal;
    if (sigaction(SIGINT, &action, NULL) == -1)
    {
        perror("sigaction");
    }

    while (true)
    {

        char current_dir[PATH_MAX];
        if (getcwd(current_dir, PATH_MAX) == NULL)
        {
            fprintf(stderr, "Error: Cannot get current working directory. %s.\n",
                    strerror(errno));
            return EXIT_FAILURE;
        }

        printf("[%s%s%s]$ ", BRIGHTBLUE, current_dir, DEFAULT);
        // fgets(args, ARGS_LEN, stdin) == NULL
        // read(STDIN_FILENO, args, ARGS_LEN) < 0
        if (fgets(args, ARGS_LEN, stdin) == NULL)
        {
            if (interrupted == SIGINT)
            {
                continue;
            }
            else
            {
                fprintf(stderr, "Error: Failed to read from stdin. %s.\n",
                        strerror(errno));
                continue;
            }
        }
        // printf("Im running\n");
        // if (read(STDIN_FILENO, args, ARGS_LEN) < 0) // #TODO how to use read for this. fgets handles urandom but doesnt print a new line
        // {
        //     if (errno == EINTR) {
        //         continue;
        //     } else {
        //         fprintf(stderr, "Error: Failed to read from stdin. %s.\n",
        //                  strerror(errno));
        //         continue;
        //     }
        // }
        // printf("[%s%s%s]$ ", BRIGHTBLUE, current_dir, DEFAULT);

        // let's make sure an arg was given at all
        bool arg_given = false;
        for (int i = 0; i < ARGS_LEN; i++)
        {
            if (args[i] == ' ' || args[i] == '\n' || args[i] == '\0')
            {
                continue;
            }
            else
            {
                arg_given = true;
                break;
            }
        }

        if (arg_given)
        {
            // Now we can remove any trailing/leading/inbetween space from that args
            trimwhitespace(args);
            removeLeadingSpaces(args);
            removeSpaceInBetween();

            //After this we need to parse the stuff into argc and *argv[]
            int i = 0;
            int j = 0;
            int k = 0;
            while (args[j] != '\0')
            {
                if (args[j] != ' ')
                {
                    argv[i][k] = args[j];
                    j++;
                    k++;
                }
                else if (args[j] == ' ')
                {
                    j++;
                    i++;
                    argv[i][k] = '\0';
                    k = 0;
                }
            }
            i++;
            argv[i][0] = '\0';
            argc = i;

            //next thing now is to call cd and exit and pass all the args to them, or if it's something else, just send it to exec
            if (starts_with(args, "exit"))
            {
                return EXIT_SUCCESS;
            }
            else if (!strcmp(args, "cd") || !strcmp(args, "cd ~"))
            {
                // Here is where we are going to start doing things for cd to go to /home/user
                uid_t uid = getuid();
                struct passwd *pw = getpwuid(uid);

                if (pw == NULL)
                {
                    fprintf(stderr, "Error: Cannot get passwd entry. %s.\n",
                            strerror(errno));
                    //Flush out the stuff from the arguments
                    flush();
                    continue;
                }
                if (chdir(pw->pw_dir) < 0)
                {
                    fprintf(stderr, "Error: Cannot change directory to '%s'. %s.\n", pw->pw_dir,
                            strerror(errno));
                    //Flush out the stuff from the arguments
                    flush();
                    continue;
                }
            }
            else if (starts_with(args, "cd "))
            {

                // Here we are going to check for the directory we are going to cd in
                if (argc != 2)
                {
                    fprintf(stderr, "Error: Too many arguments to cd.\n");
                    //Flush out the stuff from the arguments
                    flush();
                    continue;
                }

                if (chdir(argv[1]) < 0)
                {
                    fprintf(stderr, "Error: Cannot change directory to '%s'. %s.\n", argv[1],
                            strerror(errno));
                    //Flush out the stuff from the arguments
                    flush();
                    continue;
                }
            }
            else
            {
                // Here we are calling to exec on all other commands
                // Also just for exec, put argv in the right format
                char **args_to_exec;
                char copy_args[ARGS_LEN];
                for (int k = 0; k < ARGS_LEN; k++)
                {
                    copy_args[k] = args[k];
                }
                args_to_exec = get_args(copy_args, argc);

                if (args_to_exec == NULL)
                {
                    fprintf(stderr, "Error: malloc() failed. %s.\n",
                            strerror(errno));
                    flush();
                    continue;
                }

                pid_t pid;
                if ((pid = fork()) < 0)
                {
                    fprintf(stderr, "Error: fork() failed. %s.\n",
                            strerror(errno));
                    flush();
                    free(args_to_exec);
                    continue;
                }

                if (pid == 0)
                {
                    // Child
                    if (execvp(args_to_exec[0], args_to_exec) < 0)
                    {
                        fprintf(stderr, "Error: exec() failed. %s.\n",
                                strerror(errno));
                        exit(EXIT_FAILURE);
                    }
                }

                if (pid > 0)
                {
                    // We are back to the parent
                    // Wait for the child #TODO this wait fails everytime we send a SIGINT for a command like sleep 10 or yes
                    if (wait(NULL) < 0)
                    {
                        if (errno == EINTR)
                        {
                            free(args_to_exec);
                            flush();
                            continue;
                        }
                        fprintf(stderr, "Error: wait() failed.\n");
                        flush();
                    }
                }
                free(args_to_exec);
            }

            //Flush out the stuff from the arguments
            flush();
            continue;
        }
        else
        {
            continue;
        }
    }
    return EXIT_SUCCESS;
}