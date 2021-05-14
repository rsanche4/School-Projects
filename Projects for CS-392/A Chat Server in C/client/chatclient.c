/*********************************************************************************** 
 * Name        : chatclient.c
 * Author      : Sydney Cardy and Rafael Sanchez
 * Date        : 7 May 2021
 * Pledge      : I pledge my honor that I have abided by the Stevens Honor System.
 **********************************************************************************/
#include <arpa/inet.h>
#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>
#include <stdbool.h>
#include <sys/select.h>

#include "util.h"

int client_socket = -1;
char username[MAX_NAME_LEN + 1];
char inbuf[BUFLEN + 1];
char outbuf[MAX_MSG_LEN + 1];



int main(int argc, char *argv[])
{
    // Check that correct amount of arguments were inputted
    if (argc < 3)
    {
        fprintf(stderr, "Usage: %s <server IP> <port>\n", argv[0]);
        return EXIT_FAILURE;
    }

    // Init retval, server_addr, addrlen, and memset server_addr
    int retval = EXIT_SUCCESS;
    struct sockaddr_in server_addr;
    socklen_t addrlen = sizeof(struct sockaddr_in);
    memset(&server_addr, 0, addrlen); // Zero out structure

    // Check ip can be coverted
    int ip_conversion = inet_pton(AF_INET, argv[1], &server_addr.sin_addr);
    if (ip_conversion <= 0)
    {
        fprintf(stderr, "Error: Invalid IP address '%s'.\n", argv[1]);
        return EXIT_FAILURE;
    }
   

    // Check port number is correct
    int port_num = 0;
     
    if (!parse_int(argv[2], &port_num, "port number")) {
        return EXIT_FAILURE;
    }
    if ((port_num < 1024) || (port_num > 65535))
    {
        fprintf(stderr, "Error: Port must be in range [1024, 65535].\n");
        return EXIT_FAILURE;
    }

    server_addr.sin_family = AF_INET;       // Internet address family
    server_addr.sin_port = htons(port_num); // the port
                                            // server_addr.sin_addr -> ip address was already set above

 

    ssize_t bytes_read = 0;
    while (bytes_read == 0)
    {
        printf("Enter your username: ");
        fflush(stdout);
        bytes_read = read(STDIN_FILENO, username, MAX_MSG_LEN);
        
        // 1 because we are including the '\n'
        if (bytes_read > MAX_NAME_LEN + 1)
        {
            printf("Sorry, limit your username to %d characters.\n", MAX_NAME_LEN);
            fflush(stdin);
            bytes_read = 0;
            continue;
        }
        else if (bytes_read < 0 && errno != EINTR)
        {   
            printf("Error: read() failed.");
            return EXIT_FAILURE;
        } else if (bytes_read == 1) {
            bytes_read = 0;
            continue;
        }
        else if (bytes_read > 0)
        {
            username[bytes_read - 1] = '\0';
        }
    }
    

    printf("Hello, %s. Let's try to connect to the server.\n", username);

    // Create a reliable, stream socket using TCP.
    if ((client_socket = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        fprintf(stderr, "Error: Failed to create socket. %s.\n",
                strerror(errno));
        retval = EXIT_FAILURE;
        goto EXIT;
    }

    // Establish the connection to the echo server.
    if (connect(client_socket, (struct sockaddr *)&server_addr, addrlen) < 0)
    {
        fprintf(stderr, "Error: Failed to connect to server. %s.\n",
                strerror(errno));
        retval = EXIT_FAILURE;
        goto EXIT;
    }

    // Try to recieve message from server
    int bytes_recvd;
    if ((bytes_recvd = recv(client_socket, inbuf, BUFLEN, 0)) == 0)
    {
        fprintf(stderr, "All connections are busy. Try again later.\n");
        retval = EXIT_FAILURE;
        goto EXIT;
        
    }
    else if (bytes_recvd < 0)
    {
        fprintf(stderr, "Error: Failed to receive message from server. %s.\n",
                strerror(errno));
        retval = EXIT_FAILURE;
        goto EXIT;
    } else {
        // Print message recv from server
        inbuf[bytes_recvd] = '\0';
        printf("\n%s\n\n", inbuf);
    }

    

    // Send username to server
    if (send(client_socket, username, MAX_NAME_LEN+1, 0) < 0)
    {
        fprintf(stderr, "Error: Failed to send username to server. %s.\n",
                strerror(errno));
        retval = EXIT_FAILURE;
        goto EXIT;
    }

    fd_set sockset;
    
    
    while (true)
    {
        printf("[%s]: ", username);
        fflush(stdout);
        
        // Zero out and set socket descriptors for server sockets.
        // This must be reset every time select() is called.
        FD_ZERO(&sockset);
        FD_SET(client_socket, &sockset);
        FD_SET(STDIN_FILENO, &sockset);
       

        // Wait for activity on one of the sockets.
        // Timeout is NULL, so wait indefinitely.
        if (select(FD_SETSIZE, &sockset, NULL, NULL, NULL) < 0 && errno != EINTR)
        {
            fprintf(stderr, "Error: select() failed. %s.\n", strerror(errno));
            retval = EXIT_FAILURE;
            goto EXIT;
        }

        

        if (FD_ISSET(client_socket, &sockset))
        {
            bytes_recvd = recv(client_socket, inbuf, BUFLEN + 1, 0);
            if (bytes_recvd < 0)
            {
                fprintf(stderr, "Warning: Failed to receive incoming message. %s.\n",
                        strerror(errno));
            }
            else if (bytes_recvd == 0)
            {
                fprintf(stderr, "\nConnection to server has been lost.\n");
                retval = EXIT_FAILURE;
                goto EXIT;
            }
            else
            {
                inbuf[bytes_recvd] = '\0';
                if (!strcmp(inbuf, "bye"))
                {
                    printf("\nServer initiated shutdown.\n");
                    goto EXIT;
                } else {
                    printf("\n%s\n", inbuf);
                }
                
            }
            
        } 
        
        if (FD_ISSET(STDIN_FILENO, &sockset)) {
            int ret = get_string(outbuf, MAX_MSG_LEN);
            if (ret == TOO_LONG)
            {
                printf("Sorry, limit your message to %d characters.\n", MAX_MSG_LEN);
            }
            else if (ret == NO_INPUT)
            {
                continue;
            }
            else if (ret == OK)
            {
                // send message to the server
                if (send(client_socket, outbuf, strlen(outbuf), 0) < 0)
                {
                    fprintf(stderr, "Error: Failed to send message to server. %s.\n",
                            strerror(errno));
                    continue;
                }
                if (!strcmp(outbuf, "bye"))
                {
                    printf("Goodbye.\n");
                    goto EXIT;
                }
            }
        }
    }

EXIT:
    if (fcntl(client_socket, F_GETFD) >= 0)
    {
        close(client_socket);
    }
    return retval;
}