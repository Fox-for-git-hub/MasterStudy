#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
#include<sys/socket.h>
#include<sys/types.h>
#include<arpa/inet.h>
#include<netinet/in.h>
#include<netdb.h>

#define BUFSIZE 512

int main(int argc, char *argv[]){

    int s;
    int con_flag;
    struct sockaddr_in server;
    u_short port;
    char send_buf[BUFSIZE];
    int send_len;
    char recv_buf[BUFSIZE];
    int recv_len;

    //argument check
    if(argc != 3){
        printf("Usage: %s ipaddr port\n", argv[0]);
        exit(1);
    }

    //create socket
    s = socket(AF_INET, SOCK_STREAM, 0);
    if(s<0){
        perror("Socket Error\n");
        exit(1);
    }

    //set socket addr of server
    memset(&server, 0, sizeof(server));
    server.sin_family = AF_INET;
    server.sin_addr.s_addr = inet_addr(argv[1]);
    port = atoi(argv[2]);
    server.sin_port = htons(port);

    //create connection to server
    con_flag = connect(s, (struct sockaddr *)&server, sizeof(server));
    if(con_flag<0){
        perror("Connect Error\n");
        exit(1);
    }
    printf("Connected to %s\n", inet_ntoa(server.sin_addr));

    //Send Message 
    while(1){

        fgets(send_buf, BUFSIZE, stdin);

        //exit command
        if(strncmp(send_buf, "exit", 4) == 0){
            break;
        }

        //send message to server
        send_len = strlen(send_buf);
        send(s, send_buf, send_len, 0);

        //receive mesages from server
        recv_len = recv(s, recv_buf, BUFSIZE, 0);
        recv_buf[recv_len] = '\0';

        //display messages from server
        printf("%s", recv_buf);
    }

    close(s);

    return 0;

}
