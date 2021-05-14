/*********************************************************************************** 
 * Name        : mtsieve.c
 * Author      : Sydney Cardy and Rafael Sanchez
 * Date        : 23 April 2021
 * Pledge      : I pledge my honor that I have abided by the Stevens Honor System.
 **********************************************************************************/

#include <pthread.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <ctype.h>
#include <string.h>
#include <sys/sysinfo.h>
#include <math.h>

typedef struct arg_struct
{
    int start;
    int end;
} thread_args;

int total_count = 0;
pthread_mutex_t lock;

bool has_more_three(int num)
{
    int count = 0;
    while (num > 0)
    {
        if ((num % 10) == 3)
        {
            count++;
            if (count > 1)
            {
                return true;
            }
        }
        num /= 10;
    }
    return false;
}

void *prime_sieve(void *ptr)
{
    thread_args *args = (thread_args *)ptr;
    int a = args->start;
    int b = args->end;

    int upper_bound = (int)sqrt((double)b);

    int size = upper_bound + 1;
    bool low_primes_helper[size];
    for (int i = 0; i < size; i++)
    {
        low_primes_helper[i] = true;
    }
    low_primes_helper[0] = false;
    low_primes_helper[1] = false;

    // Running step 1
    for (int k = 2; k <= (int)sqrt((double)upper_bound); k++)
    {
        if (low_primes_helper[k])
        {
            for (int j = k * k; j <= upper_bound; j = k * j)
            {
                low_primes_helper[j] = false;
            }
        }
    }

    // So now running step 2
    int len = b - a + 1;
    bool *high_primes = malloc(len*sizeof(bool));
    for (int r = 0; r < len; r++)
    {
        high_primes[r] = true;
    }

    // Count is size of low_primes.

    for (int p = 2; p < upper_bound; p++)
    {
        if (low_primes_helper[p])
        {
            int i = (int)(ceil(((double)a / p))) * p - a;
            if (a <= p)
            {
                i += p;
            }
            // Then starting at i, cross off multiples of p in high primes
            for (int j = i; j < len; j += p)
            {
                high_primes[j] = false;
            }
        }
    }

    // Then run step 4. For each high primes at i set to true, print i + start
    int partial_sum = 0;
    for (int q = 0; q < len; q++)
    {
        if (high_primes[q] && has_more_three(q + a))
        {
            partial_sum++;
        }
    }

    int retval;
    if ((retval = pthread_mutex_lock(&lock)) != 0)
    {
        fprintf(stderr, "Warning: Cannot lock mutex. %s.\n",
                strerror(retval));
    }
    total_count = total_count + partial_sum;
    if ((retval = pthread_mutex_unlock(&lock)) != 0)
    {
        fprintf(stderr, "Warning: Cannot unlock mutex. %s.\n",
                strerror(retval));
    }
    free(high_primes);
    pthread_exit(NULL);
}

