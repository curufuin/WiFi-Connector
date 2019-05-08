#!/bin/bash

currentHostname=$(hostname)
hostname=$(/usr/bin/shuf -n 1 /home/pi/bin/hostnames.txt)


/sbin/ifconfig wlan1 down && /usr/bin/macchanger -r wlan1 && /sbin/ifconfig wlan1 up && /bin/echo $hostname > /etc/hostname && /bin/hostname $hostname && /bin/sed -i "s/${currentHostname}/${hostname}/g" /etc/hosts && /usr/sbin/service networking restart
