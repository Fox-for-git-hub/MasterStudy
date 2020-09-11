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
#define PORT 10000

int main(){

int s, s_new;
int bind_flag;
struct sockaddr_in client;
struct sockaddr_in server;
u_short port;
char send_buf[BUFSIZE];
int send_len;
char recv_buf[BUFSIZE];
int recv_len;
unsigned int client_len;
int i;

//create socket
s = socket(AF_INET, SOCK_STREAM, 0);
if(s<0){
    perror("Socket Error\n");
    exit(1);
}

//set socket addr of server
memset(&server, 0, sizeof(server));
server.sin_family = AF_INET;
server.sin_addr.s_addr = htonl(INADDR_ANY);
server.sin_port = htons(PORT);

//bind
bind_flag = bind(s, (struct sockaddr*)&server, sizeof(server));
if(bind_flag<0){
    perror("Bind Error");
    exit(1);
}

//listen
listen(s, 5);
printf("Listen...\n");

//Accept
s_new = accept(s, (struct sockaddr *)&client, &client_len);
printf("Connected from %s\n", inet_ntoa(client.sin_addr));

//Receive and Send back Messages
while(1){

    //Receive
    recv_len = recv(s_new, recv_buf, BUFSIZ, 0);
    if(recv_len<1) break;
    recv_buf[recv_len] = '\0';
    printf("RECV=>%s", recv_buf);

    for(i=0;i<recv_len;i++){
        send_buf[i] = recv_buf[i];
    }
    send_buf[i] = '\0';

    //Send back
    send_len = strlen(send_buf);
    send(s_new, send_buf, send_len, 0);
}

close(s_new);
close(s);

return 0;
}