int main(int argc, char *argv[])
{
    if (argc < 2)
    {
        fprintf(stderr, "Usage: ./mtsieve -s <starting value> -e <ending value> -t <num threads>\n");
        return EXIT_FAILURE;
    }

    char *sval = 0;
    int startv = -1;
    bool sGiven = false;

    char *eval = 0;
    int endingv = -1;
    bool eGiven = false;

    char *tval = 0;
    int threadnum = -1;
    bool tGiven = false;

    char checker1[1024];
    char checker2[1024];
    char checker3[1024];
    int c;
    opterr = 0;
    // #TODO Problem with atoi returning 0 on failure. What if the argument number given is actually zero?
    while ((c = getopt(argc, argv, "s:e:t:")) != -1)
    {
        switch (c)
        {
        case 's':
            sval = optarg;
            if ((startv = atoi(sval)) == 0)
            {
                fprintf(stderr, "Error: Invalid input '%s' received for parameter '-%c'.\n", sval, 's');
                return EXIT_FAILURE;
            }

            sprintf(checker1, "%d", startv);
            if (strcmp(sval, checker1) != 0)
            {
                fprintf(stderr, "Error: Integer overflow for parameter '-%c'.\n", 's');
                return EXIT_FAILURE;
            }
            sGiven = true;
            break;
        case 'e':
            eval = optarg;
            if ((endingv = atoi(eval)) == 0)
            {
                fprintf(stderr, "Error: Invalid input '%s' received for parameter '-%c'.\n", eval, 'e');
                return EXIT_FAILURE;
            }

            sprintf(checker2, "%d", endingv);
            if (strcmp(eval, checker2) != 0)
            {
                fprintf(stderr, "Error: Integer overflow for parameter '-%c'.\n", 'e');
                return EXIT_FAILURE;
            }
            eGiven = true;
            break;
        case 't':
            tval = optarg;
            if ((threadnum = atoi(tval)) == 0)
            {
                fprintf(stderr, "Error: Invalid input '%s' received for parameter '-%c'.\n", tval, 't');
                return EXIT_FAILURE;
            }

            sprintf(checker3, "%d", threadnum);
            if (strcmp(tval, checker3) != 0)
            {
                fprintf(stderr, "Error: Integer overflow for parameter '-%c'.\n", 't');
                return EXIT_FAILURE;
            }
            tGiven = true;
            break;
        case '?':
            if (optopt == 'e' || optopt == 's' || optopt == 't')
            {
                fprintf(stderr, "Error: Option -%c requires an argument.\n", optopt);
            }
            else if (isprint(optopt))
            {
                fprintf(stderr, "Error: Unknown option '-%c'.\n", optopt);
            }
            else
            {
                fprintf(stderr, "Error: Unknown option character '\\x%x'.\n",
                        optopt);
            }
            return EXIT_FAILURE;
        }
    }

    // #TODO when being given a -e20 it says it's 1 argument
    if (argc > 7)
    {
        int i = 0;
        while (argv[i] != NULL)
        {
            if (!strcmp(argv[i], "./mtsieve") || !strcmp(argv[i], "-s") || !strcmp(argv[i], "-e") || !strcmp(argv[i], "-t") ||
                !strcmp(argv[i], checker1) || !strcmp(argv[i], checker2) ||
                !strcmp(argv[i], checker3))
            {
                i++;
                continue;
            }
            else
            {
                fprintf(stderr, "Error: Non-option argument '%s' supplied.\n", argv[i]);
                return EXIT_FAILURE;
            }
        }
    }

    if (sGiven == false)
    {
        fprintf(stderr, "Error: Required argument <starting value> is missing.\n");
        return EXIT_FAILURE;
    }

    if (startv < 2)
    {
        fprintf(stderr, "Error: Starting value must be >= 2.\n");
        return EXIT_FAILURE;
    }

    if (eGiven == false)
    {
        fprintf(stderr, "Error: Required argument <ending value> is missing.\n");
        return EXIT_FAILURE;
    }

    if (endingv < 2)
    {
        fprintf(stderr, "Error: Ending value must be >= 2.\n");
        return EXIT_FAILURE;
    }

    if (endingv < startv)
    {
        fprintf(stderr, "Error: Ending value must be >= starting value.\n");
        return EXIT_FAILURE;
    }

    if (tGiven == false)
    {
        fprintf(stderr, "Error: Required argument <num threads> is missing.\n");
        return EXIT_FAILURE;
    }

    if (threadnum < 1)
    {
        fprintf(stderr, "Error: Number of threads cannot be less than 1.\n");
        return EXIT_FAILURE;
    }

    if (threadnum > 2 * get_nprocs())
    {
        fprintf(stderr, "Error: Number of threads cannot exceed twice the number of processors(%d).\n", get_nprocs());
        return EXIT_FAILURE;
    }

    printf("Finding all prime numbers between %d and %d.\n", startv, endingv);

    int vals_inside_each_seg = 0;
    int remainder = 0;
    // Now let's devide it into segments
    int number_being_tested = (endingv - startv) + 1;
    if (threadnum > number_being_tested)
    {
        threadnum = number_being_tested;
    }
    vals_inside_each_seg = (number_being_tested / threadnum);
    remainder = number_being_tested % threadnum;

    int retval;
    if ((retval = pthread_mutex_init(&lock, NULL)) != 0)
    {
        fprintf(stderr, "Error: Cannot create mutex. %s.\n", strerror(retval));
        return EXIT_FAILURE;
    }

    pthread_t threads[threadnum];
    thread_args targs[threadnum];

    int helper[threadnum]; // For each value inside the helper we will assign the number we need for each thread

    for (int i = 0; i < threadnum; i++)
    {
        helper[i] = vals_inside_each_seg;
    }

    // And then after that Imma distribute among all the remainder
    for (int j = 0; j < threadnum; j++)
    {
        if (remainder <= 0)
        {
            break;
        }
        helper[j] = helper[j] + 1;
        remainder--;
    }

    // And then after that, imma set each thread's start and ending values
    int init = startv;
    for (int k = 0; k < threadnum; k++)
    {
        targs[k].start = init;
        targs[k].end = init + helper[k] - 1;
        init = targs[k].end + 1;
    }

    // Just output the segments
    if (threadnum == 1)
    {
        printf("%d segment:\n", threadnum);
    }
    else
    {
        printf("%d segments:\n", threadnum);
    }
    for (int h = 0; h < threadnum; h++)
    {
        printf("   [%d, %d]\n", targs[h].start, targs[h].end);
    }

    for (int z = 0; z < threadnum; z++)
    {

        int retval2;
        if ((retval2 = pthread_create(&threads[z], NULL, prime_sieve, &targs[z])) != 0)
        {
            fprintf(stderr, "Error: Cannot create thread %d. %s.\n", z + 1,
                    strerror(retval2));
            return EXIT_FAILURE;
        }

        if ((retval2 = pthread_mutex_lock(&lock)) != 0)
        {
            fprintf(stderr, "Warning: Cannot lock mutex. %s.\n",
                    strerror(retval2));
        }
        if ((retval2 = pthread_mutex_unlock(&lock)) != 0)
        {
            fprintf(stderr, "Warning: Cannot unlock mutex. %s.\n",
                    strerror(retval2));
        }
    }

    for (int o = 0; o < threadnum; o++)
    {
        if (pthread_join(threads[o], NULL) != 0)
        {
            fprintf(stderr, "Warning: Thread %d did not join properly.\n",
                    o + 1);
        }
    }

    int retval3;
    if ((retval3 = pthread_mutex_destroy(&lock)) != 0)
    {
        fprintf(stderr, "Error: Cannot destroy mutex. %s.\n", strerror(retval3));
        return EXIT_FAILURE;
    }

    printf("Total primes between %d and %d with two or more '3' digits: %d\n", startv, endingv, total_count);

    return EXIT_SUCCESS;
}