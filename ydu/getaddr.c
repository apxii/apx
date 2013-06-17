#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/ioctl.h>
#include <netinet/in.h>
#include <net/if.h>
#include <arpa/inet.h>

int main(int argc, char *argv[])
{
    int fd;
    struct ifreq ifr;
    struct sockaddr_in *sip;

    fd = socket(PF_INET, SOCK_DGRAM, IPPROTO_IP);

    ifr.ifr_addr.sa_family = PF_INET;
    strncpy(ifr.ifr_name, argv[1],  IFNAMSIZ-1);

    ioctl(fd, SIOCGIFADDR, &ifr);

    close(fd);

    sip=(struct sockaddr_in *)&ifr.ifr_addr;
    printf("%s: %s\n", ifr.ifr_name, inet_ntoa(sip->sin_addr));

    return 0;
}
