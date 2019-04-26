#!/bin/bash

hostname=$(/usr/bin/shuf -n 1 ./hostnames.txt)


/sbin/ifconfig wlan1 down && /usr/bin/macchanger -r wlan1 && /sbin/ifconfig wlan1 up && /bin/echo $hostname > /etc/hostname && /bin/hostname $hostname && /usr/sbin/service networking restart
